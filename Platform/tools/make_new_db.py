import recog
import _pickle as pickle


with open('face_db.db', 'rb') as f :
    db = pickle.load(f)


new_db = recog.face_db(0.5, True)

new_db.nb_photos = db.nb_photos
new_db.next_id = db.next_id
new_db.existing_faces = db.existing_faces
new_db.existing_faces_d = db.existing_faces_d


new_db.proper_dump('better_db.json')