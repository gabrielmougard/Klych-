import json
import os
import time

t = time.time()
with open('face_db.json', 'r') as f :
    content = json.load(f)

hashes = set()
# existing_faces_d

for filename in map(lambda x : 'photos/'+x, os.listdir('photos')):
    print(filename)
    with open(filename, 'rb') as f :
        c = f.read()
        if c not in hashes:
            hashes.add(c)

for key in content['existing_faces_d']:
    print(key)
    content['existing_faces_d'][key] = list(filter(lambda x : x in hashes, content['existing_faces_d'][key]))
    
with open('face_db.json', 'w') as f :
    json.dump(content, f, indent=4)

print('done')
print('took {} s'.format(time.time() - t))