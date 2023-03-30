# Meeting Minutes 3/16/23

## Attendees
Chris, Alex, Jehan

## Agenda
Further developer schema and axioms.

## Notes / Comments
- Reified position of a potential obstacle in a given lane with a "Relative to Lane" class that points to "Lane" and "On/Left/Right" relativity to the lane.
- We have decided that any car in the given scene may have exactly one maneuver at any given time.
- How does the imaginary intersection determine the direction of each lane.
  - Based on the self car's position?
  - If so, we have not created any sense of "Self" in the schema.
  - We cannot say that "Self" is a "Car" because "Car" is currently a "Potential Obstacle" which will cause issues with "Self" blocking itself.
  - By saying "Self" is a "Physical Thing", we can give the self car a position and motion without referencing it as an obstacle.
- Talked about double yellow lines and the ability to pass slow/stopped vehicles in your lane.
  - Some debate about if you can turn left if there is a double yellow line: Normally you cannot, but certain states allow you to
  - We determined overtaking maneuver would add more work than we intended for the scope of this so we are including it as "future feature".
- Adding and reviewing current possible maneuvers

## Action Items
- Complete axioms
- Meet Tuesday
