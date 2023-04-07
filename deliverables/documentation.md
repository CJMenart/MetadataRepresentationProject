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

#### Axioms
* `Car SubClassOf conductingManeuver exactly one Maneuver.`  
	"A Car is always conducting exactly one Maneuver."

#### Remarks
* Any remarks re: usage

### Intersection
**Source Pattern:** Collection
**Source Data:** Team annotations to the Cityscapes Dataset (found under "Data Wrangling")

#### Description
Intersection was the latest addition to the ontology. At first, it was a property by which Lanes pointed to each other, a way of determining which locations in a Scenario could be reached from one another. However, we quickly realized that Intersection needed to be reified so that more details about an intersection could be tracked--to begin with, the intersection of an arbitrary number of lanes of traffic at once. 

An Intersection is a collection of lanes which tracks the direction of its attendant lanes--which are incoming or outgoing--and also their cardinality, i.e. what order the roads at an intersection can be found by counting clockwise or counterclockwise around it. We closely considered both the bag and ordered list patterns from MODL to represent this strucutre, but neither felt perfectly appropriate. There are several intricacies specific to traffic intersection, such as the additional pieces of information noted above. Lanes can also touch more than one intersection (in fact, up to two).

![schema-diagram](../schema-diagrams/Intersection.png)

#### Axioms
* `TouchingIntersection SubClassOf hasDirection exactly 1 Direction`  
	"A TouchingIntersection has exactly one Direction"
* `TouchingIntersection SubClassOf hasCardinality exactly 1 Cardinality`  
	"A TouchingIntersection has exactly one Lane"
* `TouchingIntersection SubClassOf inverse touchesIntersection exactly 1 Lane`  
	"A TouchingIntersection has exactly one Cardinality"
* `TouchingIntersection SubClassOf inverse touchesLane exactly 1 Intersection`  
	"A TouchingIntersection has exactly one Intersection"
* `Scenario SubClassOf hasIntersection exactly one ImaginaryIntersection`  
	"A Scenario has exacty one Intersection which is an ImaginaryIntersection."

#### Remarks
* Any remarks re: usage

### Lane
**Source Data:** Team annotations to the Cityscapes Dataset (found under "Data Wrangling")

#### Description
The "Lane" class represents a drivable segment of road that vehicles may proceed along. A single Lane never crosses an intersection; all parts of the road on the far side of an intersection count as a new lane. You can picture Intersections as nodes on a graph, and Lanes as edges connecting them. 

In fact, all Lanes have a direction relative to at least one Intersection. This is how their direction is specified. If an intersection is not within visual range, in a given scenario, an assumption is made that the Lane is emanating from an Intersection some distance behind the Self vehicle, called the "Imaginary Intersection". 

Another natural unit of consideration for traffic-related reasoning is the "Road". In this ontology, Lanes are the most-used fundamental unit, but Roads do exist, as a collection of Lanes. In fact, a Road is a doubly-linked list of lanes. Lanes use the "directlyLeftOf" and "directlyRightOf" to represent lanes that are adjacent to each other with no other surfaces in between. This is important for determining which lanes can be traversed by cutting across a road, whether by a car performing a lane change or a pedestrian walking through a crossing. Most of the time, these transitive relationships are enough for reasoning about Lanes. Road is technically made redundant by them, but retained not only because it may have future use but for making some rules and axioms considerably more conscise. Determining whether Lanes are in the same Road is simpler to express than checking whether two Lanes are rechable via a chain of leftOf and rightOf relationships.


![schema-diagram](../schema-diagrams/Lane.png)

#### Axioms
* `Lane SubClassOf directLeftOf max 1 Lane`  
	"A Lane can be directly left of at most one other Lane."
* `Lane SubClassOf directRightOf max 1 Lane`   
	"A Lane can be directly right of at most one other Lane."
* `directLeftOf inverse of directRightOf`  
	"If one Lane is directly left of another Lane, the second Lane is directly right of the first Lane."
* `Lane SubClassOf visiblyEndsAt max 1 Distance`   
	"A Lane has at most one Distance away where it visibly ends."
* `Road SubClassOf inverse inRoad min 1 Lane`   
	"A Road has at least one Lane"
* `Lane SubClassOf touchesIntersection min 1 TouchingIntersection`   
	"A Lane always touches at least one Intersection."
* `Lane SubClassOf touchesIntersection max 2 TouchingIntersection`  
	"A Lane always touches at most two Intersections."
* `Lane SubClassOf inRoad exactly 1 Road`  
	"Every Lane is in exactly one Road"
* `Distance SubClassOf hasValue some xsd:float`  
	"A Distance is represented by a floating-point value."

#### Remarks
* Any remarks re: usage

### Potential Obstacle
**Source Data:** Cityscapes Dataset

#### Description
Obstacles (or Potential Obstacles) represent things on the road that could block our driving (or things which could potentially end up on the road and do so). Theoretically an AgentRole could be used to represent Obstacles, but we concluded that this seemed to represent unnecessary overhead. 

What we need to know about an PotentialObstacle, and what is modeld, is its position, and, if relevant, its movement in space. Specifically, positions and movements are modeled in terms of which lanes an obstalce is obstructing and which lanes it might obstruct. The Obstacle class is used to mark PotentialObstacles which have become actual Obstacles, that is, occupy space in the road. 

![schema-diagram](../schema-diagrams/PotentialObstacle.png)

#### Axioms
* `Position SubClassOf onLane max 2 Lane`   
	"A Position is always in at most 2 Lanes."
* `RelToLane SubClassOf relation exactly 1 Left/Right/On`   
	"The Position of a Potential Obstacle is either on a Lane, or to the right or left of a Lane."
* `Position SubClass hasRelativity exactly one RelToLane`  
* `RelToLane SubClass relToLane exactly one Lane`  
	"A Position is always given relative to a single Lane."
* `Motion SubClassOf direction exactly one Left/Right`  
	"A Motion is either to the left or right" (implicitly relative to the current Road.)
* `Motion SubClassOf towardsLane min 1 Lane`  
	"A Motion is always twoards at least one Lane."  
* `Obstacle SubClassOf relToLane o relativity some On  (This manchester is almost certainly wrong)`  
	"If the Position of a Potential Obstacle is not on any Lanes, that PotentialObstacle is not an Obstacle. Otherwise, it is."

#### Remarks
* Any remarks re: usage

### Scenario
**Source Data:** Cityscapes Dataset

#### Description
The scenario is the key notion that organizes all other information in this knowledge graph. Each scenario represents a given image of a traffic situation from the point-of-view of a vehicle in it. Using the traffic image, we may determine the lanes and intersections, as well as all potential obstacles and traffic instruction indicators that may affect our queries regarding potential available maneuevers. All Lanes, Intersections, and obstacles potential or realized belong to a particular Scenario. Additionally, each traffic image will reveal environmental information that may be relevant such as weather conditions, outside temperature, and time of day. These are tracked in the Ontology via several Stub patterns.

![schema-diagram](../schema-diagrams/Scenario.png)

#### Axioms
* `Scenario SubClassOf hasEnviornment exactly 1 Environment`  
	"A Scenario has exactly one Environment"
* `Environment SubClassOf hasTemperature at most 1 Temperature`  
	"An Environment has up one Temperature."
* `Scenario SubClassOf containsLane min 1 Lane`  
	"A Scenario contains at least one Lane."
* `PhysicalThing SubClassOf inverse hasThing exactly 1 Scenario`  
	"Every PhysicalThing is within exactly one Scenario."
* `Scenario SubClassOf hasIntersection min 1 Intersection`  
	"A Scenario has at least one Intersection"
* `Scenario SubClassOf aboutCar exactly 1 Self`  
	"A Scenario has exactly one Self corresponding to the user's vehicle"
* `Temperature SubClassOf hasValue some xsd:integer`  
	"A Temperature is represented as an integer value"

#### Remarks
* Any remarks re: usage

### Traffic Instruction Indicator
**Source Data:** The Cityscapes dataset and team annotations to it (found under "Data Wrangling")

#### Description
This key notion encompasses any physical object on or near the road that provides information to drivers, such as road or traffic signs, road markings, and traffic lights. (We exclude lane lines from this definition). Each Traffic Instruction Indicator conveys a traffic instruction, represented using a controlled vocabulary, applied to a given lane or lanes. These instructions will provide information and/or restrictions to the possible maneuvers for the vehicle.

![schema-diagram](../schema-diagrams/TrafficInstructionIndicator.png)

#### Axioms
* `Traffic Instruction Indicator (TII) SubClassOf conveys exactly 1 Traffic Instruction`  
	"Traffic Instruction Indicator (TII) conveys a single Traffic Instruction"
* `Traffic Instruction Indicator (TII) SubClassOf hasCategory exactly 1 Restriction/Warning/Info`  
	"Traffic Instruction Indicator (TII) has exactly one category of Restriction/Warning/Info"
* `Traffic Sign DisjointWith Traffic Light`  
        "A Traffic Sign is mutually exclusive from Traffic Light"
* `Traffic Light DisjointWith Road Marking`    
        "A Traffic Light is mutually exclusive from  Road Marking"
* `Traffic Sign DisjointWith Road Marking`  
	"Traffic Light, Road Marking, and Traffic Sign are all mutually exclusive types of Traffic Instruction Indicator (TII)."

#### Remarks
* Any remarks re: usage

## The Overall Knowledge Graph
### Namespaces
* prefix: namespace
* prefix: namespace

### Schema Diagram
![schema-diagram](./schema-diagram.png)

### Axioms
* `T SubClassOf for-all hasValue only xsd:AnyValue`  
	"All stubs (using the hasValue relationship) point to an xsd primitive."

### Usage
Adapted from `validation.md`, i.e., the competency questions + SPARQL queries.


