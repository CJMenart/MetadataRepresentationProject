# Traffic Scenario Ontology
![all-schemas](schema-diagrams/all-together.png)

## Scenarios
![schema-diagram](schema-diagrams/Scenario.png)

### Axioms (English)
* "A scenario has exactly one Environment"
* "An environment has (up to?) one hasTemperature."
* "A scenario has exactly one currentLane (if currentLane stays a thing)"
* "Every physical thing is pointed to by exactly one Scenario via hasThing."
* "A Scenario has atleast one intersection"
* "A Scenario has exactly one Self"

### Axioms (Manchester)
* Scenario SubClassOf =1 hasEnviornment some Environment
* Environment SubClassOf <=1 hasTemperature some Temperature
* Scenario SubClassOf =1 currentLane some Lane 
* PhysicalThing SubClassOf (inverse?) hasThing some Scenario

## Lanes
![schema-diagram](schema-diagrams/Lane.png)

### Axioms
* "A Lane can be directLeftOf at most one other Lane."
* "A Lane can be directRightOf at most one other Lane."
* "If one Lane is directLeftOf another Lane, that lane is directRightOf the first Lane."
* "If a Lane is directRightOf another Lane, both of those Lanes are inRoad the same Road."
* "A Lane has at most one visiblyEndsAt relationship with a Distance."
* "A Road has atleast one lane"
* "A lane always touches one or two TouchingIntersections."

### Rules
* "All lanes that touch the same interesection and are inRoad of same road have the same cardinality"


## Intersections
![schema-diagram](schema-diagrams/Intersection.png)

### Axioms
* "For every lane that touchesIntersection an Intersection, that Intersection points to that lane with one of either ingoingLane or outgoingLane." 
* "A touchingIntersection has exactly one direction"
* "A touchingIntersection has exactly one lane"
* "A touchingIntersection has exactly one cardinality"
* "A touchingIntersection has exactly one intersection"

## Traffic Instruction Indicators
![schema-diagram](schema-diagrams/TrafficInstructionIndicator.png)

### Axioms
* "Every Traffic Instruction Indicator is a PhysicalThing (but only some TIIs are Potential Obstacles)"
* Every TII is exactly one of a Traffic Light, a Traffic Sign, or a Road Marking."
* "TII can be restrictive" 

## Potential Obstacles
![schema-diagram](schema-diagrams/PotentialObstacle.png)

### Axioms
* "A Position is always in at most 2 lanes."
* "The position of a potentialObstacle relative to lane"
* "The position of a potentialObstacle can be exactly one onLane, rightOfLane, leftOfLane"
* "If the Position of a PotentialObstacle is not onLane any Lanes, that PotentialObstacle is not an Obstacle. Otherwise, it is."
* "Motion has exactly one left/right relationship" (implicitly relative to the current road.)
* "Motion has atleast one towardsLane"  

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