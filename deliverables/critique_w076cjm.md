# Critique Assignment
**Author:** given name + family name

## Group 1: The Airplane Group
**Members:** Antrea, Erin, and Sydney

### Summary
Group 1's ontology was structured around airplanes. The knowledge graph was used to store and retrieve information on planes and plane parts, their models, and a single type of event from an aircraft's history, crashes.

### Strengths
I appreciated this group's use of graphical notation for axioms, which did, indeed, make them easier to read quickly. 

It was also neat to learn how literal values could be inserted into SPARQL queries. 

The use of stubs to model numerous bits of data was a good form of re-use, which ought to help the graph remain more maintainable, and the same goes for the re-use of "Temporal Entity" in dealing with crashes.

### Weaknesses
There were a couple of unusual decisions in designing/naming class hierarchies in this ontology, following a pattern, which I do not agree with. First, as discussed in class, PlaneModel was listed as a subclass of Plane. This was explained with the rationale, "A Piper (a type of plane) is a Plane, and a Cessna (another type of Plane) is a Plane, and so on." But this doesn't really follow. Even according to Object-Oriented Programming, the proper way to express this would be to state that each of these classes was a subclass of Plane individually. I think the confusion stemmed from the way that Controlled Vocabularies are expressed in this course's knowledge graphs: Piper (a member of a controlled vocabulary) is a "subclass" of PlaneModel. Therefore, making PlaneModel a subclass of Plane efficiently makes all the types Plane classes, right! But expressing "Piper" as en element of a controlled vocabulary implies that the object "Piper" is a type, a model, not a *specific* physical Plane, and so ultimately I don't think this is a good representation. 

A similar-looking pattern occurred relating to crashes. The group appears to have made "occuredOnDate" (whose range is TemporalEntities) a property of CrashType, not a property of a Crash itself. I could make little sense of this until the later discussion on Plane and PlaneModels clarified the thinking at play.

Finally, I was uncertain if "asString" was an appropriate property to put in a KG, especially given that everything in this graph was already represented as a string to begin with.


## Group 3: SOL of Life
**Members:** Brandon, Ryan, and Mega

### Summary
This group's ontology was space-related, specifically aimed at the use case of supporting asteroid mining. Relevant information that was tracked included the positions and paths of asteroids, as well as known information about their mineral contents determined by spectrography.

### Strengths

This group's graph included a large amount of re-use of existing ontology design patterns. In addition to several patterns from MODL, they used a patterns from something called "SOSA".

The Result and Quantity pattern was clearly a useful way to add extensibility and maintainability to a graph which might incorporate lots of nuemrical measurements from different sources in any future life.

All in all, this was the most complete knowledge graph produced by the course, in the sense of fulfilling its stated remit and looking like a KG which might actually exist in the real world. The most serious strength of the group was their ability to define a project scope which was amenable to the production fo a useful KG and then keep that scope under tight rein. But this to be expected given that members of this group are existing members of the KASTLE lab.


### Weaknesses

Though probably justifiable, it was unclear whether using the "EntityWithProvenance" pattern was truly necessary for most of the information in the graph. I don't believe that provenance ever arose when handling any of the competency questions.

There are two different kinds of "name" strings, stored directly as xsd primitives pointed to directly by an asteroid. It may make better sense to combine these two representations under the banner of a single object, for future maintainability. 

While nitpicky, some of the rectangles in the project's diagrams were rounded, and some were not. I spent a couple of minutes attempting to determine if this represented anything rather than being a function of when the group remembered to adjust the node's shape.