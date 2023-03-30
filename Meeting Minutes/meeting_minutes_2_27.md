# Meeting Minutes 2/23/23

## Attendees
Chris, Alex, Jehan

## Agenda
 - Finish schema diagrams?
 - Finalize list of key notions
 - Write justifications for key notions

## Notes / Comments

 - To recap: Intersections only have direction relative to interesections. But we always need to know if adjacent road lanes have opposite direction. Therefore, the "ImaginaryIntersection" allow us to always track this information. That needs to end up in the key notions notes probably.
 - Chris: Need ways to know which lanes are "right hand turns" or "left hand turns" relative to each other at a given intersection
 - We spend another half hour talking about intersections again
 - Alex working on diagrams while Chris begins justifying key notions 
 - Jehan proposes moving on from intersections, and also modeling Cars as different from Pedestrians in some way (mainly, in their assumed patterns of movement). He begins working on a schema for that 
 - Alex and Chris still end up arguing about intersections again for the remainder of the hour 
 - Briefly revisit whether Lane's "visibly ends at" should be an xsd:Float or a Fix, currently leaning toward float.
 - Alex: "How can we do this the easiest instead of making it super complicated?"
 - Discussing different kinds of traffic lights, discuss whether the appropraite reactions to those lights can be encoded given that we have thus far studiously avoided explicitly encoding any notion of time.

## Action Items
- Needs to add notes about data sources for each key notion (Chris)
- Review Potential Obstacle schema (Jehan)
- Review Intersection schema (Chris)
- Fully enumerate the enums for all controlled vocabularies (notably Maneuever) (assigned to Jehan)
- Finish justifying key notions (Alex)
