# Traffic Scenario Ontology
![all-schemas](schema-diagrams/all-together.png)

## Scenarios
![schema-diagram](schema-diagrams/Scenario.png)

### Axioms (English)
* "A scenario has exactly one Environment"
* "An environment has (up to?) one hasTemperature."
* "A Scenario containsLane at least one Lane."
* "Every physical thing is pointed to by exactly one Scenario via hasThing."
* "A Scenario has atleast one intersection"
* "A Scenario has exactly one Self"

### Axioms (Manchester)
* Scenario SubClassOf hasEnviornment exactly 1 Environment
* Environment SubClassOf hasTemperature at most 1 Temperature
* Scenario SubClassOf containsLane min 1 Lane
* PhysicalThing SubClassOf inverse hasThing exactly 1 Scenario
* Scenario SubClassOf hasIntersection min 1 Intersection
* Scenario SubClassOf aboutCar exactly 1 Self

## Lanes
![schema-diagram](schema-diagrams/Lane.png)

### Axioms (English)
* "A Lane can be directLeftOf at most one other Lane."
* "A Lane can be directRightOf at most one other Lane."
* "If one Lane is directLeftOf another Lane, that lane is directRightOf the first Lane."
* "A Lane has at most one visiblyEndsAt relationship with a Distance."
* "A Road has atleast one lane"
* "A lane always touches one or two TouchingIntersections."
* "Every Lane is in at most one Road"  (could this be exactly 1?)

### Axioms (Manchester)
* Lane SubClassOf directLeftOf max 1 Lane
* Lane SubClassOf directRightOf max 1 Lane 
* directLeftOf inverse of directRightOf
* Lane SubClassOf visiblyEndsAt max 1 Distance 
* Road SubClassOf inverse inRoad min 1 Lane 
* Lane SubClassOf touchesIntersection min 1 TouchingIntersection
* Lane SubClassOf touchesIntersection max 2 TouchingIntersection
* Lane SubClassOf inRoad max 1 Road

### Rules
* "All lanes that touch the same interesection and are inRoad of same road have the same cardinality"
* "If a Lane is directRightOf another Lane, both of those Lanes are inRoad the same Road."

## Intersections
![schema-diagram](schema-diagrams/Intersection.png)

### Axioms (English)
* "A touchingIntersection has exactly one direction"
* "A touchingIntersection has exactly one lane"
* "A touchingIntersection has exactly one cardinality"
* "A touchingIntersection has exactly one intersection"
* "A Scenario has exacty one intersection which is an Imaginary Intersection."

### Axioms (Manchester)
* TouchingIntersection SubClassOf hasDirection exactly 1 Direction
* TouchingIntersection SubClassOf hasCardinality exactly 1 Cardinality
* TouchingIntersection SubClassOf inverse touchesIntersection exactly 1 Lane
* TouchingIntersection SubClassOf inverse touchesLane exactly 1 Intersection
* Scenario SubClassOf hasIntersection exactly one ImaginaryIntersection

## Traffic Instruction Indicators
![schema-diagram](schema-diagrams/TrafficInstructionIndicator.png)

### Axioms (English)
* "Traffic Instruction Indicator (TII) conveys a single traffic instruction"
* "Traffic Instruction Indicator (TII) has exactly one category of Restriction, Warning, or Info"
* "Every Traffic Instruction Indicator is a PhysicalThing (but only some TIIs are Potential Obstacles)"
* "Every TII is exactly one of a Traffic Light, a Traffic Sign, or a Road Marking."
* "TII can be restrictive" 

### Axioms (Manchester)
* Traffic Instruction Indicator (TII) SubClassOf conveys exactly 1 Traffic Instruction
* Traffic Instruction Indicator (TII) SubClassOf hasCategory exactly 1 Restriction/Warning/Info
* PhysicalThing SubClassOf Traffic Instruction Indicator (TII)
* Traffic Instruction Indicator (TII) SubClassOf Road Marking
* Traffic Instruction Indicator (TII) SubClassOf Traffic Sign
* Traffic Instruction Indicator (TII) SubClassOf Traffic Light
* Traffic Sign DisjointWith Traffic Light
* Traffic Light DisjointWith Road Marking
* Traffic Sign DisjointWith Road Marking

## Potential Obstacles
![schema-diagram](schema-diagrams/PotentialObstacle.png)

### Axioms (English)
* "A Position is always in at most 2 lanes."
* "The position of a potentialObstacle can be exactly one onLane, rightOfLane, leftOfLane"
* "If the Position of a PotentialObstacle is not onLane any Lanes, that PotentialObstacle is not an Obstacle. Otherwise, it is."
* "Motion has exactly one left/right relationship" (implicitly relative to the current road.)
* "Motion has atleast one towardsLane"  

### Axioms (Manchester)
* Position SubClassOf onLane max 2 Lane 
* 
* 
* Motion SubClassOf direction exactly one Left/Right 
* Motion SubClassOf towardsLane min 1 Lane

### Rules 
* "If a Position is in two Lanes, then one of those two lanes is directRightOf the other."
* "If a potential obstacles' motion is towards a lane then that motion is towards lanes that are directlyrightof/leftof and between that position and lane."

## Cars
![schema-diagram](schema-diagrams/Car.png)

### Axioms
* "A Car is always conductingManeuever exactly one manuever."



## Rules about Maneuevers (not real/in graph at this time)
* "If one Lane is an ingoingLane of an intersection, and another lane is an outgoingLane of the same intersection, a lane switch maneuver between those two lanes is not allowed." (not really an axiom)
* "If there is a Car that is Moving on an Incoming Lane to an Intersection, any manuever which passes through that intersection from a different Lane, which is not Parallel to that Lane (has the same or opposite Cardinality), is not allowed???" (Intersecting Car Axiom)
* "If there is a Stop Sign at a Lane and Intersection, and we are not at that intersection, any maneuver which passes through that intersection from that Lane is not allowed."
* "If there is a Stop Light at a Lane and Intersection, any maneuver which passes through that intersection from that Lane is not allowed."
* "If there is a Speed Limit sign (in a Lane/Scenario?) the FormalSpeedLimit is equal to that sign's numerical value."
* "If there is a Priority Lane sign at an Intersection, the Intersecting Car Axiom does not apply if we are in the Lane containing the sign or Parallel to that Lane."
* "If a Lane contains a Turn Lane Marking, then Turn maneuvers from Parallel Lanes that do not contain Turn Lane Markings are not allowed." (?)
  * Also need to express that turn may be allowed only in one direction at that point
* "If a Lane contains a Turn Only Lane Marking, then Continue(?) maneuvers from that Lane are not allowed."
