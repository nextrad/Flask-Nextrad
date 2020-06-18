import os
import cv2
from base_camera import BaseCamera


class Camera0(BaseCamera):
    video_source = 1

    def __init__(self):
        if os.environ.get('OPENCV_CAMERA_SOURCE'):
            Camera0.set_video_source(int(os.environ['OPENCV_CAMERA_SOURCE']))
        super(Camera0, self).__init__()

    @staticmethod
    def set_video_source(source):
        Camera0.video_source = source

    @staticmethod
    def frames():
        camera = cv2.VideoCapture(Camera0.video_source)
        if not camera.isOpened():
            raise RuntimeError('Could not start camera.')

        while True:
            # read current frame
            _, img = camera.read()

            # encode as a jpeg image and return it
            yield cv2.imencode('.jpg', img)[1].tobytes()

class Camera1(BaseCamera):
    video_source = 1

    def __init__(self):
        if os.environ.get('OPENCV_CAMERA_SOURCE'):
            Camera1.set_video_source(int(os.environ['OPENCV_CAMERA_SOURCE']))
        super(Camera1, self).__init__()

    @staticmethod
    def set_video_source(source):
        Camera1.video_source = source

    @staticmethod
    def frames():
        camera = cv2.VideoCapture(Camera1.video_source)
        if not camera.isOpened():
            raise RuntimeError('Could not start camera.')

        while True:
            # read current frame
            _, img = camera.read()

            # encode as a jpeg image and return it
            yield cv2.imencode('.jpg', img)[1].tobytes()

class Camera2(BaseCamera):
    video_source = 1

    def __init__(self):
        if os.environ.get('OPENCV_CAMERA_SOURCE'):
            Camera2.set_video_source(int(os.environ['OPENCV_CAMERA_SOURCE']))
        super(Camera2, self).__init__()

    @staticmethod
    def set_video_source(source):
        Camera2.video_source = source

    @staticmethod
    def frames():
        camera = cv2.VideoCapture(Camera2.video_source)
        if not camera.isOpened():
            raise RuntimeError('Could not start camera.')

        while True:
            # read current frame
            _, img = camera.read()

            # encode as a jpeg image and return it
            yield cv2.imencode('.jpg', img)[1].tobytes()

