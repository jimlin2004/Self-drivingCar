import cv2
import numpy as np

class Predict(object):
    def __init__(self, classname: str, box: list, conf: float):
        self.classname = classname
        self.box = box
        self.conf = conf

class Yolo_module(object):
    def __init__(self, classfile_path: str, cfg_path: str, weight_path: str, cap_num = 0) -> None:
        self.classnames = []
        with open(classfile_path, "rt") as f:
            self.classnames = f.read().rstrip("\n").split("\n")
        self.net = cv2.dnn.readNetFromDarknet(cfg_path, weight_path)
        self.net.setPreferableBackend(cv2.dnn.DNN_BACKEND_OPENCV)
        self.input_width = 320
        self.input_height = 320
        self.confThreshold = 0.5
        self.nmsThreshold = 0.3

    def __findObjects(self, outputs, img: np.ndarray) -> list:
        H, W, C = img.shape
        bbox = []
        classids = []
        confs = []
        for output in outputs:
            for array in output:
                scores = array[5:]
                classid = np.argmax(scores)
                confidence = scores[classid]
                if(confidence > self.confThreshold):
                    w, h = int(array[2] * W), int(array[3] * H)
                    x, y = int((array[0] * W) - w/2), int((array[1] * H) - h/2)
                    bbox.append([x,y,w,h])
                    classids.append(classid)
                    confs.append(float(confidence))
        indices = cv2.dnn.NMSBoxes(bbox, confs, self.confThreshold, self.nmsThreshold)
        result = []
        for i in indices:
            box = bbox[i[0]]
            classname = self.classnames[classids[i[0]]]
            conf = confs[i[0]]
            pre = Predict(classname, box, conf)
            result.append(pre)
        return result

    def predict(self, img) -> list:
        blob = cv2.dnn.blobFromImage(img, 1/255, (self.input_width, self.input_height), [0,0,0], 1, crop = False)
        self.net.setInput(blob)
        layernames = self.net.getLayerNames()
        outputnames = [layernames[i[0] - 1] for i in self.net.getUnconnectedOutLayers()]
        outputs = self.net.forward(outputnames)
        return self.__findObjects(outputs, img)

    def __puttext_and_draw_pre(self, img: np.ndarray, obj: Predict):
        cv2.rectangle(img, (obj.box[0], obj.box[1]), (obj.box[0] + obj.box[2], obj.box[1] + obj.box[3]), (150, 0, 0), 2)
        cv2.putText(img,"{} {}%".format(obj.classname, int(obj.conf*100)), (obj.box[0], obj.box[1] - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.6, (255, 0, 255), 2)

    def reset_parameter(self, img: np.ndarray, pre: list, speed: int, is_stop: bool):
        speed = speed
        is_stop = False
        for obj in pre:
            if (obj.conf >= 0.5):
                # print(f"{obj.box[2]}, {obj.box[3]}")
                self.__puttext_and_draw_pre(img, obj)
                if (obj.classname == "Limit40"):
                    speed = 40
                elif (obj.classname == "Limit60"):
                    speed = 60
                elif (obj.classname == "Limit100"):
                    speed = 100
                if ((obj.classname == "Human" or obj.classname == "RedLight" or obj.classname == "Car") and (obj.box[2] >= 60 and obj.box[3] >= 60)):
                    is_stop = True
                    print("STOP")
                else:
                    is_stop = False
                    
        return [speed, is_stop]
    
    def test(self, img: np.ndarray):
        pre = self.predict(img)
        for obj in pre:
            if (obj.conf >= 0.5):
                self.__puttext_and_draw_pre(img, obj)
                if ((obj.classname == "Human" or obj.classname == "RedLight" or obj.classname == "Car") and (obj.box[2] >= 120 and obj.box[3] >= 120)):
                    print("STOP")
                    print(f"{obj.box[2]}, {obj.box[3]}")
    
if __name__ == "__main__":
    obj = Yolo_module("cfg/self-driving-car.names", "cfg/yolov4-tiny.cfg", "weight/yolov4-tiny_final.weights")
    cap = cv2.VideoCapture(0)
    while (cap.isOpened()):
        ret, img = cap.read()
        obj.test(img)
        cv2.imshow("img", img)
        cv2.waitKey(1)