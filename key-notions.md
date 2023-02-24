# Key Notions
* Obstacle
* Maneuever (as in "allowed thing the ego vehicle can do")
* Traffic Instruction Element (such as sign, road marking, etc?)
* Traffic Lane / Drivable Surface
* A navigation example / scenario
* Status of vehicle in front of us?
* Position in space (but may be tracked relative to the ego-vehicle in terms the vehicle cares about)
* Intersection
* Direction of lane (incoming/outgoing)
* "Direction of lane is relative to the Intersection" 


# Axioms accompanying schema diagrams 
(May move these later)

Scenarios:
* "A scenario has exactly one Environment"
* "A scenario has exactly one currentLane (if currentLane stays a thing)"
* "Every physical thing is pointed to by exactly one scnenario via hasThing."

Lanes:
* "A Lane can be directLeftOf or directRightOf at most one other Lane. It has at most one visible ending."
* "A PhysicalThing can be in at most two lanes. If it is in twoLanes, then one of those two lanes is directRightOf the other."
* "If one Lane is directLeftOf another Lane, that Lane is directRightOf the first."
* "A Lane can intersect any number of Lanes"
* "An Intersection is a drivable surface which connects multiple lanes"
* "A lane always touches one or more Intersections."
* "If a Lane can be reached from another Lane through directRightOf and directLeftOf relationships, those two lanes are Parallel?" (But this is not the only time?)

Intersections:
* "For every lane that touchesIntersection an Intersection, that Intersection points to that lane with one of either ingoingLane or outgoingLane."
* "If there is a Car that is Moving on an Incoming Lane to an Intersection, any manuever which passes through that intersection from a different Lane, which is not Parallel to that Lane, is not allowed???" (Intersecting Car Axiom)

Traffic Instructions:
* "Every Traffic Instruction Indicator is a PhysicalThing (but only some TIIs are Potential Obstacles)"
* Every TII is exactly one of a Traffic Light, a Traffic Sign, or a Road Marking."

Attempt to Express Traffic Instructions with Axioms (Incomplete, might not work at all):
* "If there is a Stop Sign at an Intersection, and we are not at that intersection, any maneuver which passes through that intersection is not allowed."
* "Ditto for red traffic lights"
* "If there is a Speed Limit sign (in a Lane/Scenario?) the FormalSpeedLimit is equal to that sign's numerical value."
* "If there is a Priority Lane sign at an Intersection, the Intersecting Car Axiom does not apply if we are in the Lane containing the sign or Parallel to that Lane."
