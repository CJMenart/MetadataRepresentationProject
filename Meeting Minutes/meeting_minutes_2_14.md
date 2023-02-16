# Meeting Minutes 2/14/23
## Attendees
Chris, Alex, Jehan
## Agenda
Develop Use Cases and Use Case Document

## Notes / Comments
Starting brainstorming on use cases…today! Making first commits to our project GitHub and everything. 
Brainstorms:
-Datasets: Cityscapes, other self-driving datasets, Wordnet (to get taxonomies)
-Possibility: self-driving car as user? Determining whether it is safe to stop from sensor detections and using knowledge graph
-Can use 3d info from some datasets for 3d spatial reasoning
-We could add navigation, and be answering navigation queries, like, “I want to drive somewhere with a great restaurant scene?” and where is the nearest place where that is? Something like that
-Trajectories, like we did on whiteboard in class—map trajectories of person, ask questions about where they are likely to go in the future. Is a ball going to roll into the street? 
-Want to be able to ask, what color will this light change to, if this light changes, what will move or stop? 
-Do I need to slow down based on the light?
-What happens if vehicle X crashes into a person? Versus, what happens if vehicle X crashes into a building? (in one case, the vehicle definitely stops, but in the other case, keeps going.)
-Is the room cluttered? (That might be a machine-learning question)
-What objects are sitting on the table/road (that could be based on spatial info)
-What kind of room is this depending on what’s in the room? A kitchen if there is a stove, a bedroom if there is a bed, etc.
-If this bottle falls, what will happen when it hits the ground? Does it break? Spill stuff? Etc?
-Alex: Would be based on material of bottle, is it open or closed, etc.
	How far is it off the ground
-Car maintenance related stuff? Like…symptom is X, possible issue is Y (“missing tail-light”) and then, what is the action you have to take. (Phone dealership, or does the car need to pull off the road). Jehan: Could model consequences of not taking an action/having an issue
-Commonsense reasoning about people: Being older or younger than other people, family relationships
	-Jehan: Answer the trolley-problem questions about who the self-driving car should hit
-We should probably assume that car user gets to use this as well
-Oh! What if, car is an electric car. There’s a trip planning element—can I get from A to B? Do I need to charge at a certain station before setting off, based on my driving range?
-How crowded a place is? 
-What kind of law enforcement stuff is relevant?
-Another angle is: Car needs to know the laws and be able to figure out how not to break them. Can ask stuff like: Is this proposed maneuver? Can I use the stereo or another feature here? Etc.
	-That actually overlaps with the questions about maintenenance vis a vis the ideas about consequences Jehan mentioned earlier
-So there’s parking and speed restrictions based on times of day, so. That’s the sort of thing the self-driving car needs to know! 
-Can only turn right on red if not during school hours, or only in curb lane. Am I in the curb lane? What is a curb lane?
-Which side of the road do I drive on? Based on geographic location
-One-way roads
-Noise restrictions
-Parking?? Stuff we can do about parking? Handicapped parking? I guess KG is not super-useful for “Do I fit in this parking spot?” But might be useful for height clearances
-Weight limits, weighing stations for trucks
-Trip planning could include mandatory breaks for truckers, or user-set…driving-time limits per day for a long trip
-Weather conditions as they affect driving (“Road may be icy”)
-What is time that railway crossings are closed (another kind of sign you need to know how to follow)
-Should I hit the dog instead of the person?
-What regions off-road might be safe in case of an emergency?
-Something about pets
-Tolls (that seems to fall under trip planning again)
-MPG falls under trip planning
-Will objects move? Will this metal slide off this truck? Will this ball roll off the driveway and into the road?)
-Prices of fuel (could be tricky b/c it changes so often)
-What is the Final Destination?
-Can I hit this car window with a hammer? (Material properties) Will it break?
-Safety features
-How fast can a car crash into something and the driver can still survive?
	-The driver has airbags but the passengers may not

Examine data situation:
We don’t yet have data for some of these proposed questions: Maintenance information, signage and driving laws, navigation/trip-planning stuff (although geographic information should be easy to come by)

## Action Items
Before Thursday:
-Everyone needs to look for more datasets
-Come into Thursday with an opinion about Competency Questions to keep, Narrative
Objective for Thursday Class:
-Complete use_cases.md
We will need to make decisions about what parts of knowledge graph we are willing to write by hand.
