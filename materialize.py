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
        add_scenario(graph, scenario)
    

    TODO TODO TODO
    
    # Initialize from a file
    # filename = "path/to/file"
    # with open(filename, "w") as f:
    #     graph.parse(f)

    # TODO delort
    kastle_members = ["Cogan", "Andrea", "Brandon"]
    for x in kastle_members:
        # Add a specific triple
        # g.add( (subject_node, predicate_node, object_node) )
        graph.add( (pfs["ex"][x], a, pfs["ex"]["Person"]) )




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
def add_scenario(graph, scenario):
    imname = scenario[0][:scenario[0].index('leftImg8bit.png')-1]
    graph.add((pfs['ex'][imname], a, pfs['ex']['Scenario']))
    for road_or_intr in scenario[1]:
        if 'Road' in road_or_intr:
            # Road
            roadname = f"{imname}_{road_or_intr[0].strip()}"
            graph.add((pfs['ex'][roadname], a, pfs['ex']["Road"]))
            for lane in road_or_intr[1]:
                lanename = f"{roadname}_{lane[0].strip()}"
                graph.add((pfs['ex'][lanename], a, pfs['ex']["Lane"]))
                graph.add((pfs['ex'][lanename], pfs['ex']['inRoad'], pfs['ex'][roadname]))
        else:
            # Intersections
            intname = f"{imname}_{road_or_intr[0].strip()}"
            graph.add((pfs['ex'][intname], a, pfs['ex']['Intersection']))
            
    
    #TODO scrape other objects from Cityscape--filter out those already in?
    
    
    # TODO tie lanes together 
    
    # TODO apply Movement of moving vehicles