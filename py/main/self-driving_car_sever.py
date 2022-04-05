from tools.Decision_maker import Decision_maker
from tools.LaneFinding import LaneFinding
from tools.CNN.tools.model_module import Prediction
from tools.joystick import Virtual_joystick
from tools.yolo_Module import Yolo_module
import threading
import cv2
import numpy as np
import struct
import pickle
import socket

class Self_driving_car(object):
    def __init__(self, host: str, port: int, is_show: bool) -> None:
        self.is_show = is_show
        print("[INFO] start loading...")
        self.Decision_maker = Decision_maker("tools/CNN/model_keras_2022_03_27_SGD_balance")
        print("[INFO] tensorflow model loaded finished")
        self.Yolo_module = Yolo_module("tools/cfg/self-driving-car.names", "tools/cfg/yolov4-tiny.cfg", "tools/weight/yolov4-tiny_final.weights")
        print("[INFO] yolo model loaded finished")
        self.cap = cv2.VideoCapture(0)
        self.LaneFinding = LaneFinding(0)
        self.virtual_joystick = Virtual_joystick()
        # self.command_dict = {
        #     0: "stop",
        #     1: "forward",
        #     2: "back",
        #     3: "turn_right",
        #     4: "turn_left"
        # }
        self.command_dict = {
            0: "forward",
            1: "turn_right", 
            2: "turn_left"
        }
        self.speed_dict = {
            40: "set_speed_40",
            60: "set_speed_60",
            100: "set_speed_100"
        }
        self.turn_dict = {
            0: "set_outside_turn",
            1: "set_outside_turn",
            2: "set_outside_turn"
        }
        self.run = True
        self.is_stop = False
        self.server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.server.bind((host, port))
        self.server.listen(5)
        print("[INFO] Listening on {}:{}".format(host, port))
        self.conn, self.addr = self.server.accept()
        print("[INFO] Connected by {}".format(self.addr))
        self.thread_self_driving = threading.Thread(target=self.start_self_driving, name="Thread_self_driving")
    
    def __predict(self, img: np.ndarray, speed: int) -> Prediction:
        return self.Decision_maker.predict(img, speed)
    
    def __sent_data(self, prediction: Prediction, is_stop: bool) -> list: 
        #sent command to Arduino
        if (not is_stop):
            print(self.command_dict[prediction.command])
            # print(self.turn_dict[prediction.turn])
            print(self.speed_dict[self.virtual_joystick.event.speed])
            data = dict()
            data.update({"command": self.command_dict[prediction.command]})
            data.update({"turn": self.turn_dict[0]})
            data.update({"speed": self.virtual_joystick.event.speed})
            pickle_data = pickle.dumps(data)
            size = len(pickle_data)
            self.conn.sendall(struct.pack("Q", size) + pickle_data)
        else:
            data = dict()
            data.update({"command": "stop"})
            data.update({"turn": self.turn_dict[0]})
            data.update({"speed": self.virtual_joystick.event.speed})
            pickle_data = pickle.dumps(data)
            size = len(pickle_data)
            self.conn.sendall(struct.pack("Q", size) + pickle_data)

    def __recv_data(self)->np.ndarray:
        # conn, addr = self.server.accept()
        # print("\033[1;32;1m [INFO] Connected by {} \033[0m\n".format(addr))
        data = b""
        payload_size = struct.calcsize("Q")
        while (len(data) < payload_size):
            data += self.conn.recv(4096)
        packed_msg_size = data[:payload_size]
        data = data[payload_size:]
        msg_size = struct.unpack("Q", packed_msg_size)[0]
        while (len(data) < msg_size):
            data += self.conn.recv(4096)
        pickle_data = data[:msg_size]
        data = data[msg_size:]
        pickle_data = pickle.loads(pickle_data)
        frame = cv2.imdecode(pickle_data["image"], cv2.IMREAD_COLOR)
        return frame

    def start_self_driving(self):
        while (self.run):
            frame = self.__recv_data()
            prediction_yolo = self.Yolo_module.predict(frame)
            self.virtual_joystick.event.speed, self.is_stop = self.Yolo_module.reset_parameter(frame, prediction_yolo, self.virtual_joystick.event.speed, self.is_stop)
            prediction =  self.__predict(frame, self.virtual_joystick.event.speed)
            # print(prediction.command, prediction.turn)
            # cv2.putText(frame, "Command: {} Turn: {}".format(prediction.command, prediction.turn), (10, 60), cv2.FONT_HERSHEY_SIMPLEX, 1, (154, 24, 90), 2)
            if (self.is_show):
                cv2.imshow("cap", frame)
                if cv2.waitKey(1) == ord('q'):
                    cv2.destroyWindow("cap")
                    self.run = False
            if (not self.is_stop):
                self.__sent_data(prediction, False)
            else:
                self.__sent_data(prediction, True)

    def start(self):
        self.thread_self_driving.setDaemon(True)
        self.thread_self_driving.start()

    def stop(self):
        self.thread_self_driving.join()

if __name__ == "__main__":
    self_driving_car = Self_driving_car("192.168.168.11", 8000, True)
    self_driving_car.start()
    self_driving_car.stop()