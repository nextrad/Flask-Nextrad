import os
import cv2
import imutils
import time
# from base_camera import BaseCamera
import threading
try:
    from greenlet import getcurrent as get_ident
except ImportError:
    try:
        from thread import get_ident
    except ImportError:
        from _thread import get_ident

# import mrcnn.config
# import mrcnn.utils
# from mrcnn.model import MaskRCNN
# from pathlib import Path

face_cascade=cv2.CascadeClassifier(cv2.data.haarcascades + "haarcascade_frontalface_default.xml")
ds_factor=0.6
min_area = 300
move_thresh = 50



def cv_conversion(img, face=0, bg_sub=1, firstFrame=None, deep_boat=0):
    '''Not a pretty way of adding opencv conversions to the vid streams'''
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

class CameraEvent():
    """An Event-like class that signals all active clients when a new frame is
    available.
    """
    def __init__(self):
        self.events = {}

    def wait(self):
        """Invoked from each client's thread to wait for the next frame."""
        ident = get_ident()
        if ident not in self.events:
            # this is a new client
            # add an entry for it in the self.events dict
            # each entry has two elements, a threading.Event() and a timestamp
            self.events[ident] = [threading.Event(), time.time()]
        return self.events[ident][0].wait()

    def set(self):
        """Invoked by the camera thread when a new frame is available."""
        now = time.time()
        remove = None
        for ident, event in self.events.items():
            if not event[0].isSet():
                # if this client's event is not set, then set it
                # also update the last set timestamp to now
                event[0].set()
                event[1] = now
            else:
                # if the client's event is already set, it means the client
                # did not process a previous frame
                # if the event stays set for more than 5 seconds, then assume
                # the client is gone and remove it
                if now - event[1] > 5:
                    remove = ident
        if remove:
            del self.events[remove]

    def clear(self):
        """Invoked from each client's thread after a frame was processed."""
        self.events[get_ident()][0].clear()



class Camera():
    def __init__(self, name, video_source):
        self.name = name
        self.video_source = video_source
        self.camera_found = 0
        self.firstFrame = None
        self.cv_on = 0

        self.thread = None  # background thread that reads frames from camera
        self.frame = None  # current frame is stored here by background thread
        self.last_access = 0  # time of last client access to the camera
        self.event = CameraEvent()
        self.thread_close = 0

        # if os.environ.get('OPENCV_CAMERA_SOURCE'):
        #     Camera.set_video_source(int(os.environ['OPENCV_CAMERA_SOURCE']))
        # self.start_thread()

    def start_thread(self):
        if os.path.exists(self.video_source):
            if self.thread is None:
                self.last_access = time.time()

                # start background frame thread
                self.thread = threading.Thread(target=self._thread)
                self.thread.start()

                # wait until frames are available
                while self.get_frame() is None:
                    time.sleep(0)
        else:
            print(f'Please Check Video Source Directory for {self.name}')

    def set_video_source(self,source):
        self.video_source = source

    def get_frame(self):
        """Return the current camera frame."""
        self.last_access = time.time()

        # wait for a signal from the camera thread
        self.event.wait()
        self.event.clear()

        return self.frame

    def frames(self):
        camera = cv2.VideoCapture(self.video_source)
        if not camera.isOpened():
            raise RuntimeError(f'Could not start camera {self.name}')

        while True:
            self.camera_found=1
            # read current frame
            try:
                _, img = camera.read()
                if self.cv_on:
                    img, self.firstFrame = cv_conversion(img, bg_sub=1, firstFrame=self.firstFrame)
                # encode as a jpeg image and return it
                yield cv2.imencode('.jpg', img)[1].tobytes()
            except:
                self.thread_close = 1
                print(f'Failed to read {self.name} stream. Please ensure stream is active.')
                self.camera_found = 0
                break

    def _thread(self):
        """Camera background thread."""
        print(f'Starting camera thread for {self.name}')
        frames_iterator = self.frames()
        for frame in frames_iterator:
            self.frame = frame
            self.event.set()  # send signal to clients
            time.sleep(0)

            # if there hasn't been any clients asking for frames in
            # the last 10 seconds then stop the thread
            if time.time() - self.last_access > 10:
                frames_iterator.close()
                print(f'Stopping {self.name} thread due to inactivity.')
                break
            if self.thread_close:
                frames_iterator.close()
                break
        self.thread = None


# class Camera(BaseCamera):
#     def __init__(self, name, video_source):
#         self.name = name
#         self.video_source = video_source
#         self.camera_found = 0
#         self.firstFrame = None
#         # if os.environ.get('OPENCV_CAMERA_SOURCE'):
#         #     Camera.set_video_source(int(os.environ['OPENCV_CAMERA_SOURCE']))
#         if os.path.exists(self.video_source):
#             super(Camera, self).__init__()
#         else:
#             print(f'Please Check Video Source Directory for {self.name}')

#     def set_video_source(self,source):
#         self.video_source = source

#     def frames(self):
#         camera = cv2.VideoCapture(self.video_source)
#         if not camera.isOpened():
#             raise RuntimeError(f'Could not start camera {self.name}')

#         while True:
#             self.camera_found=1
#             # read current frame
#             _, img = camera.read()
#             img, self.firstFrame = cv_conversion(img, bg_sub=1, firstFrame=self.firstFrame)
#             # encode as a jpeg image and return it
#             yield cv2.imencode('.jpg', img)[1].tobytes()
