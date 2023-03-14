# Key Notions
* Potential Obstacle
  * Obstacles (or Potential Obstacles) represent things on the road that could block our driving (or things which could potentially end up on the road and do so). Theoretically an AgentRole could be used to represent Obstalces, but it was decided this represented unnecessary overhead. All we really need to know about an obstacle is its position (and possibly movement) in space--which lanes it is obstructing and which it might obstruct. We don't care about it at all outside of this, so the Obstacle class is used directly to represent any objects which can be obstacles, as seen in "PotentialObstacle.png"
  * Cars and Pedestrians are both things modeled in our knowledge graph. However, it has been determined that these subcategories of Obstacle will not recieve their own key notions. In the schema determined so far, we do not care to model the details of these different kinds of obstructions (such as model of car or physical attributes of pedestrians).
* Maneuever (as in "allowed thing the ego vehicle can do")
  * One of the core imagined functions of our KG is reasoning over what meanuevers are possible for a self-driving vehicle to perform, and which ones it is actually allowed to do. Here, these will be represented by a controlled vocabulary, which we can iterate over and "check" against the existence of things which might make them disallowed. 
  * Theoretically, these could use the Events pattern from MODL, but using ParticipantRoles or SpatioTemporalExtents would significantly increase the complexity of our ontolgoy and does not seem to fit directly into our use cases.
* Traffic Instruction Indicator
  * This key notion encompasses any physical object on or near the road that provides information to drivers, such as road or traffic signs, road markings, and traffic lights. (We exclude lane lines from this definition). Each Traffic Instruction Indicator conveys a traffic instruction, represented using a controlled vocabulary, applied to a given lane or lanes. These instructions will provide information and/or restrictions to the possible maneuvers for the vehicle. 
* Traffic Lane / Drivable Surface
   * This key notion encompases any surface that a vehicle/car can drive on. All lanes have a direction relative to an intersection, if an intersection is not within visual range an assumption is made that the lane is coming from an intersection. Lanes can have other lanes to the right and left. We are using "directlyLeftOf" and "directlyRightOf" to represent lanes that are adjacent to the lane without nothing in between. A manuever of switch lanes can be conducted if the lanes are directlyRightOF or directlyLeftOf and both lanes are in the same direction relative to the same intersection.
* Intersection
  * Originally, Intersection was a property by which Lanes pointed to each other. However, we quickly realized that Intersection needed to be reified so that more details about an intersection could be tracked--for starters, the intersection of an arbitrary number of lanes of traffic at once. An Intersection is a collection of lanes. We considered both the bag and ordered list patterns to model this strucutre, but neither were adequate. There are several intricacies specific to traffic intersection. And intersection needs to track the relative positions of the lanes it touches, so that our reasoner can determine whether manuevers are left or right turns based on the lanes they go to and from. Furthermore, a lane can touch more than one intersection. We determined that each lane in a given intersection will have a cardinality, represented as a controlled vocabulary, with respect to the user vehicle's position. Additionally, each lane at the intersection will also have a direction it points with respect to the intersection itself.
* A Scenario (Traffic Image)
  * The scenario is the key notion that combines all the other key notions using a given traffic image. Using the traffic image, we may determine the lanes and intersections, as well as all potential obstacles and traffic instruction indicators that may affect our queries regarding potential available maneuevers. Additionally, each traffic image will reveal environmental information that may be necessary such as weather conditions, outside temperature, and time of day.


* Notably absent thus far is an explicity notion of position in 3-dimensional space.

# Data Sources
* Potential Obstacle: Self-Driving Sensor Datasets (Cityscapes, BDD100K, KITTI)
  * WordNet could be useful if we model taxonomies of obstacles but our use cases do not appear to have necessitated this so far
* Maneuvers: This will have to be hand-entered
* Traffic Instruction Indicator: Traffic Signage Data, which will need to be manually translated to triples
* Traffic Lane: This can be obtained from BDD100K only (otherwise must be hand-entered)
* Navigation Scenarios: Self-Driving Sensor Datasets (Cityscapes, BDD100K, KITTI)
* Intersection: These may have to be tagged by hand

# Simplifying Assumptions
* We assume that our self-driving car drives on the road and never goes off-road
* (On probation) We assume that an intersection between no more than two roads at a time
* Pedestrians do not exist in intersections
* Cars which are required to yield to another entity with the right-of-way will always do so
* There are no relevant differences in behavior between different classes of cars: sedans, trucks, vans, etc. behave in the same way
* Other vehicles do not perform illegal maneuvers, such as parking permanently in the middle of a road

# List of possible manuevers:
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

