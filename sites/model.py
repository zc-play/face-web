# coding: utf-8
import os
import base64
import json

from sqlalchemy import Column, String, INTEGER, SmallInteger
from cli import db
from rpc.face_rec_client import face_rec_rpc


class Face(db.Model):

    id = Column(INTEGER(), primary_key=True, autoincrement=True)
    name = Column(String(256))
    path = Column(String(1024))
    is_train = Column(SmallInteger)
    encoding = Column(String(2048))
    dataset = Column(String(256))

    def __init__(self, name, path, is_train=False):
        self.name = name
        self.path = path
        self.is_train = is_train
        self.data = None
        self.rec_info = None

    def save(self):
        db.session.add(self)
        db.session.commit()

    def get_org_data(self):
        if not os.path.exists(self.path):
            self.data = '该图像缺失'
            return
        with open(self.path, 'rb') as f:
            img = f.read()
        img_b64 = base64.b64encode(img)
        self.data = 'data:image/gif;base64,%s' % str(img_b64, 'utf-8')

    def get_rec_data(self, method, dataset='lfw'):
        res = face_rec_rpc(self.id, method, dataset)
        self.data = res.get('stream')
        self.rec_info = json.loads(res.get('rec_info'))
        print(self.rec_info)

    def record_train(self):
        self.is_train = True
        self.save()


