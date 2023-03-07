# Meeting Minutes 3/7/23

## Attendees
Chris, Alex, Jehan

## Agenda
 - Unsure: Cogan did not post any updates
 - Work on Axioms

## Notes / Comments
 - Scenario ( =1 hasEnvironment.Environment
 - Scenario ( >=1 containsLane.Lane
 - Scenario ( >=0 hasThing.PhysicalThing
 - Scenario ( >=1 hasIntersection.Intersection

 - Environment ( =1 hasTemperature.xsd:float
 - Environment ( =1 hasDateTimeStamp.xsd:DateTimeStamp
 - Environment ( =1 hasWeatherCondition.WeatherCondition
 
 - Lane ( <=1 visiblyEndsAt.xsd:float
 - Lane ( <=1 directlyLeftOf.Lane
 - Lane ( <=1 directlyRightOf.Lane
 - Lane ( \lnot directlyRightOf.self
 - Lane ( \forall directlyRightOf \thereexists Lane ( directlyLeft.self
   - For all lanes that have a directlyRightOf relation to lane, there exists a lane that has directlyLeftOf relation to self
 - Lane ( \forall hasTrafficInstructionIndicator.TII
 - /forall Lane >=1 touchesIntersection.Intersection
 - /forall Lane <=2 touchesIntersection.Intersection
 - /forall Lane <=2 
 - Lane ( /forall directlyRightOf o inRoad -o inRoad.self
 - Lane ( /thereexists inRoad.Road


## Action Items
- Adjust diagram to include Road (Chris)
- Continue thinking about possible axioms, including Intersection
- Discuss possible maneuvers
