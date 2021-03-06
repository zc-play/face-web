# coding: utf-8
from flask import request, redirect, render_template

from cli import app, db
from sites.model import Face
from sqlalchemy import func

# You can change this to any folder on your system
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif'}


def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


origin_face = []
dataset = 'vgg'


@app.route('/', methods=['GET', 'POST'])
def home():
    global origin_face, dataset

    # Check if a valid image file was uploaded
    rec_face = None
    # 选未训练的4个
    is_flush = request.args.get('is_flush')
    data_set = request.args.get('dataset')
    if data_set:
        dataset = data_set

    print('.......................{}'.format(dataset))

    if request.method == 'POST':
        face_id = request.form.get('id')
        method = request.form.get('method')
        # method = 'dlib'
        if face_id:
            rec_face = Face.query.filter_by(id=face_id).first()
            try:
                rec_face.get_rec_data(method=method, dataset=dataset)
            except:
                pass

    print('is_flush: ', is_flush)
    if is_flush == '1':
        origin_face = []

    if not origin_face:
        faces = db.session.query(Face).\
            filter(Face.is_train == 0, Face.dataset == dataset).\
            order_by(func.rand()).limit(4).all()
        for face in faces:
            face.get_org_data()
            origin_face.append(face)

    return render_template('index.html', origin_face=origin_face, rec_face=rec_face)


@app.route('/desc')
def sys_desc():
    return render_template('desc.html')

