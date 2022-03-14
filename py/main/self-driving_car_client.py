import pickle
import struct
from tools.LaneFinding import LaneFinding
from tools.joystick import Virtual_joystick
import threading
import cv2
import numpy as np
import socket

class Self_driving_car(object):
    def __init__(self, is_show: bool) -> None:
        self.cap = cv2.VideoCapture(0)
        self.LaneFinding = LaneFinding(0)
        self.virtual_joystick = Virtual_joystick()
        self.run = True
        self.is_stop = False
        self.client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.client.connect(("192.168.168.20", 8000))
        self.thread_self_driving = threading.Thread(target=self.start_self_driving, name="Thread_self_driving")
    
    def __sent_command(self, command, turn, speed) -> None:
        #sent command to Arduino
        self.virtual_joystick.listen(speed)
        self.virtual_joystick.listen(command)
        self.virtual_joystick.listen(turn)

    def __recv_data(self):
        data = b""
        payload_size = struct.calcsize("Q")
        while (1):
            while (len(data) < payload_size):
                data += self.client.recv(4096)
            packed_msg_size = data[:payload_size]
            data = data[payload_size:]
            msg_size = struct.unpack("Q", packed_msg_size)[0]
            while (len(data) < msg_size):
                data += self.client.recv(4096)
            pickle_data = data[:msg_size]
            data = data[msg_size:]
            pickle_data = pickle.loads(pickle_data)
            return [pickle_data["command"], pickle_data["turn"], pickle_data["speed"]]

    def __frame_to_data(self, frame: np.ndarray):
        encode_param = [int(cv2.IMWRITE_JPEG_QUALITY), 90]
        frame = cv2.resize(frame, (320, 320))
        result, img_encode = cv2.imencode(".jpg", frame, encode_param)
        return img_encode

    def start_self_driving(self):
        while (self.run):
            ret, frame = self.cap.read()
            data = self.__frame_to_data(frame)
            pickle_data = pickle.dumps({"image": data})
            size = len(pickle_data)
            self.client.sendall(struct.pack("Q", size) + pickle_data)
            command, turn, speed = self.__recv_data()
            self.__sent_command(command, turn, speed)

    def start(self):
        self.thread_self_driving.setDaemon(True)
        self.thread_self_driving.start()

    def stop(self):
        self.thread_self_driving.join()

if __name__ == "__main__":
    self_driving_car = Self_driving_car(True)
    self_driving_car.start()
    self_driving_car.stop()