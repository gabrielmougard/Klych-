# Face recogntion part

Based on the face_recognition python library and on flask
The db, when loaded stays in memory.

# Python HTTP endpoint to access a db

* upload -> requires file, password | POST optional big_file : boolean => avoid resolution reduction for big photos
* find   -> requires file, password | POST
* dump   -> requires password       | POST
* how_many_faces ->                 | GET
* how_many_photos ->                | GET


# todo

* repair db (add photo hashes)
* remove photo dupes