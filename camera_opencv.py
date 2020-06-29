import os
import cv2
import imutils
from base_camera import BaseCamera, BaseCamera1, BaseCamera2

# import mrcnn.config
# import mrcnn.utils
# from mrcnn.model import MaskRCNN
# from pathlib import Path

face_cascade=cv2.CascadeClassifier(cv2.data.haarcascades + "haarcascade_frontalface_default.xml")
ds_factor=0.6
min_area = 300
move_thresh = 50



def cv_conversion(img, face=0, bg_sub=1, firstFrame=None, deep_boat=0):
    if face==1:

        img=cv2.resize(img,None,fx=ds_factor,fy=ds_factor,interpolation=cv2.INTER_AREA)
        gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        face_rects=face_cascade.detectMultiScale(gray,1.2,5)
        for (x,y,w,h) in face_rects:
            cv2.rectangle(img,(x,y),(x+w,y+h),(0,255,0),2)
            break
        return img

    if bg_sub==1:
        # frame = imutils.resize(img, width=500)
        gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        gray = cv2.GaussianBlur(gray, (21, 21), 0)

        if firstFrame is None:
            firstFrame = gray

        # compute the absolute difference between the current frame and
        # first frame
        frameDelta = cv2.absdiff(firstFrame, gray)
        thresh = cv2.threshold(frameDelta, move_thresh, 255, cv2.THRESH_BINARY)[1]
        # dilate the thresholded image to fill in holes, then find contours
        # on thresholded image
        thresh = cv2.dilate(thresh, None, iterations=2)
        cnts = cv2.findContours(thresh.copy(), cv2.RETR_EXTERNAL,
            cv2.CHAIN_APPROX_SIMPLE)
        cnts = imutils.grab_contours(cnts)
        # loop over the contours
        for c in cnts:
            # if the contour is too small, ignore it
            if cv2.contourArea(c) < min_area:
                continue
            # compute the bounding box for the contour, draw it on the frame,
            # and update the text
            (x, y, w, h) = cv2.boundingRect(c)
            cv2.rectangle(img, (x, y), (x + w, y + h), (0, 255, 0), 2)

        return img, firstFrame

    if deep_boat==1:

        return img, firstFrame

class Camera(BaseCamera):
    video_source = 0
    def __init__(self):
        # if os.environ.get('OPENCV_CAMERA_SOURCE'):
        #     Camera.set_video_source(int(os.environ['OPENCV_CAMERA_SOURCE']))
        super(Camera, self).__init__()

    @staticmethod
    def set_video_source(source):
        Camera.video_source = source

    @staticmethod
    def frames():
        firstFrame = None
        camera = cv2.VideoCapture(Camera.video_source)
        if not camera.isOpened():
            raise RuntimeError('Could not start camera.')
        while True:
            # read current frame
            _, img = camera.read()
            img, firstFrame = cv_conversion(img, bg_sub=1, firstFrame=firstFrame)
            # encode as a jpeg image and return it
            yield cv2.imencode('.jpg', img)[1].tobytes()

class Camera1(BaseCamera1):
    video_source = 1

    def __init__(self):
        # if os.environ.get('OPENCV_CAMERA_SOURCE'):
        #     Camera.set_video_source(int(os.environ['OPENCV_CAMERA_SOURCE']))
        super(Camera1, self).__init__()

    @staticmethod
    def set_video_source(source):
        Camera1.video_source = source

    @staticmethod
    def frames():
        firstFrame = None
        camera = cv2.VideoCapture(Camera1.video_source)
        if not camera.isOpened():
            raise RuntimeError('Could not start camera.')
        while True:
            # read current frame
            _, img = camera.read()
            img, firstFrame = cv_conversion(img, bg_sub=1, firstFrame=firstFrame)
            # encode as a jpeg image and return it
            yield cv2.imencode('.jpg', img)[1].tobytes()

class Camera2(BaseCamera2):
    video_source = 2
    def __init__(self):
        # if os.environ.get('OPENCV_CAMERA_SOURCE'):
        #     Camera.set_video_source(int(os.environ['OPENCV_CAMERA_SOURCE']))
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
            img = cv_conversion(img)
            # encode as a jpeg image and return it
            yield cv2.imencode('.jpg', img)[1].tobytes()
