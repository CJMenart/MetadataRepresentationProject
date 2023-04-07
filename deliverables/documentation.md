# Name of the Knowledge Graph
**Authors:** Jehan Fernando, Chris Menart, Alex Moore

## Use Case Scenario
### Narrative 
Adapted from `use-case.md`.

### Competency Questions
Adapted from `use-case.md`.

### Integrated Datasets
Adapted from `use-case.md`.

### References
Adapted from `use-case.md`.

## Modules
<!-- There should be one module section per module (essentially per key-notion) -->
### Car
**Source Data:** Cityscapes Dataset

#### Description
Cars are of obvious interest to a system concerned with traffic and roads. One of the most obvious pieces of information to track about cars would be make, model, or other forms of classification. But after debate, we chose not to include these details, resulting in the lightest schema in the ontology. What we care about with respect to vehicles is rather where they are (which is covered by the PotentialObstacle schema) and where they are going.

One of the core imagined functions of our KG is reasoning over what meanuevers are possible for a self-driving vehicle to perform, and which ones it is actually allowed to do. Here, these will be represented by a controlled vocabulary, which we can iterate over and "check" against the existence of things which might make them disallowed. This same controlled vocabulary can be used to track the actions currently being executed by our neighbors.

Theoretically, these could use the Events pattern from MODL, but using ParticipantRoles or SpatioTemporalExtents would significantly increase the complexity of our ontolgoy and does not seem to fit directly into our use cases.

![schema-diagram](../schema-diagrams/Car.png)


### Intersection
**Source Pattern:** Collection
**Source Data:** Team annotations to the Cityscapes Dataset (found under "Data Wrangling")

#### Description
Intersection was the latest addition to the ontology. At first, it was a property by which Lanes pointed to each other, a way of determining which locations in a Scenario could be reached from one another. However, we quickly realized that Intersection needed to be reified so that more details about an intersection could be tracked--to begin with, the intersection of an arbitrary number of lanes of traffic at once. 

An Intersection is a collection of lanes which tracks the direction of its attendant lanes--which are incoming or outgoing--and also their cardinality, i.e. what order the roads at an intersection can be found by counting clockwise or counterclockwise around it. We closely considered both the bag and ordered list patterns from MODL to represent this strucutre, but neither felt perfectly appropriate. There are several intricacies specific to traffic intersection, such as the additional pieces of information noted above. Lanes can also touch more than one intersection (in fact, up to two).

![schema-diagram](../schema-diagrams/Intersection.png)


### Lane
**Source Data:** Team annotations to the Cityscapes Dataset (found under "Data Wrangling")

#### Description
The "Lane" class represents a drivable segment of road that vehicles may proceed along. A single Lane never crosses an intersection; all parts of the road on the far side of an intersection count as a new lane. You can picture Intersections as nodes on a graph, and Lanes as edges connecting them. 

In fact, all Lanes have a direction relative to at least one Intersection. This is how their direction is specified. If an intersection is not within visual range, in a given scenario, an assumption is made that the Lane is emanating from an Intersection some distance behind the Self vehicle, called the "Imaginary Intersection". 

Another natural unit of consideration for traffic-related reasoning is the "Road". In this ontology, Lanes are the most-used fundamental unit, but Roads do exist, as a collection of Lanes. In fact, a Road is a doubly-linked list of lanes. Lanes use the "directlyLeftOf" and "directlyRightOf" to represent lanes that are adjacent to each other with no other surfaces in between. This is important for determining which lanes can be traversed by cutting across a road, whether by a car performing a lane change or a pedestrian walking through a crossing. Most of the time, these transitive relationships are enough for reasoning about Lanes. Road is technically made redundant by them, but retained not only because it may have future use but for making some rules and axioms considerably more conscise. Determining whether Lanes are in the same Road is simpler to express than checking whether two Lanes are rechable via a chain of leftOf and rightOf relationships.


![schema-diagram](../schema-diagrams/Lane.png)


### Potential Obstacle
**Source Data:** Cityscapes Dataset

#### Description
Obstacles (or Potential Obstacles) represent things on the road that could block our driving (or things which could potentially end up on the road and do so). Theoretically an AgentRole could be used to represent Obstacles, but we concluded that this seemed to represent unnecessary overhead. 

What we need to know about an PotentialObstacle, and what is modeld, is its position, and, if relevant, its movement in space. Specifically, positions and movements are modeled in terms of which lanes an obstalce is obstructing and which lanes it might obstruct. The Obstacle class is used to mark PotentialObstacles which have become actual Obstacles, that is, occupy space in the road. 

![schema-diagram](../schema-diagrams/PotentialObstacle.png)


### Scenario
**Source Data:** Cityscapes Dataset

#### Description
The scenario is the key notion that organizes all other information in this knowledge graph. Each scenario represents a given image of a traffic situation from the point-of-view of a vehicle in it. Using the traffic image, we may determine the lanes and intersections, as well as all potential obstacles and traffic instruction indicators that may affect our queries regarding potential available maneuevers. All Lanes, Intersections, and obstacles potential or realized belong to a particular Scenario. Additionally, each traffic image will reveal environmental information that may be relevant such as weather conditions, outside temperature, and time of day. These are tracked in the Ontology via several Stub patterns.

![schema-diagram](../schema-diagrams/Scenario.png)


### Traffic Instruction Indicator
**Source Data:** The Cityscapes dataset and team annotations to it (found under "Data Wrangling")

#### Description
This key notion encompasses any physical object on or near the road that provides information to drivers, such as road or traffic signs, road markings, and traffic lights. (We exclude lane lines from this definition). Each Traffic Instruction Indicator conveys a traffic instruction, represented using a controlled vocabulary, applied to a given lane or lanes. These instructions will provide information and/or restrictions to the possible maneuvers for the vehicle.

![schema-diagram](../schema-diagrams/TrafficInstructionIndicator.png)



#### Axioms
* `axiom in manchester syntax` <br />
natural language description
* `axiom in manchester syntax` <br />
natural language description

#### Remarks
* Any remarks re: usage

## The Overall Knowledge Graph
### Namespaces
* prefix: namespace
* prefix: namespace

### Schema Diagram
![schema-diagram](./schema-diagram.png)

### Axioms
* `axiom in manchester syntax` <br />
natural language description
* `axiom in manchester syntax` <br />
natural language description

### Usage
Adapted from `validation.md`, i.e., the competency questions + SPARQL queries.


