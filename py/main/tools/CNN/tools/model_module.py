import tensorflow as tf
try:
    from img_to_data import Converter
except:
    from tools.CNN.tools.img_to_data import Converter
import numpy as np

class Prediction(object):
    def __init__(self, pre: list):
        self.command = None
        self.turn = None
        self.__get_data(pre)

    def __get_data(self, pre: list):
        # self.command, self.turn = [np.argmax(i, axis = 1)[0] for i in pre]
        self.command = pre.argmax(axis=-1)[0]

class Model_Module(object):
    def __init__(self, model_path: str) -> None:
        gpus = tf.config.experimental.list_physical_devices("GPU")
        tf.config.experimental.set_visible_devices(gpus[0], "GPU")
        tf.config.experimental.set_memory_growth(gpus[0], True)
        # self.dict_command = {
        #     1: "forward",
        #     3: "turn_right", 
        #     4: "turn_left"
        # }
        self.dict_command = {
            0: "forward",
            2: "turn_right", 
            1: "turn_left"
        }
        self.dict_speed = {
            0: "straight",
            1: "outside_turn",
            2: "inside_turn"
        }
        print("[INFO] Waitting for load model...")
        self.model = tf.keras.models.load_model(model_path)
        self.converter = Converter()
        print("[INFO] Done!")

    def predict_by_path(self, img_path: str, speed: int) -> np.ndarray:
        data, speed = self.converter.convert(img_path, speed)
        prediction = self.model.predict([data, speed])
        prediction = Prediction(prediction)
        return prediction

    def predict(self, img: np.ndarray, speed: int) -> np.ndarray:
        data, speed = self.converter.convert(img, speed)
        # prediction = self.model.predict([data, speed])
        prediction = self.model.predict(data)
        prediction = Prediction(prediction)
        return prediction

if __name__ == "__main__":
    model_module = Model_Module("model_keras")
    model_module.predict("data1/images/1071.jpg", 100)