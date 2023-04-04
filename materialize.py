"""
Instructions to download data before running:
Cityscapes data downloaded from https://www.cityscapes-dataset.com/downloads/
You will need an academic account, so be a student or researcher

There are a list of products on this page. Each comes as a zipped directory containing files with similar formatting (usually)
Unzip all downloaded products in a file which you will pass to this program as the cityscapes_root argument
Products used (all from the training partition) are:
gtFine (semantic segmentation labels)
Cityscapes 3D Bounding Boxes
CityscapesPersons
'vehicle_sequence', aka scenario-level metadata

TODO use Depth

"""

import json
import numpy as np
from pathlib import Path
import os, sys
import cv2
##### Graph stuff
import rdflib
from rdflib import URIRef, Graph, Namespace, Literal
from rdflib import OWL, RDF, RDFS, XSD, TIME
# Prefixes
name_space = "https://kastle-lab.org/"
# TODO maybe delete prefixes we aren't actually using
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
"project": Namespace("http://www.semanticweb.org/CS7810/Driving/Project#"),
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
pre = pfs["project"]

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
        if line.startswith("#"):
            continue
        ntabs = line.count('\t')
        line = line.lstrip()
        #print(f"ntabs, line: {ntabs}, {line}")
        dest = overall
        for t in range(ntabs):
            dest = dest[-1][1]
        if line and not line.isspace():
            dest.append((line, []))
    return overall
    
    
def add_scenario_markup(graph, scenario):
    posInd = 0
    imname = scenario[0][:scenario[0].index('leftImg8bit.png')-1]
    graph.add((pre[imname], a, pre['Scenario']))
    for road_or_intr in scenario[1]:
        if 'Road' in road_or_intr[0]:
            # Road
            roadname = f"{imname}_{no_whitespace(road_or_intr[0])}"
            graph.add((pre[roadname], a, pre["Road"]))
            prevlanename = None
            for lane in road_or_intr[1]:
                lanename = f"{roadname}_{no_whitespace(lane[0])}"
                graph.add((pre[lanename], a, pre["Lane"]))
                graph.add((pre[lanename], pre['inRoad'], pre[roadname]))
                graph.add((pre[imname], pre['containsLane'], pre[lanename]))
                
                # Tie lanes together 
                if prevlanename:
                    graph.add((pre[lanename], pre['directlyRightOf'], pre[prevlanename]))
                    graph.add((pre[prevlanename], pre['directlyLeftOf'], pre[lanename]))
                prevlanename = lanename
                
                for entity in lane[1]:
                    beside = None
                    # only records position rn. Type comes from other method
                    entity_str = entity[0]
                    if 'Ends at' in entity_str:
                       distance = entity_str.lstrip().split()[2]
                       graph.add((pre[lanename], pre['visiblyEndsAt'], Literal(distance) ))
                       continue
                    
                    if entity_str.startswith('L'):
                        beside = 1
                        entity_str = entity_str[1:]
                    if entity_str.startswith('R'):
                        beside = 2
                        entity_str = entity_str[1:]
                    
                    e_num = entity_str.lstrip().split()[0]
                    ename = f"{imname}_{e_num}"
                    description = "".join(entity_str.lstrip().split()[1:])
                    if 'Self' in ename:
                        graph.add((pre[ename], a, pre['Self']))
                        graph.add((pre[imname], pre['aboutCar'], pre[ename]))
                        graph.add((pre[ename], pre['hasPosition'], pre[f'{imname}_pos{posInd}']))
                        graph.add((pre[f'{imname}_pos{posInd}'], a, pre['Position']))
                        graph.add((pre[f'{imname}_pos{posInd}'], pre['hasRelativity'], pre[f'{imname}_rel{posInd}']))
                        graph.add((pre[f'{imname}_rel{posInd}'], pre['relToLane'], pre[lanename]))
                        graph.add((pre[f'{imname}_rel{posInd}'], pre['relativity'], pre[f'Left-Right-On.On']))
                        posInd += 1
                    elif int(e_num) < 100:  # TII
                        graph.add((pre[lanename], pre['hasTrafficInstructionIndicator'], pre[ename])) 
                        graph.add((pre[ename], pre['conveys'], pre[f'TrafficInstruction.{description}']))
                    else:  # physical stuff
                        graph.add((pre[ename], pre['hasPosition'], pre[f'{imname}_pos{posInd}']))
                        graph.add((pre[f'{imname}_pos{posInd}'], a, pre['Position']))
                        graph.add((pre[f'{imname}_pos{posInd}'], pre['hasRelativity'], pre[f'{imname}_rel{posInd}']))
                        graph.add((pre[f'{imname}_rel{posInd}'], pre['relToLane'], pre[lanename]))
                        relativity = 'On' if beside is None else ('Left' if beside == 1 else 'Right')
                        graph.add((pre[f'{imname}_rel{posInd}'], pre['relativity'], pre[f'Left-Right-On.{relativity}']))
                        
                        if int(e_num) < 26000 and description:  # , probably pedestrian
                            graph.add((pre[ename], pre['hasMotion'], pre[f'{imname}_motion{posInd}']))
                            graph.add((pre[f'{imname}_motion{posInd}'], pre['direction'], pre[f'Left-Right.{description}']))
                        elif description:  # vehicle
                            graph.add(( pre[ename], pre['conductingManuever'], pre[f'Manuever.{description}']))
                        posInd += 1
        else:
            # Intersections
            intname = f"{imname}_{no_whitespace(road_or_intr[0])}"
            #print(f"intname: {intname}")
            graph.add((pre[intname], a, pre['Intersection']))
            graph.add((pre[imname], pre['hasIntersection'], pre[intname]))
            if 'Imaginary' in intname:
                graph.add((pre[intname], a, pre['ImaginaryIntersection']))
                for cardinality in road_or_intr[1]:
                    cardiname = pre['Cardinality.' + cardinality[0].strip()]
                    for direction in cardinality[1]:
                        dirname = pre['Direction.' + direction[0].strip()]
                        for lane in direction[1]:
                            letters = lane[0].strip()
                            lanename = f"{imname}_Road{letters[0]}_Lane{letters[1]}"
                            touchname = f"{imname}_{letters}2{no_whitespace(road_or_intr[0])}"
                            graph.add((pre[touchname], a, pre['TouchingIntersection']))
                            graph.add((pre[intname], pre['touchesLane'], pre[touchname]))
                            graph.add((pre[lanename], pre['touchesIntersection'], pre[touchname]))
                            graph.add((pre[touchname], pre['hasCardinality'], pre[cardiname]))
                            graph.add((pre[touchname], pre['hasDirection'], dirname))            
    
    
def add_scenario_json(graph, imname, cityscapes_root):
    cityscapes_root = Path(cityscapes_root)
    split = 'train'  # TODO detect this if more data is added 
    city = imname.split('_')[0]
    imname = imname[:imname.index('leftImg8bit.png')-1]
    #print(f"add_scenario_json imname: {imname}")
    
    bbox3d_json = cityscapes_root / 'gtBbox3d' / split / city / (imname + '_gtBbox3d.json')
    with open(bbox3d_json, 'r') as f:
        bbox3d = json.load(f)
    add_vehicles(graph, imname, bbox3d)

    # depthmap used to localize pedestrians
    disparity_png = cityscapes_root / 'disparity' / split / city / (imname + '_disparity.png')
    depth = parse_depth(disparity_png)
    
    people_json = cityscapes_root / 'gtBboxCityPersons' / split / city / (imname + '_gtBboxCityPersons.json')
    with open(people_json, 'r') as f:
        people = json.load(f)
    add_pedestrian(graph, imname, people, depth)
    
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
        graph.add((pre[f"{imname}_{oid}"], a, pre['Car']))  # every vehicle is a car atm
        graph.add((pre[f"{imname}_{oid}"], a, pre['PotentialObstacle']))
        graph.add((pre[imname], pre['hasThing'], pre[f"{imname}_{oid}"]))
        # TODO could revisit handling of position 
        if (pre[f"{imname}_{oid}"], pre['hasPosition'], None) in graph:
            # I like the contains syntax. Very Pythonic
            dist = np.linalg.norm(obj['3d']['center'])
            graph.add((pre[f"{imname}_{oid}"], pre['distanceDownLane'], Literal(dist)))
        

def add_pedestrian(graph, imname, people, depth):
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
        graph.add((pre[f"{imname}_{oid}"], a, pre['Pedestrian']))
        graph.add((pre[f"{imname}_{oid}"], a, pre['PotentialObstacle']))
        graph.add((pre[imname], pre['hasThing'], pre[f"{imname}_{oid}"]))
        # positions unknown--unless TODO we parse depth maps for estimate. 
        # Theoretically possible by extracting instance-label polygon and indexing into transformed depth map
        
        for _, _, pos in graph.triples((pre[f"{imname}_{oid}"], pre['hasPosition'], None)):
            rel = graph.value(pos, pre['hasRelativity'])
            relativity = graph.value(rel, pre['relativity'])
            if relativity == pre[f'Left-Right-On.On']:
                depth_estimate = average_depth(depth, *obj['bbox'])
                print(f'depth_estimate: {depth_estimate}')
                graph.add((pre[f"{imname}_{oid}"], pre['distanceDownLane'], Literal(depth_estimate)))
                
        
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
            graph.add((pre[f"{imname}_{tii_id}"], a, pre['TrafficInstructionIndicator']))
            graph.add((pre[imname], pre['hasThing'], pre[f"{imname}_{tii_id}"]))
        else:
            misc_id += 1
            graph.add((pre[f"{imname}_{misc_id}"], a, pre['PhysicalThing']))
            graph.add((pre[imname], pre['hasThing'], pre[f"{imname}_{misc_id}"]))
            

def guess_obstacles(graph, imname):
    # attempt to apply some materialization rules...written, unwritten, and hazarded at :P
    
    # Obstacles are PotentialObstacles that are on Lanes.
    # or can we just have the Reasoner do that?
    
    # But motion we have to do 
    # Cars we are kind of guessing. 
    # find all subjects of any type
    for car, p, o in graph.triples((None, a, pre['Car'])):
        pos = graph.value(car, pre['hasPosition'])
        if not pos:
            continue 
        for _, _, relation in graph.triples((pos, pre['hasRelativity'], None)):
            if graph.value(relation, pre['relativity']) == pre['Left-Right-On.On']:
                lane = graph.value(relation, pre['relToLane'])
                # find out if lane has a reason to stop. Otherwise assume car is moving. 
                for backRelation, _, _ in graph.triples((None, pre['relToLane'] , lane)):
                    backPos = graph.value(predicate = pre['hasRelativity'], object=backRelation, any=False)
                    otherEntity = graph.value(predicate = pre['hasPosition'], object=backPos, any=False)
                    # If car already conducting a maneuver, don't auto-decide it
                    if (otherEntity, pre['conductingManuever'], None) in graph:
                        continue  # TODO apply Motions to this depending
                    stopInstructions = ['TrafficInstruction.StopSign', 'TrafficInstruction.RedLight']
                    stopInstructions = [pre[inst] for inst in stopInstructions]
                    if any([(otherEntity, pre['conveys'], si) in graph for si in stopInstructions]): 
                        graph.add((car, pre['conductingManuever'], pre['Manuever.GoingStraight']))
                        # check for it moving over other lanes?????? Add 'Motion' to it.
                    else:
                        graph.add((car, pre['conductingManuever'], pre['Stopped']))
    for pedestrian, p, o in graph.triples((None, a, pre['Pedestrian'])):
        for _, _, motion in graph.triples((pedestrian, pre['hasMotion'], None)):
            for _, _, direction in graph.triples((motion, pre['direction'], None)):
                pos = graph.value(pedestrian, pre['hasPosition'])
                rel = graph.value(pos, pre['hasRelativity'])
                lane = graph.value(rel, pre['relToLane'])
                dirRel = pre['directlyRightOf'] if direction == pre['Left-Right.Right'] else pre['directlyLeftOf']
                lane = graph.value(lane, dirRel)
                while lane is not None:
                    graph.add((motion, pre['towardsLane'], lane))
                    lane = graph.value(lane, dirRel)


def parse_scenario_metadata(graph, imname, metadata):
    metadata['speed']
    metadata['outsideTemperature']
    
    graph.add((pre[f'{imname}_Self'], pre['hasSpeed'], pre[f'{imname}_ssp']))
    graph.add((pre[f'{imname}_ssp'], a, pre['SpeedMPS']))
    graph.add((pre[f'{imname}_ssp'], pre['hasValue'], Literal(metadata['speed'])))
    
    # Environment
    # Environment is under alt namespace
    # Weather%20Condition
    graph.add((pre[imname], pre['hasEnvironment'], pre[f'{imname}_env']))
    graph.add((pre[f'{imname}_env'], pre['hasTemperature'], pre[f'{imname}_tmp']))
    graph.add((pre[f'{imname}_tmp'], pre['hasValue'], Literal(metadata['outsideTemperature'])))
    graph.add((pre[imname], pre['hasWeatherCondition'], pre[f'{imname}_weth']))
    graph.add((pre[f'{imname}_weth'], pre['hasWeatherType'], pre['WeatherType.Sunny']))


def parse_depth(disparity_png):
    # Disparity->Depth computation constants posted by dataset authors here (https://github.com/mcordts/cityscapesScripts)
    disparity = cv2.imread(str(disparity_png), cv2.IMREAD_ANYDEPTH | cv2.IMREAD_UNCHANGED)
    #print(np.max(disparity))
    distance = ( disparity.astype(float) - 1. ) / 256
    distance[disparity == 0] = -1
    return distance


def average_depth(depth, x0, y0, w, h):
    box = depth[y0:y0+h, x0:x0+w]
    box = box[box!=-1]
    return np.mean(box)
    

if __name__=='__main__':
    main(sys.argv[1], sys.argv[2])