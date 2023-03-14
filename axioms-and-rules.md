
# Axioms accompanying schema diagrams 
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
* "A Lane has at most one visible ending."
* "A PhysicalThing can be in at most two lanes. If it is in two Lanes, then one of those two lanes is directRightOf the other."
* "If one Lane is directLeftOf another Lane, that Lane is directRightOf the first."
* "A lane always touches one or two Intersections."
* "If a Lane can be reached from another Lane through directRightOf and directLeftOf relationships, those two lanes are Parallel?" (But this is not the only time necessarily?!)
* If one Lane is an ingoingLane of an intersection, and another lane is an outgoingLane of the same intersection, a lane switch maneuver between those two lanes is not allowed."

Intersections:
* "An Intersection is a drivable surface which connects multiple lanes" (not really an axiom)
* "For every lane that touchesIntersection an Intersection, that Intersection points to that lane with one of either ingoingLane or outgoingLane."
* "If there is a Car that is Moving on an Incoming Lane to an Intersection, any manuever which passes through that intersection from a different Lane, which is not Parallel to that Lane, is not allowed???" (Intersecting Car Axiom)

Traffic Instructions:
* "Every Traffic Instruction Indicator is a PhysicalThing (but only some TIIs are Potential Obstacles)"
* Every TII is exactly one of a Traffic Light, a Traffic Sign, or a Road Marking."

Attempt to Express Traffic Instructions with Axioms (Incomplete, might not work at all):
* "If there is a Stop Sign at a Lane and Intersection, and we are not at that intersection, any maneuver which passes through that intersection from that Lane is not allowed."
* "If there is a Stop Light at a Lane and Intersection, any maneuver which passes through that intersection from that Lane is not allowed."
* "If there is a Speed Limit sign (in a Lane/Scenario?) the FormalSpeedLimit is equal to that sign's numerical value."
* "If there is a Priority Lane sign at an Intersection, the Intersecting Car Axiom does not apply if we are in the Lane containing the sign or Parallel to that Lane."
* "If a Lane contains a Turn Lane Marking, then Turn maneuvers from Parallel Lanes that do not contain Turn Lane Markings are not allowed." (?)
  * Also need to express that turn may be allowed only in one direction at that point
* "If a Lane contains a Turn Only Lane Marking, then Continue(?) maneuvers from that Lane are not allowed."

List of possible manuevers:
* Move Forward: continue on current lane
* Merge Left: change lanes to directlyLeftOf outgoing lane
* Merge Right: change lanes to directlyRightOf outgoing lane
* Turn Left: change lane to a left outgoing lane at an intersection
* Turn Right: change lane to a right outgoing lane at an intersection
* Stop: Come to a full stop
* Stop at designated spot adn continue: Stop at designated area and proceed with caution
* U-Turn: change lanes to directlyLeftOf incoming lane
* Reverse: traverse backwards on current lane
* Proceed with caution
* Decrease Speed
* Increase Speed