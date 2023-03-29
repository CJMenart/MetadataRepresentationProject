## Data Annotation ##

* The other plaintexts located in this folder are manual annotations, added to existing self-driving datasets to bring them up to the requirements of the CS7810 self-driving ontology 

* This 'extra' information, i.e. the info which we must add, mostly alings with everything modeled by the Lane, Road, and Intersection schemas.

* Plaintext indicates vehicles and pedestrians using instanceIds from Cityscapes, and traffic instruction indicators using their order of appearance in a given scenario, to tie these entities back to their representations in the original data

* The indentation structure of the plaintext indicates the collection relationships between Lanes, Roads, and Intersections

* Descriptions of Traffic Instruction Indicators are also added


## Data Loading ##

* All logic for reading data is currently found in materialization.py

* Object labels/positions/etc. are extracted from Cityscapes 3D, Cityscapes Persons, and the original Cityscapes semantic segmentation data, training split. Currently all information is extracted from JSON files. 

* There is unique information (namely depth information) in image files, but we have not extracted it yet, and it is pending available project time

* Wrangling BDD100K dataset is pending available project time 