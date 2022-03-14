import threading
import cv2
import numpy as np
from LaneFinding import LaneFinding
from joystick import Joystick

class Test(object):
    def __init__(self):
        self.run = True
        self.cap = cv2.VideoCapture(0)
        # self.client = Client("127.0.0.1", 8000)
        self.laneFinding = LaneFinding(0)
        self.joystick = Joystick(0)
        self.tread_joystick = threading.Thread(target=self.listen_key, name="Joystick_thread")
        self.tread_cap = threading.Thread(target=self.show_cap, name="Socket_thread")
    def listen_key(self):
        while (self.run):
            self.joystick.listen()
    def show_cap(self):
        while (self.cap.isOpened()):
            ret, frame = self.cap.read()
            cv2.imshow("cap", frame)
            cv2.waitKey(1)

    def start(self):
        self.tread_joystick.setDaemon(True)
        self.tread_cap.setDaemon(True)
        self.tread_joystick.start()
        self.tread_cap.start()
    def stop(self):
        self.tread_cap.join()
        self.tread_joystick.join()
if __name__ == "__main__":
    test = Test()
    test.start()
    test.stop()
