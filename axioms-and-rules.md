# (In English) Rules Accompanying Schema Diagrams 
(May move these later)
(UNDER CONSTRUCTION, and in some cases already out of date)

Scenarios:
* "A scenario has exactly one Environment"
* "An environment has (up to?) one hasTemperature."
* "A scenario has exactly one currentLane (if currentLane stays a thing)"
* "Every physical thing is pointed to by exactly one scnenario via hasThing."

Lanes:
* "A Lane can be directLeftOf at most one other Lane."
* "A Lane can be directRightOf at most one other Lane."
* "If one Lane is directLeftOf another Lane, that lane is directRightOf the first Lane."
* "If a Lane is directRightOf another Lane, both of those Lanes are inRoad the same Road."
* "A Lane has at most one visiblyEndsAt relationship with a Distance."
* "A lane always touches one or two TouchingIntersections."


Intersections:
* If one Lane is an ingoingLane of an intersection, and another lane is an outgoingLane of the same intersection, a lane switch maneuver between those two lanes is not allowed."
* "An Intersection is a drivable surface which connects multiple lanes" (not really an axiom)
* "For every lane that touchesIntersection an Intersection, that Intersection points to that lane with one of either ingoingLane or outgoingLane."
* "If there is a Car that is Moving on an Incoming Lane to an Intersection, any manuever which passes through that intersection from a different Lane, which is not Parallel to that Lane, is not allowed???" (Intersecting Car Axiom)

Traffic Instructions:
* "Every Traffic Instruction Indicator is a PhysicalThing (but only some TIIs are Potential Obstacles)"
* Every TII is exactly one of a Traffic Light, a Traffic Sign, or a Road Marking."

Potential Obstacles:
* "A Position is always in at most lanes. If it is in two Lanes, then one of those two lanes is directRightOf the other."
* "If the Position of a PotentialObstacle is not onLane any Lanes, that PotentialObstacle is not an Obstacle. Otherwise, it is."
* "A motion is towardsLane at most one Lane."


Car:
* "A Car is always conductingManeuever exactly one manuever."


Attempt to Express Traffic Instructions with Axioms (Incomplete, might not work at all):
* "If there is a Stop Sign at a Lane and Intersection, and we are not at that intersection, any maneuver which passes through that intersection from that Lane is not allowed."
* "If there is a Stop Light at a Lane and Intersection, any maneuver which passes through that intersection from that Lane is not allowed."
* "If there is a Speed Limit sign (in a Lane/Scenario?) the FormalSpeedLimit is equal to that sign's numerical value."
* "If there is a Priority Lane sign at an Intersection, the Intersecting Car Axiom does not apply if we are in the Lane containing the sign or Parallel to that Lane."
* "If a Lane contains a Turn Lane Marking, then Turn maneuvers from Parallel Lanes that do not contain Turn Lane Markings are not allowed." (?)
  * Also need to express that turn may be allowed only in one direction at that point
* "If a Lane contains a Turn Only Lane Marking, then Continue(?) maneuvers from that Lane are not allowed."



# (Tentative) Rules Translated into Axioms


# (Tentative) Rules that can only be Translated in First-Order Logic