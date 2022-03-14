import cv2
import tensorflow as tf
import numpy as np

class Converter(object):
    def __init__(self):
        self.speed_dict = {
            40: np.array([1, 0, 0]),
            60: np.array([0, 1, 0]),
            100: np.array([0, 0, 1])
        }

    def convert_from_img_by_path(self, path: str, speed: int) -> np.ndarray:
        speed = self.speed_dict[speed]
        speed = np.reshape(speed, (1, speed.shape[0]))
        img = cv2.imread(path)
        img = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        img = img / 255
        data = np.reshape(img, (1, img.shape[0], img.shape[1], 1))
        return [data, speed]

    def convert(self, img: np.ndarray, speed: int) -> np.ndarray:
        speed = self.speed_dict[speed]
        speed = np.reshape(speed, (1, 3))
        img = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        img = img / 255
        data = cv2.resize(img, (320, 320))
        data = np.reshape(data, (1, 320, 320, 1))
        return [data, speed]

if __name__ == "__main__":
    obj = Converter()
    # obj.convert("test", 40)