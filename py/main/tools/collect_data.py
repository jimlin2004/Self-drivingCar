import threading
import cv2
import numpy as np
import pickle
import struct
from Client import Client
from LaneFinding import LaneFinding
from joystick import Joystick

class Collect_data(object):
    def __init__(self):
        self.run = True
        self.cap = cv2.VideoCapture(0)
        self.client = Client("127.0.0.1", 8000)
        self.laneFinding = LaneFinding(0)
        self.joystick = Joystick(0)
        self.tread_joystick = threading.Thread(target=self.listen_key, name="Joystick_thread")
        self.tread_Socket = threading.Thread(target=self.sent_data, name="Socket_thread")
    def listen_key(self):
        while (self.run):
            self.joystick.listen()
    def frame_to_data(self, frame: np.ndarray):
        encode_param = [int(cv2.IMWRITE_JPEG_QUALITY), 90]
        frame = cv2.resize(frame, (320, 320))
        result, img_encode = cv2.imencode(".jpg", frame, encode_param)
        return img_encode
    def sent_data(self):
        data = dict()
        while (self.cap.isOpened()):
            ret, frame = self.cap.read()
            if (self.run):
                frame = self.laneFinding.transform_img(frame)
                cv2.imshow("client", frame)
                cv2.waitKey(1)
                img_data = self.frame_to_data(frame)
                data.update({"image": img_data})
                data.update({"command": self.joystick.event.command})
                if (self.joystick.event.command == 3 or self.joystick.event.command == 4):
                    data.update({"speed": 100})
                else:
                    data.update({"speed": self.joystick.event.speed})
                if (self.joystick.event.command == 3 or self.joystick.event.command == 4):
                    data.update({"turn": self.joystick.event.turn})
                else:
                    data.update({"turn": 0})
                pickle_data = pickle.dumps(data)
                size = len(pickle_data)
                self.run = self.client.sent_data(pickle_data, size)
            else:
                self.cap.release()
    def start(self):
        self.tread_joystick.setDaemon(True)
        self.tread_Socket.setDaemon(True)
        self.tread_joystick.start()
        self.tread_Socket.start()
    def stop(self):
        self.tread_Socket.join()
        self.tread_joystick.join()
if __name__ == "__main__":
    collect_data = Collect_data()
    collect_data.start()
    collect_data.stop()
