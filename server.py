import recog
import img_handler
import os
import time
import uuid
import subprocess
import sys
import json
import Fancy_term as term
from flask import Flask, flash, request, redirect, url_for, jsonify
import mp_pool

pool = mp_pool.Pool(6)
print_info = term.Smart_print(style=term.Style(
    color=term.colors.yellow, substyle=["bold"]))
print_error = term.Smart_print(style=term.Style(
    color=term.colors.red, substyle=["bold"]))
# settings

max_size = 480

with open('conf.json', 'r') as f:
    cfg = json.load(f)
password_server = cfg['base_password']
img_server_port = cfg['img_serv_port']
flask_port = cfg['flask_port']
UPLOAD_FOLDER = cfg['upload_folder']
use_gpu = cfg['use_gpu']
tolerance = cfg['tolerance']
using_resize = cfg['using_resize']
nb_worker = cfg['workers']

if use_gpu:
    print_info('Using GPU')


# launching the go server to handle image serv
print_info('starting img server on port {}'.format(img_server_port))
pid = subprocess.Popen(
    [
        "go",
        "run",
        "serv_imgs.go",
        str(img_server_port),
        str(UPLOAD_FOLDER)
    ],
    shell=False
).pid
print_info('Go server PID is {}'.format(pid))


# handling db_loading
db = None
db_filename = cfg['db_filename']

if len(sys.argv) >= 2:
    if sys.argv[1] == 'load':
        db = recog.face_db(nb_worker=nb_worker)
        db.proper_load(db_filename)
        db.tolerance = tolerance
        print('loaded {} faces'.format(len(db.existing_faces)))
        print('db contains {}'.format(db.nb_photos))
    else:
        db = recog.face_db(tolerance, use_gpu=use_gpu)
else:
    db = recog.face_db(tolerance, use_gpu=use_gpu)

db.tolerance = tolerance
print_info('tolerance set to {}'.format(db.tolerance))
# creating flask app here
app = Flask(__name__)

# small decorators
# decorating to avoid flask issues


def wrap_decorator(deco):
    def f(func):
        fu = deco(func)
        fu.__name__ = func.__name__
        return fu
    return f


@wrap_decorator
def needs_password(func):
    return lambda *args: func(*args) if request.form['password'] == password_server else 'Invalid password'


@wrap_decorator
def check_has_file(func):
    def fe(*args):
        if 'file' not in request.files:
            return 'file is missing'
        if request.files['file'].filename == '':
            return 'file is missing'
        return func(*args)
    return fe


def make_id():
    return str(uuid.uuid4())


@app.route('/upload', methods=['POST'])
@needs_password
@check_has_file
def upload():
    file = request.files['file']
    big_file = False
    if 'big_file' in request.form and request.form['big_file']:
        big_file = True
    filename = file.filename

    _id = make_id()
    path = os.path.join(UPLOAD_FOLDER, '{}.jpg'.format(_id))
    print('saving at path {}'.format(path))
    file.save(path)
    temp_filename = os.path.join('temp', '{}.jpg'.format(_id))
    if not big_file:
        pool.map_one(img_handler.resize_image, (path, max_size, temp_filename))
    added, added_to_profile, took = db.add_new_picture(path, temp_filename)

    # file already exists
    if added == -1:
        os.remove(path)
    # always removing tempfile
    os.remove(temp_filename)

    return jsonify({
        'added': added,
        'added_to_profile': added_to_profile,
        'took': took,
    })


@app.route('/ch_tolerance', methods=['POST'])
@needs_password
def change_tolerance():
    old = db.tolerance
    db.tolerance = float(request.form['tolerance'])
    return jsonify({
        'old': old,
        'new': db.tolerance
    })


@app.route('/how_many_faces', methods=['GET'])
def how_many_faces():
    return jsonify({
        'nb_faces': len(db.existing_faces)
    })


@app.route('/how_many_photos', methods=['GET'])
def how_many_photos():
    return jsonify({
        'nb_photos': db.nb_photos
    })


@app.route('/find', methods=['POST'])
@check_has_file
def find():
    file = request.files['file']
    filename = make_id() + '.jpg'
    path = os.path.join('temp', filename)
    file.save(path)
    # auto-resize part
    if using_resize:
        try:
            img_handler.resize_image(path, max_size)
        except Exception as e:
            print(e)

    # actual finding part
    found, took = [], 0
    try:
        found, took = db.find_pictures(path)
    except Exception as e:
        print_error(e.__str__())
        print("could'nt any find face")
        return jsonify({'error': "can't find face", 'found': found})

    # trying to remove the temp file
    # try:
    #     os.remove(path)
    # except:
    #     print_error('error removing temp file')

    print('took {} s to find {} pictures'.format(took, len(found)))

    return jsonify({
        'found': found,
        'took': took
    })


@app.route('/dump', methods=['POST'])
@needs_password
def dump_db():
    db.proper_dump(db_filename)
    return 'just dumped the db'


def make_bool(string: str):
    return string.lower() == 'true'


@app.route('/set_resize', methods=['POST'])
@needs_password
def set_resize():
    global using_resize
    using_resize = make_bool(request.form['using_resize'])
    return jsonify({
        'using_resize': using_resize
    })


app.run(port=flask_port)
