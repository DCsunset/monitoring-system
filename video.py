import cv2

class Video:
    def __init__(self, rstp_options=None):
        if not rstp_options:
            # Using system camera
            self.video = cv2.VideoCapture(0)
        else:
            string = "http://" + \
                    rstp_options['username'] + ":" + \
                    rstp_options['password'] + "@" + \
                    rstp_options['ip'] + ":" + \
                    rstp_options['port']
            self.video = cv2.VideoCapture(string)

        #self.video.set(cv2.CAP_PROP_FRAME_WIDTH, 640)

    def __del__(self):
        self.video.release()

    def get_frame(self):
        success, frame = self.video.read()
        return frame

    @staticmethod
    def encode_frame(frame):
        # Use MJPEG
        ret, jpeg = cv2.imencode('.jpg', frame)
        return jpeg.tobytes()

