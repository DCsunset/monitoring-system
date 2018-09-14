import cv2

class Video:
    def __init__(self, rstp_options=None):
        if not rstp_options:
            # Using system camera
            self.video = cv2.VideoCapture(0)
        else:
            pass

    def __del__(self):
        self.video.release()

    def get_frame(self):
        success, image = self.video.read()
        # Use MJPEG
        ret, jpeg = cv2.imencode('.jpg', image)
        return jpeg.tobytes()

