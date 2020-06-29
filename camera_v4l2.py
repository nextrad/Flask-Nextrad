import io
from PIL import Image
import select
import v4l2capture
from base_camera import BaseCamera


class Camera(BaseCamera):
    """Requires python-v4l2capture module: https://github.com/gebart/python-v4l2capture"""

    video_source = '/dev/video0'

    @staticmethod
    def frames():
        try:
            video = v4l2capture.Video_device(Camera.video_source)
            # Suggest an image size. The device may choose and return another if unsupported
            size_x = 640
            size_y = 480
            size_x, size_y = video.set_format(size_x, size_y)
            video.create_buffers(1)
            video.queue_all_buffers()
            video.start()
            bio = io.BytesIO()

            try:
                while True:
                    select.select((video,), (), ())  # Wait for the device to fill the buffer.
                    image_data = video.read_and_queue()
                    image = Image.frombytes("RGB", (size_x, size_y), image_data)
                    image.save(bio, format="jpeg")
                    yield bio.getvalue()
                    bio.seek(0)
                    bio.truncate()
            finally:
                video.close()

        except:
            print('Cannot access device:',Camera.video_source)


    @staticmethod
    def set_video_source(source):
        Camera.video_source = source

class Camera1(BaseCamera):
    """Requires python-v4l2capture module: https://github.com/gebart/python-v4l2capture"""

    video_source_1 = '/dev/video1'

    @staticmethod
    def frames():
        try:
            video_1 = v4l2capture.Video_device(Camera1.video_source_1)
            # Suggest an image size. The device may choose and return another if unsupported
            size_x = 640
            size_y = 480
            size_x, size_y = video_1.set_format(size_x, size_y)
            video_1.create_buffers(1)
            video_1.queue_all_buffers()
            video_1.start()
            bio = io.BytesIO()

            try:
                while True:
                    select.select((video_1,), (), ())  # Wait for the device to fill the buffer.
                    image_data = video_1.read_and_queue()
                    image = Image.frombytes("RGB", (size_x, size_y), image_data)
                    image.save(bio, format="jpeg")
                    yield bio.getvalue()
                    bio.seek(0)
                    bio.truncate()
            finally:
                video_1.close()
        except:
            print('Cannot access device:',Camera1.video_source_1)

    @staticmethod
    def set_video_source_1(source):
        Camera1.video_source_1 = source



