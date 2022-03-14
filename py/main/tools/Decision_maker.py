from tools.CNN.tools.model_module import Model_Module
import numpy as np

class Decision_maker(object):
    def __init__(self, path: str):
        self.model_module = Model_Module(path)
    def predict(self, img: np.ndarray, speed: int):
        return self.model_module.predict(img, speed)