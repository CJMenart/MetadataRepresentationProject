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

"A Lane can be directLeftOf or directRightOf at most one other Lane. It has at most one visible ending."
"A PhysicalThing can be in at most two lanes. If it is in twoLanes, then one of those two lanes is directRightOf the other."
"If one Lane is directLeftOf another Lane, that Lane is directRightOf the first."
"A Lane can intersect any number of Lanes"
"An Intersection is a drivable surface which connects multiple lanes"
"A lane always one or more intersections"
