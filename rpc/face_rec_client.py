# coding: utf-8
import base64
import json
from io import BytesIO

import grpc
from PIL import Image
from rpc.face_rec_pb2_grpc import FaceRecognitionStub

from rpc.face_rec_pb2 import MyStr

channel = grpc.insecure_channel('localhost:50051')
stub = FaceRecognitionStub(channel)


def face_rec_rpc(face_id, method='dlib', dataset='lfw', is_return=True, is_save=False, save_path='test.png'):
    """
    rpc client, send a request of face recognition to rpc server
    :param face_id: str,
    :param is_return: return base64 of the recognition face
    :param method: dlib or facenet
    :param is_save: the flag if save image
    :param save_path: save path
    :return:
    """
    req_data = json.dumps(dict(face_id=face_id, method=method, dataset=dataset))
    response = stub.face_rec_str(MyStr(name=req_data))
    if is_return:
        return dict(stream='data:image/gif;base64,%s' % response.stream, rec_info=response.name)

    if is_save:
        img_bytes = base64.b64decode(response.stream)
        img_fp = BytesIO(img_bytes)
        img = Image.open(img_fp)
        img.save(save_path)


if __name__ == '__main__':
    print(face_rec_rpc(dict(face_id=1), method='dlib'))
