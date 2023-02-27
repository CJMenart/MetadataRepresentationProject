# Key Notions
* Potential Obstacle
  * Obstacles (or Potential Obstacles) represent things on the road that could block our driving (or things which could potentially end up on the road and do so). Theoretically an AgentRole could be used to represent Obstalces, but it was decided this represented unnecessary overhead. All we really need to know about an obstacle is its position (and possibly movement) in space--which lanes it is obstructing and which it might obstruct. We don't care about it at all outside of this, so the Obstacle class is used directly to represent any objects which can be obstacles, as seen in "PotentialObstacle.png"
  * Cars and Pedestrians are both things modeled in our knowledge graph. However, it has been determined that these subcategories of Obstacle will not recieve their own key notions. In the schema determined so far, we do not care to model the details of these different kinds of obstructions (such as model of car or physical attributes of pedestrians).
* Maneuever (as in "allowed thing the ego vehicle can do")
  * One of the core imagined functions of our KG is reasoning over what meanuevers are possible for a self-driving vehicle to perform, and which ones it is actually allowed to do. Here, these will be represented by a controlled vocabulary, which we can iterate over and "check" against the existence of things which might make them disallowed. 
  * Theoretically, these could use the Events pattern from MODL, but using ParticipantRoles or SpatioTemporalExtents would significantly increase the complexity of our ontolgoy and does not seem to fit directly into our use cases.
* Traffic Instruction Indicator
  * This key notion encompasses any physical object on the road that provides information to drivers, such as road or traffic signs, road markings, and traffic lights. (We exclude lane lines from this definition). Each Traffic Instruction Indicator is categorized using a controlled vocabulary,  
* Traffic Lane / Drivable Surface
* A navigation example / scenario
* Intersection
* Direction of lane (incoming/outgoing)
* Position in space (but may be tracked relative to the ego-vehicle in terms the vehicle cares about)

# Simplifying Assumption
* We assume that our self-driving car drives on the road and never goes off-road
* (On probation) We assume that an intersection between no more than two roads at a time

# Axioms accompanying schema diagrams 
(May move these later)

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
