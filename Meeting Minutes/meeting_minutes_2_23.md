# Meeting Minutes 2/23/23
## Attendees
Chris, Alex, Jehan
## Agenda
 - Create some actual schema diagrams?
 - Solidify Schema from Tuesday?
 - Schedule mtgs for Spring Break Week

## Notes / Comments
 - Should "allowable Maneuvers" and "speed limit we should go" be objects in the KG attached to a Scenario?
 - Can we compute their values only using axioms?

Fine-Tuning Schema:
  - Weather should be an entity attached to Environment (like temp is)
  - How do we model Lanes? It seems like we want to model lanes
  - Proposed: leftOf and rightOf other lanes, physical objects can be inLane, lane may have a visible ending
  - We have not, so far, made the choice to model the Road as an Object
  - I picture 'directLeftOf' meaning a lane adjacent to another lane such that a vehicle or other object can slide from one to the other
  - We currently do not explicitly model buildings or non-drivable area. Adds complexity--may not be needed?
  - Talking about whether to model 'bad' maneuvers like "diagonal" need to be modeled
  - We can model lane changes and following a lane with current schema. What about turns onto other roads? 
  - We model intersecting roads as lanes with the intersects relationship (lanes also need direction)
  - By default, you can make a turn onto any intersecting lane as long as you turn into the direction that lane travels
  - You can be restricted by traffic instructions
  - Actually, we may need to *reify* the intersects relationship (between lanes) so that we can model properties of that relationship such as where it occurs
  - When we reify "Intersection", intuitive understanding of it immediately switches from "this is a relationship between 2 lanes" to "this is an intersection between two roads (meaning that an Intersection might, thus, relate many individual Lanes)." Is that actually a good change to make?
  - Jehan proposes tracking the direction of lanes as "ingoing" or "outgoing" relative to an intersection. The default rule is that you may only turn onto lanes Outgoing from an intersection, modified only by traffic instructions.
  - Alex: "This is becoming very quickly complicated"
  - Why did today become totally absorbed by debating Lane?
  - We have a plan, briefly, where the direction of a lane is actually a property connecting Lanes and Intersections. That's all you need to know. But then Jehan brings up that if there is a road with no visible intersections, you still need to know whether you can transfer to an adjacent lane--is it ongoing or incoming?
  - Jehan proposes tracking 2 kinds of directions--relative to intersections and relative to us--but Alex and I hate that.
  - I propose an "imaginary intersection" behind us (there was an intersection behind us at some point in the past) which lets us track whether the lanes are ingoing or outgoing relative to that
  - Alex: When do we switch to focusing on the intersection in front of us?
  - Alex declares roundabouts to be out of scope. Along with possibly other variants.
  - I don't think that turn maneuvers are going to be modeled as "left turn" or "right turn". I think they will be modeled as "turn into (a specific lane)" because of how we are modeling them now. This is also future-proof to modeling multi-road intersections even though we may not actually do that here
  - We probably have a class picking out the "Imaginary Intersection"

## Action Items
- We need to meet over Spring break at some point--let's pick a meeting time
- Chris will write more axioms based on our current model
- Alex will do some more diagrams, put them on the GitHub
- Jehan will write axioms and diagrams related to Lanes
- Let's meet Monday, in the Boffin lab, at 11 AM, to continue this discussion
