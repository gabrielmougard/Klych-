# Face recogntion part

Based on the face_recognition python library and on flask
The db, when loaded stays in memory.

# Python HTTP endpoint to access a db
4 points :

* upload -> requires file, password | POST
* find   -> requires file, password | POST
* dump   -> requires password       | POST
* how_many_faces ->                 | GET
* how_many_photos ->                | GET

The db is saved as a pickled python object (easier for now)