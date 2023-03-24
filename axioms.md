# Traffic Scenario Ontology
![all-schemas](schema-diagrams/all-together.png)

## Scenarios
![schema-diagram](schema-diagrams/Scenario.png)

### Axioms
* Scenario SubClassOf hasEnviornment exactly 1 Environment  
	"A scenario has exactly one Environment"
* Environment SubClassOf hasTemperature at most 1 Temperature  
	"An environment has up one Temperature."
* Scenario SubClassOf containsLane min 1 Lane  
	"A Scenario contains at least one Lane."
* PhysicalThing SubClassOf inverse hasThing exactly 1 Scenario  
	"Every physical thing is within exactly one Scenario."
* Scenario SubClassOf hasIntersection min 1 Intersection  
	"A Scenario has at least one intersection"
* Scenario SubClassOf aboutCar exactly 1 Self  
	"A Scenario has exactly one Self corresponding to the user's vehicle"
* Temperature SubClassOf hasValue some xsd:integer  
	"A Temperature is represented as an integer value"

## Lanes
![schema-diagram](schema-diagrams/Lane.png)

### Axioms
* Lane SubClassOf directLeftOf max 1 Lane  
	"A Lane can be directly left of at most one other Lane."
* Lane SubClassOf directRightOf max 1 Lane   
	"A Lane can be directly right of at most one other Lane."
* directLeftOf inverse of directRightOf  
	"If one Lane is directly left of another Lane, the second lane is directly right of the first Lane."
* Lane SubClassOf visiblyEndsAt max 1 Distance   
	"A Lane has at most one Distance away where it visibly ends."
* Road SubClassOf inverse inRoad min 1 Lane   
	"A Road has at least one Lane"
* Lane SubClassOf touchesIntersection min 1 TouchingIntersection  
* Lane SubClassOf touchesIntersection max 2 TouchingIntersection  
	"A Lane always touches one or two Intersections."
* Lane SubClassOf inRoad exactly 1 Road  
	"Every Lane is in exactly one Road"
* Distance SubClassOf hasValue some xsd:float  
	"A Distance is represented by a floating-point value."
	
### Rules
* "All lanes that touch the same interesection and are inRoad of same road have the same cardinality"
* "If a Lane is directRightOf another Lane, both of those Lanes are inRoad the same Road."

## Intersections
![schema-diagram](schema-diagrams/Intersection.png)

### Axioms
* TouchingIntersection SubClassOf hasDirection exactly 1 Direction  
	"A touchingIntersection has exactly one direction"
* TouchingIntersection SubClassOf hasCardinality exactly 1 Cardinality  
	"A touchingIntersection has exactly one lane"
* TouchingIntersection SubClassOf inverse touchesIntersection exactly 1 Lane  
	"A touchingIntersection has exactly one cardinality"
* TouchingIntersection SubClassOf inverse touchesLane exactly 1 Intersection  
	"A touchingIntersection has exactly one intersection"
* Scenario SubClassOf hasIntersection exactly one ImaginaryIntersection  
	"A Scenario has exacty one intersection which is an Imaginary Intersection."
	
## Traffic Instruction Indicators
![schema-diagram](schema-diagrams/TrafficInstructionIndicator.png)

### Axioms
* Traffic Instruction Indicator (TII) SubClassOf conveys exactly 1 Traffic Instruction  
	"Traffic Instruction Indicator (TII) conveys a single traffic instruction"
* Traffic Instruction Indicator (TII) SubClassOf hasCategory exactly 1 Restriction/Warning/Info  
	"Traffic Instruction Indicator (TII) has exactly one category of Restriction, Warning, or Info"
* Traffic Sign DisjointWith Traffic Light  
        "A Traffic Sign is mutually exclusive from Traffic Light"
* Traffic Light DisjointWith Road Marking    
        "A Traffic Light is mutually exclusive from  Road Marking"
* Traffic Sign DisjointWith Road Marking  
	"Traffic Lights, Road Markings, and Traffic Signs are all mutually exclusive types of TIIs."

### Unneeded?
* Traffic Instruction Indicator (TII) SubClassOf PhysicalThing  
	"Every Traffic Instruction Indicator is a PhysicalThing (but only some TIIs are Potential Obstacles)"
* Road Marking SubClassOf Traffic Instruction Indicator (TII)  
* Traffic Sign SubClassOf Traffic Instruction Indicator (TII)  
* Traffic Light SubClassOf Traffic Instruction Indicator (TII)
	"Traffic Lights, Road Markings, and Traffic Signs are all types of TIIs."

## Potential Obstacles
![schema-diagram](schema-diagrams/PotentialObstacle.png)


### Axioms
* Position SubClassOf onLane max 2 Lane   
	"A Position is always in at most 2 lanes."
* RelToLane SubClassOf relation exactly 1 Left/Right/On   
	"The Position of a potential obstacle is either on a lane, or to the right or left of a lane."
* Position SubClass hasRelativity exactly one RelToLane  
* RelToLane SubClass relToLane exactly one Lane  
	"A Position is always given relative to a single Lane."
* Motion SubClassOf direction exactly one Left/Right  
	"A Motion is either to the left or right" (implicitly relative to the current road.)
* Motion SubClassOf towardsLane min 1 Lane  
	"A Motion is always twoards at least one Lane."  
* Obstacle SubClassOf relToLane o relativity some On  (This manchester is almost certainly wrong)  
	"If the Position of a Potential Obstacle is not on any Lanes, that PotentialObstacle is not an Obstacle. Otherwise, it is."

### Rules 
* "If a Position is in two Lanes, then one of those two lanes is directRightOf the other."
* "If a potential obstacles' motion is towards a lane then that motion is towards lanes that are directlyrightof/leftof and between that position and lane."

## Cars
![schema-diagram](schema-diagrams/Car.png)

### Axioms
* Car SubClassOf conductingManeuever exactly one maneuver.  
	"A Car is always conducting exactly one manuever."

## General (Not Module-Specific)
* T SubClassOf for-all hasValue only xsd:AnyValue  
	"All stubs (using the hasValue relationship) point to an xsd primitive."


## Rules about Maneuevers (not real/in graph at this time)
* "If one Lane is an ingoingLane of an intersection, and another lane is an outgoingLane of the same intersection, a lane switch maneuver between those two lanes is not allowed." (not really an axiom)
* "If there is a Car that is Moving on an Incoming Lane to an Intersection, any manuever which passes through that intersection from a different Lane, which is not Parallel to that Lane (has the same or opposite Cardinality), is not allowed???" (Intersecting Car Axiom)
* "If there is a Stop Sign at a Lane and Intersection, and we are not at that intersection, the only manuever allowed is the stop at spot and proceed."
* "If there is a Stop Light at a Lane and Intersection, any maneuver that is not the stop maneuever from that Lane is not allowed."
* "If there is a Speed Limit sign (in a Lane/Scenario?) the FormalSpeedLimit is equal to that sign's numerical value."
* "If there is a Priority Lane sign at an Intersection, the Intersecting Car Axiom does not apply if we are in the Lane containing the sign or Parallel to that Lane."(Gonna Keep it till later)
* "If a Lane contains a Turn Lane Marking, then Turn maneuvers from Parallel Lanes that do not contain Turn Lane Markings are not allowed." (?)
  * Also need to express that turn may be allowed only in one direction at that point
* "If a Lane contains a Left/Right Turn Only Lane Marking, then move Forwards maneuvers from that Lane are not allowed."
