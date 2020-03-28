# Credits: https://github.com/log0/video_streaming_with_flask_example
# https://github.com/informramiz/Face-Detection-OpenCV

import cv2


class VideoCamera(object):
    def __init__(self):
        self.video = cv2.VideoCapture(0)
        self.lbp_face_cascade = cv2.CascadeClassifier(
            'data/lbpcascade_frontalface.xml')

    def __del__(self):
        self.video.release()

    def get_frame(self):
        success, image = self.video.read()

        # Do stuff
        image = self.detect_faces(image)

        ret, jpeg = cv2.imencode('.jpg', image)
        return jpeg.tobytes()

    def detect_faces(self, colored_img):
        img_copy = colored_img.copy()
        gray = cv2.cvtColor(img_copy, cv2.COLOR_BGR2GRAY)
        faces = self.lbp_face_cascade.detectMultiScale(gray,
                                                       scaleFactor=1.1,
                                                       minNeighbors=5)

        for (x, y, w, h) in faces:
            cv2.rectangle(img_copy, (x, y), (x+w, y+h), (255, 191, 0), 2)

        return img_copy
