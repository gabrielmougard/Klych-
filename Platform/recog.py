######################
#    Writter Plawn   #
######################


import face_recognition as f
import flask
import json
import time
import _pickle as pickle
import threading
import dlib
import face_recognition_models
import numpy as np
import mp_pool as mp

default_tolerance = 0.5


face_detector = dlib.get_frontal_face_detector()

predictor_68_point_model = face_recognition_models.pose_predictor_model_location()
pose_predictor_68_point = dlib.shape_predictor(predictor_68_point_model)

predictor_5_point_model = face_recognition_models.pose_predictor_five_point_model_location()
pose_predictor_5_point = dlib.shape_predictor(predictor_5_point_model)

cnn_face_detection_model = face_recognition_models.cnn_face_detector_model_location()
cnn_face_detector = dlib.cnn_face_detection_model_v1(cnn_face_detection_model)

face_recognition_model = face_recognition_models.face_recognition_model_location()
face_encoder = dlib.face_recognition_model_v1(face_recognition_model)


def _raw_face_locations(img, number_of_times_to_upsample=1, model="hog"):
    return cnn_face_detector(img, number_of_times_to_upsample) if model == 'cnn' else face_detector(img, number_of_times_to_upsample)


def _css_to_rect(css):
    return dlib.rectangle(css[3], css[0], css[1], css[2])


def _raw_face_landmarks(face_image, face_locations=None, model="large"):
    # if face_locations is None:
    #     face_locations = _raw_face_locations(face_image)
    # else:
    #     face_locations = [_css_to_rect(face_location)
    #                       for face_location in face_locations]
    face_locations = _raw_face_locations(face_image) if face_locations is None else [
        _css_to_rect(face_location) for face_location in face_locations]
    pose_predictor = pose_predictor_5_point if model == 'small' else pose_predictor_68_point
    return [pose_predictor(face_image, face_location) for face_location in face_locations]


def face_encodings(face_image, known_face_locations=None, num_jitters=1, model='small'):
    raw_landmarks = _raw_face_landmarks(
        face_image, known_face_locations, model=model)
    return [np.array(face_encoder.compute_face_descriptor(face_image, raw_landmark_set, num_jitters)) for raw_landmark_set in raw_landmarks]


def distances_faces(face_encodings, face_to_compare):
    return np.linalg.norm(face_encodings - face_to_compare, axis=1)


def timeit(func):
    def f(*args, **kwargs):
        t = time.time()
        res = func(*args, **kwargs)
        return res, time.time()-t
    return f


class NumpyEncoder(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, np.ndarray):
            return obj.tolist()
        return json.JSONEncoder.default(self, obj)



class face_db:
    def __init__(self, tolerance=default_tolerance, use_gpu=False):
        self.existing_faces = []
        self.existing_faces_d = {}
        self.next_id = 0
        self.nb_photos = 0
        self.tolerance = tolerance
        self.model1 = 'hog'
        self.model2 = 'small'
        self.pool = mp.Pool(processes=4)

        self.map_find = functools.partial(f.face_locations, model=self.model1)
        self.map_encode = functools.partial(f.face_encodings, model=self.model2)


        if use_gpu:
            self.model1 = 'cnn'
            self.model2 = 'large'

    @timeit
    def find_pictures(self, photo_file):
        
        img = f.load_image_file(photo_file)
        t = time.time()
        locations = self.pool.map_one(self.map_find, (img, ))
        # print('hey', locations)
        # locations = f.face_locations(img, model=self.model1)
        print('locations are', locations)
        face = face_encodings(img, locations, 1, self.model2)[0]
        print('time to encode is {} s'.format(time.time() - t))
        del locations
        del img
        result = distances_faces(self.existing_faces, face)
        del face
        i = np.argmin(result)
        if result[i] <= self.tolerance:
            del result
            return self.existing_faces_d[i]
        else:
            print('The face is not in the db')
            return []

    @timeit
    def add_new_picture(self, photo_filename):
        img = f.load_image_file(photo_filename)
        t = time.time()
        locations = f.face_locations(img, model=self.model1)
        faces = face_encodings(img, locations, 1, self.model2)
        print('time to encode is {} s'.format(time.time() - t))
        print('faces=', len(faces))
        result = map(lambda face: f.compare_faces(
            self.existing_faces, face, tolerance=self.tolerance), faces)
        new_faces = 0
        for res, face in zip(result, faces):
            try:
                # we found the face of someone alrady registered
                i = res.index(True)
                self.existing_faces_d[i].append(photo_filename)

            except:
                # the face doesn't exists yet
                self.existing_faces.append(face)
                self.existing_faces_d[self.next_id] = [photo_filename]
                self.next_id += 1
                new_faces += 1

        self.nb_photos += 1

        print('added {}'.format(new_faces))
        return new_faces

    def next_name(self):
        return self.nb_photos

    def dump(self, filename):
        with open(filename, 'wb') as f:
            pickle.dump(self, f)

    def proper_dump(self, filename):
        d = {}
        d['existing_faces'] = self.existing_faces
        d['existing_faces_d'] = self.existing_faces_d
        d['next_id'] = self.next_id
        d['nb_photos'] = self.nb_photos
        d['tolerance'] = self.tolerance

        with open(filename, 'w') as f:
            json.dump(d, f, cls=NumpyEncoder)

    def proper_load(self, filename):
        with open(filename, 'r') as f:
            content = json.load(f)

        self.nb_photos = content['nb_photos']
        self.tolerance = content['tolerance']
        self.next_id = content['next_id']
        self.existing_faces_d = {
            int(key): content['existing_faces_d'][key] for key in content['existing_faces_d']}
        self.existing_faces = [np.asarray(i)
                               for i in content['existing_faces']]
