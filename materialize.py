# Added imports 
import json
import numpy as np
from pathlib import Path
import os, sys
##### Graph stuff
import rdflib
from rdflib import URIRef, Graph, Namespace, Literal
from rdflib import OWL, RDF, RDFS, XSD, TIME
# Prefixes
name_space = "https://kastle-lab.org/"
# TODO edit these
pfs = {
"kl-res": Namespace(f"{name_space}lod/resource/"),
"kl-ont": Namespace(f"{name_space}lod/ontology/"),
"geo": Namespace("http://www.opengis.net/ont/geosparql#"),
"geof": Namespace("http://www.opengis.net/def/function/geosparql/"),
"sf": Namespace("http://www.opengis.net/ont/sf#"),
"wd": Namespace("http://www.wikidata.org/entity/"),
"wdt": Namespace("http://www.wikidata.org/prop/direct/"),
"dbo": Namespace("http://dbpedia.org/ontology/"),
"time": Namespace("http://www.w3.org/2006/time#"),
"ssn": Namespace("http://www.w3.org/ns/ssn/"),
"sosa": Namespace("http://www.w3.org/ns/sosa/"),
"cdt": Namespace("http://w3id.org/lindt/custom_datatypes#"),
"ex": Namespace("http://www.semanticweb.org/rochelle/ontologies/2023/2/untitled-ontology-5#"),
"alt": Namespace("http://www.semanticweb.org/rochelle/ontologies/2023/2/untitled-ontology-5#untitled-ontology-5#"),
"rdf": RDF,
"rdfs": RDFS,
"xsd": XSD,
"owl": OWL,
"time": TIME
}

# Initialization shortcut(s)
def init_kg(prefixes=pfs):
    kg = Graph()
    for prefix in pfs:
        kg.bind(prefix, pfs[prefix])
    return kg
# rdf:type shortcut
a = pfs["rdf"]["type"]

def no_whitespace(line):
    return "".join(line.split())


def main(markup_file, cityscapes_root):
    # Initialize an empty graph
    graph = init_kg()

    # Parse manual markup
    with open(markup_file, 'r') as file:
        markup = file.readlines()
    markup = tabs_to_nest(markup)
    
    for scenario in markup:
        # TODO scenario-level metadata (temp, car speed, etc.)
        print(f"main imname: {scenario[0]}")
        add_scenario_markup(graph, scenario)
        add_scenario_json(graph, scenario[0], cityscapes_root)
        guess_obstacles(graph, scenario[0])
                
    # TODO anything that's not Cityscapes
    
    # Save
    output_file = "materialization.ttl"
    temp = graph.serialize(format="turtle", encoding="utf-8", destination=output_file)
    print("Done!")
    
    
def tabs_to_nest(textlines):
    overall=[]
    for line in textlines:
        line = line.rstrip()
        ntabs = line.count('\t')
        line = line.lstrip()
        print(f"ntabs, line: {ntabs}, {line}")
        dest = overall
        for t in range(ntabs):
            dest = dest[-1][1]
        if line and not line.isspace():
            dest.append((line, []))
    return overall
    
    
def add_scenario_markup(graph, scenario):
    posInd = 0
    imname = scenario[0][:scenario[0].index('leftImg8bit.png')-1]
    graph.add((pfs['ex'][imname], a, pfs['ex']['Scenario']))
    for road_or_intr in scenario[1]:
        if 'Road' in road_or_intr:
            # Road
            roadname = f"{imname}_{no_whitespace(road_or_intr[0])}"
            graph.add((pfs['ex'][roadname], a, pfs['ex']["Road"]))
            prevlanename = None
            for lane in road_or_intr[1]:
                lanename = f"{roadname}_{no_whitespace(lane[0])}"
                graph.add((pfs['ex'][lanename], a, pfs['ex']["Lane"]))
                graph.add((pfs['ex'][lanename], pfs['ex']['inRoad'], pfs['ex'][roadname]))
                graph.add((pfs['ex'][imname], pfs['alt']['ContainsLane'], pfs['ex'][lanename]))
                
                # Tie lanes together 
                if prevlanename:
                    graph.add((pfs['ex'][lanename], pfs['ex']['directlyRightOf'], pfs['ex'][prevlanename]))
                prevlanename = lanename
                
                for entity in lane[1]:
                    # only records position rn. Type comes from other method
                    e_num = entity[0].lstrip().split()[0]
                    ename = f"{imname}_{e_num}"
                    if 'Self' in ename:
                        graph.add((pfs['ex'][ename], a, pfs['alt']['Self']))
                    if int(e_num) < 100:  # TII
                        graph.add((pfs['ex'][lanename], pfs['alt']['hasTrafficInstructionIndicator'], pfs['ex'][ename]))           
                    else:  # physical stuff
                        graph.add((pfs['ex'][ename], pfs['ex']['hasPosition'], pfs['ex'][f'{imname}_pos{posInd}']))
                        graph.add((pfs['ex'][f'{imname}_pos{posInd}'], a, pfs['ex']['Position']))
                        graph.add((pfs['ex'][f'{imname}_pos{posInd}'], pfs['ex']['hasRelativity'], pfs['ex'][f'{imname}_rel{posInd}']))
                        graph.add((pfs['ex'][f'{imname}_rel{posInd}'], pfs['ex']['relToLane'], pfs['ex'][lanename]))
                        graph.add((pfs['ex'][f'{imname}_rel{posInd}'], pfs['ex']['relativity'], pfs['ex']['Left/Right/On.On']))
                        posInd += 1
        else:
            # Intersections
            intname = f"{imname}_{no_whitespace(road_or_intr[0])}"
            print(f"intname: {intname}")
            graph.add((pfs['ex'][intname], a, pfs['alt']['Intersection']))
            graph.add((pfs['ex'][imname], pfs['ex']['hasIntersection'], pfs['ex'][intname]))
            if 'Imaginary' in intname:
                graph.add((pfs['ex'][intname], a, pfs['ex']['Imaginary%20Intersection']))
                for cardinality in road_or_intr[1]:
                    cardiname = pfs['ex']['Cardinality.' + cardinality[0].strip()]
                    for direction in cardinality[1]:
                        dirname = pfs['ex']['Direction.' + direction[0].strip()]
                        for lane in direction[1]:
                            letters = lane[0].strip()
                            lanename = f"{imname}_Road{letters[0]}_Lane{letters[1]}"
                            touchname = f"{imname}_{letters}2{intname[len('Intersection'):]}"
                            graph.add((pfs['ex'][touchname], a, pfs['ex']['Touching%20Intersection%20']))
                            graph.add((pfs['ex'][intname], pfs['ex']['touchesLane'], pfs['ex'][touchname]))
                            graph.add((pfs['ex'][lanename], pfs['ex']['touchesIntersection'], pfs['ex'][touchname]))
                            graph.add((pfs['ex'][touchname], pfs['alt']['hasCardinality'], pfs['ex'][cardiname]))
                            graph.add((pfs['ex'][touchname], pfs['ex']['hasDirection'], pfs['ex'][dirname]))            
    

    # TODO apply Movement of moving vehicles
    # Also Obstacle class
    
    
def add_scenario_json(graph, imname, cityscapes_root):
    cityscapes_root = Path(cityscapes_root)
    split = 'train'  # TODO detect this if more data is added 
    city = imname.split('_')[0]
    imname = imname[:imname.index('leftImg8bit.png')-1]
    print(f"add_scenario_json imname: {imname}")
    
    bbox3d_json = cityscapes_root / 'gtBbox3d' / split / city / (imname + '_gtBbox3d.json')
    with open(bbox3d_json, 'r') as f:
        bbox3d = json.load(f)
    add_vehicles(graph, imname, bbox3d)
    
    people_json = cityscapes_root / 'gtBboxCityPersons' / split / city / (imname + '_gtBboxCityPersons.json')
    with open(people_json, 'r') as f:
        people = json.load(f)
    add_pedestrian(graph, imname, people)
    
    semseg_json = cityscapes_root / 'gtFine' / split / city / (imname + '_gtFine_polygons.json')
    with open(semseg_json, 'r') as f:
        misc = json.load(f)
    add_misc(graph, imname, misc)
    
    meta_json = cityscapes_root / 'vehicle_sequence' / split / city / (imname + '_vehicle.json')
    with open(meta_json, 'r') as f:
        metadata = json.load(f)
    parse_scenario_metadata(graph, imname, metadata)
    

def add_vehicles(graph, imname, bbox3d):
    use_classes = ['car', 'truck', 'bus', 'train', 'motorcycle', 'bicycle', 'caravan']
    # ignore: tunnel, dynamic, trailer
        
    objects = bbox3d['objects']
    
    for obj in objects:
        if obj['label'] not in use_classes:
            continue
        oid = obj['instanceId']
        graph.add((pfs['ex'][f"{imname}_{oid}"], a, pfs['ex']['Car']))  # every vehicle is a car atm
        graph.add((pfs['ex'][f"{imname}_{oid}"], a, pfs['ex']['Potential%20Obstacle%20']))
        graph.add((pfs['ex'][imname], pfs['ex']['hasThing'], pfs['ex'][f"{imname}_{oid}"]))
        # TODO could revisit handling of position 
        if (pfs['ex'][f"{imname}_{oid}"], pfs['ex']['hasPosition'], None) in graph:
            # I like the contains syntax. Very Pythonic
            dist = np.linalg.norm(obj['3d']['center'])
            graph.add((pfs['ex'][f"{imname}_{oid}"], pfs['ex']['distanceDownLane'], Literal(dist)))
        

def add_pedestrian(graph, imname, people):
    """
    Takes a CityPersons JSON dictionary and modified it in place
    so classes have been mapped to the BDD100K system
    """
    use_classes = ['pedestrian', 'sitting person', 'person group', 'person (other)']
    # ignored: rider, ignore 
 
    for obj in people['objects']:
        if obj['label'] not in use_classes:
            continue 
        oid = obj['instanceId']
        graph.add((pfs['ex'][f"{imname}_{oid}"], a, pfs['ex']['Pedestrian']))
        graph.add((pfs['ex'][f"{imname}_{oid}"], a, pfs['ex']['Potential%20Obstacle%20']))
        graph.add((pfs['ex'][imname], pfs['ex']['hasThing'], pfs['ex'][f"{imname}_{oid}"]))
        # positions unknown--unless TODO we parse depth maps for estimate. 
        # Theoretically possible by extracting instance-label polygon and indexing into transformed depth map
        
        
def add_misc(graph, imname, instance_labels):

    use_classes = ['building', 'vegetation', 'pole', 'wall', 'traffic light', 'traffic sign']
    # Ignored: lots of stuff. Sky, road, self, various forms of 'not actually an object', etc...
    
    # schema missing description literal?
    misc_id = 0
    tii_id = 0
    for obj in instance_labels['objects']:
        if obj['label'] not in use_classes:
            continue
        if 'traffic' in obj['label']:
            tii_id += 1
            graph.add((pfs['ex'][f"{imname}_{tii_id}"], a, pfs['alt']['TrafficInstructionIndicator']))
            graph.add((pfs['ex'][imname], pfs['ex']['hasThing'], pfs['ex'][f"{imname}_{tii_id}"]))
        else:
            misc_id += 1
            graph.add((pfs['ex'][f"{imname}_{misc_id}"], a, pfs['alt']['Physical%20Thing']))
            graph.add((pfs['ex'][imname], pfs['ex']['hasThing'], pfs['ex'][f"{imname}_{misc_id}"]))
            

def guess_obstacles(graph, imname):
    # an attempt to apply materialization rules...written, unwritten, and hazarded at :P
    
    # Obstacles are PotentialObstacles that are on Lanes.
    # or can we just have the Reasoner do that?
    
    # But motion we have to do 
    # Cars we are kind of guessing. 
    # TODO pedestrians
    # find all subjects of any type
    for car, p, o in graph.triples((None, a, pfs['ex']['Car'])):
        pos = graph.value(car, pfs['ex']['hasPosition'])
        if not pos:
            continue 
        for _, _, relation in graph.triples((pos, pfs['ex']['hasRelativity'], None)):
            if graph.value(relation, pfs['ex']['relativity']) == pfs['ex']['Left/Right/On.On']:
                lane = graph.value(relation, pfs['ex']['relToLane'])
                # find out if lane has a reason to stop. Otherwise assume car is moving. 
                for backRelation, _, _ in graph.triples((None, pfs['ex']['relToLane'] , lane)):
                    backPos = graph.value(predicate = pfs['ex']['hasRelativity'], object=backRelation, any=False)
                    otherEntity = graph.value(predicate = pfs['ex']['hasPosition'], object=backPos, any=False)
                    stopInstructions = ['Traffic%20Instruction.StopSign', 'Traffic%20Instruction.RedLight']
                    stopInstructions = [pfs['ex'][inst] for inst in stopInstructions]
                    if any([(otherEntity, pfs['alt']['conveys'], si) in graph for si in stopInstructions]): 
                        graph.add((car, pfs['ex']['conductingManuever'], pfs['ex']['Manuever.GoingStraight']))
                        # check for it moving over other lanes?????? Add 'Motion' to it.
                    else:
                        graph.add((car, pfs['ex']['conductingManuever'], pfs['ex']['Stopped']))
            

def parse_scenario_metadata(graph, imname, metadata):
    metadata['speed']
    metadata['outsideTemperature']
    
    graph.add((pfs['ex'][f'{imname}_Self'], pfs['ex']['hasSpeed'], pfs['ex'][f'{imname}_ssp']))
    graph.add((pfs['ex'][f'{imname}_ssp'], a, pfs['ex']['SpeedMPS']))
    graph.add((pfs['ex'][f'{imname}_ssp'], pfs['alt']['hasValue'], Literal(metadata['speed'])))
    
    # Environment
    # Environment is under alt namespace
    # Weather%20Condition
    graph.add((pfs['ex'][imname], pfs['ex']['hasEnvironment'], pfs['ex'][f'{imname}_env']))
    graph.add((pfs['ex'][f'{imname}_env'], pfs['alt']['hasTemperature'], pfs['ex'][f'{imname}_tmp']))
    graph.add((pfs['ex'][f'{imname}_tmp'], pfs['alt']['hasValue'], Literal(metadata['outsideTemperature'])))
    graph.add((pfs['ex'][imname], pfs['alt']['hasWeatherCondition'], pfs['ex'][f'{imname}_weth']))
    graph.add((pfs['ex'][f'{imname}_weth'], pfs['ex']['hasWeatherType%20'], pfs['ex']['Weather%20Type.Sunny']))
    


if __name__=='__main__':
    main(sys.argv[1], sys.argv[2])