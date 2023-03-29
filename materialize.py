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
"ex": Namespace("https://example.com/"),
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


def main(markup_file, cityscapes_root):


    # Initialize an empty graph
    graph = init_kg()


    # Read manual markup
    with open(markup_file, 'r') as file:
        markup = file.readlines()
    markup = tabs_to_nest(markup)
    
    for scenario in markup:
        add_scenario_markup(graph, scenario)
        add_scenario_json(graph, scenario[0], cityscapes_root)

    TODO TODO TODO
    

    # Save
    output_file = "output.ttl"
    temp = graph.serialize(format="turtle", encoding="utf-8", destination=output_file)
    
    
def tabs_to_nest(textlines):
    overall=[]
    
    for line in textlines:
        ntabs = line.count('\t')
        dest = overall
        for t in range(ntabs):
            dest = dest[-1][1]
        if not line.isspace():
            dest.append((line.strip(), []))
    return overall
    
    #TODO add roads/lanes/whatever to scenario too
def add_scenario_markup(graph, scenario):
    posInd = 0
    imname = scenario[0][:scenario[0].index('leftImg8bit.png')-1]
    graph.add((pfs['ex'][imname], a, pfs['ex']['Scenario']))
    for road_or_intr in scenario[1]:
        if 'Road' in road_or_intr:
            # Road
            roadname = f"{imname}_{road_or_intr[0].strip()}"
            graph.add((pfs['ex'][roadname], a, pfs['ex']["Road"]))
            prevlanename = None
            for lane in road_or_intr[1]:
                lanename = f"{roadname}_{lane[0].strip()}"
                graph.add((pfs['ex'][lanename], a, pfs['ex']["Lane"]))
                graph.add((pfs['ex'][lanename], pfs['ex']['inRoad'], pfs['ex'][roadname]))
                
                # Tie lanes together 
                if prevlanename:
                    graph.add((pfs['ex'][lanename], pfs['ex']['directlyRightOf'], pfs['ex'][prevlanename]))
                prevlanename = lanename
                
                for entity in lane[1]:
                    # only records position rn. Type comes from other stuff
                    e_num = entity[0].lstrip().split()[0]
                    ename = f"{imname}_{e_num}"
                    graph.add((pfs['ex'][ename], pfs['ex']['hasPosition'], pfs['ex'][f'{imname}_pos{posInd}']))
                    graph.add((pfs['ex'][f'{imname}_pos{posInd}'], a, pfs['ex']['Position']))
                    graph.add((pfs['ex'][f'{imname}_pos{posInd}'], pfs['ex']['hasRelativity', pfs['ex'][f'{imname}_rel{posInd}']))
                    graph.add((pfs['ex'][f'{imname}_rel{posInd}'], pfs['ex']['relToLane'], pfs['ex'][lanename]))
                    graph.add((pfs['ex'][f'{imname}_rel{posInd}'], pfs['ex']['relativity'], pfs['ex']['On']))
                    posInd += 1
        else:
            # Intersections
            intname = f"{imname}_{road_or_intr[0].strip()}"
            graph.add((pfs['ex'][intname], a, pfs['ex']['Intersection']))
            if 'Imaginary' in intname:
                graph.add((pfs['ex'][intname], a, pfs['ex']['ImaginaryIntersection']))
                for cardinality in road_or_intr[1]:
                    cardiname = cardinality[0].strip()
                    for direction in cardinality[1]:
                        dirname = direction[0].strip()
                        for lane in direction[1]:
                            letters = lane[0].strip()
                            lanename = f"{imname}_Road{letters[0]}_Lane{letters[1]}"
                            touchname = TODO 
                            graph.add((pfs['ex'][touchname], a, pfs['ex']['TouchingIntersection']))
                            graph.add((pfs['ex'][intname], pfs['ex']['touchesLane'], pfs['ex'][touchname]))
                            graph.add((pfs['ex'][lanename], pfs['ex']['touchesIntersection'], pfs['ex'][touchname]))
                            graph.add((pfs['ex'][touchname], pfs['ex']['hasCardinality'], pfs['ex'][cardiname]))
                            graph.add((pfs['ex'][touchname], pfs['ex']['hasDirection'], pfs['ex'][dirname]))            
    
    #TODO scrape other objects from Cityscape--filter out those already in?
    
    
    # TODO apply Movement of moving vehicles
    
    
add_scenario_json(graph, imname, cityscapes_root):
    raise NotImplementedError