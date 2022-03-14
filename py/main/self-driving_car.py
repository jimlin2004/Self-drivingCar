from tools.Decision_maker import Decision_maker
from tools.LaneFinding import LaneFinding
from tools.CNN.tools.model_module import Prediction
from tools.joystick import Virtual_joystick
from tools.yolo_Module import Yolo_module
import threading
import cv2
import numpy as np
import colorama

class Self_driving_car(object):
    def __init__(self, is_show: bool) -> None:
        self.is_show = is_show
        print(colorama.Fore.GREEN + "[INFO] start loading...")
        self.Decision_maker = Decision_maker("tools/CNN/model_keras_speed100")
        print(colorama.Fore.GREEN + "[INFO] tensorflow model loaded finished")
        self.Yolo_module = Yolo_module("tools/cfg/self-driving-car.names", "tools/cfg/yolo-fastest-1.1.cfg", "tools/weight/yolo-fastest-1_last.weights")
        print(colorama.Fore.GREEN + "[INFO] yolo model loaded finished")
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
            2: "turn_right", 
            1: "turn_left"
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
        self.thread_self_driving = threading.Thread(target=self.start_self_driving, name="Thread_self_driving")
    
    def __predict(self, img: np.ndarray, speed: int) -> Prediction:
        return self.Decision_maker.predict(img, speed)
    
    def __sent_command(self, prediction: Prediction) -> None: 
        #sent command to Arduino
        print(self.command_dict[prediction.command])
        print(self.turn_dict[prediction.turn])
        print(self.speed_dict[self.virtual_joystick.event.speed])
        self.virtual_joystick.listen(self.virtual_joystick.event.speed)
        self.virtual_joystick.listen(self.command_dict[prediction.command])
        self.virtual_joystick.listen(self.turn_dict[prediction.turn])

    def start_self_driving(self):
        while (self.run):
            ret, frame = self.cap.read()
            prediction_yolo = self.Yolo_module.predict(frame)
            self.virtual_joystick.event.speed, self.is_stop = self.Yolo_module.reset_parameter(frame, prediction_yolo, self.virtual_joystick.event.speed, self.is_stop)
            prediction =  self.__predict(frame, self.virtual_joystick.event.speed)
            # print(prediction.command, prediction.turn)
            cv2.putText(frame, "Command: {} Turn: {}".format(prediction.command, prediction.turn), (10, 60), cv2.FONT_HERSHEY_SIMPLEX, 1, (154, 24, 90), 2)
            if (self.is_show):
                cv2.imshow("cap", frame)
                if cv2.waitKey(1) == ord('q'):
                    cv2.destroyWindow("cap")
                    self.run = False
            if (not self.is_stop):
                self.__sent_command(prediction)
            else:
                self.virtual_joystick.listen("stop")

    def start(self):
        self.thread_self_driving.setDaemon(True)
        self.thread_self_driving.start()

    def stop(self):
        self.thread_self_driving.join()

if __name__ == "__main__":
    self_driving_car = Self_driving_car(True)
    self_driving_car.start()
    self_driving_car.stop()