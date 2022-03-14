import cv2 
import numpy as np
import math

class LaneFinding(object):
    def __init__(self, cap_num: int) -> None:
        self.cap = cv2.VideoCapture(cap_num)

    def __gamma_transform(self, img: np.ndarray) -> np.ndarray:
        mean = np.mean(img) if (len(img.shape) == 2) else np.mean(cv2.cvtColor(img, cv2.COLOR_BGR2GRAY))
        gamma = math.log10(0.5) / math.log10(mean / 255)
        gamma_table = [np.power(x / 255.0, gamma) * 255.0 for x in range(256)]
        gamma_table = np.round(np.array(gamma_table)).astype(np.uint8)
        return cv2.LUT(img, gamma_table)

    def __ROI_area(self, img) -> np.ndarray:
        points1 = np.array([[0, 480], [150, 250], [490, 250], [640, 480]])
        mask = np.zeros_like(img)
        cv2.fillPoly(mask, [points1], (255, 255, 255))
        mask_img = cv2.bitwise_and(img, mask)
        return mask_img

    def transform_img(self, img: np.ndarray) -> np.ndarray:
        # points1 = np.float32([[0, 480], [180, 50], [460, 50], [640, 480]])
        points1 = np.float32([[0, 480], [150, 250], [490, 250], [640, 480]])
        points2 = np.float32([[0, 480], [0, 0], [640, 0], [640, 480]])
        M = cv2.getPerspectiveTransform(points1, points2)
        transform_img = cv2.warpPerspective(img, M, (640, 480))
        return transform_img

    def __circle_point(self, img):
        points = np.array([[0, 480], [150, 250], [490, 250], [640, 480]])
        for p in points:
            cv2.circle(img, p, 5, (0, 0, 200), 3)
        # cv2.imshow("circle", img)

    def __find_line(self, frame: np.ndarray) -> np.ndarray:
        frame_br = cv2.GaussianBlur(frame, (7,7), 0)
        frame_canny = cv2.Canny(frame_br, 100, 200)
        frame_canny = self.__ROI_area(frame_canny)
        # cv2.imshow("canny", frame_canny)
        lines = cv2.HoughLinesP(frame_canny  , 1, np.pi / 180, 1, np.array([]), 1, 10)
        canvas = np.zeros(frame_canny.shape)
        if (lines is not None):
            for line in lines:
                for x1, y1, x2, y2 in line:
                    # cv2.line(frame, (x1, y1), (x2, y2), (230, 57, 70), 3)
                    cv2.line(canvas, (x1, y1), (x2, y2), (255, 255, 255), 1)
        canvas = self.transform_img(canvas)
        cv2.imshow("canvas", canvas)
        return frame

    def run(self) -> None:
        while(self.cap.isOpened()):
            t = cv2.getTickCount()
            ret, frame = self.cap.read()            
            frame = self.__gamma_transform(frame)
            frame = self.__transform_img(frame)
            # self.__circle_point(frame)
            # frame = self.__ROI_area(frame)
            # frame = self.__find_line(frame)
            # self.__circle_point(frame)
            t = (cv2.getTickCount() - t) / cv2.getTickFrequency()
            fps = str(round((1.0 / t), 3))
            cv2.putText(frame, "FPS: "+fps, (0, 50), cv2.FONT_HERSHEY_SIMPLEX, 1, (143, 157, 42), 3)
            cv2.imshow("cap", frame)
            key = cv2.waitKey(1)
            if (key == ord('q')):
                self.cap.release()
        cv2.destroyAllWindows()
        # cv2.destroyWindow("cap")
    
    def test(self):
        img = cv2.imread("E:/code/project/Self-drivingCar/py/main/tools/data1/images/0.jpg")
        cv2.imshow("origin", img)
        cv2.imshow("ga", self.__gamma_transform(img))
        cv2.imshow("trans", self.transform_img(img))
        cv2.waitKey(0)

if __name__ == "__main__":
    lanefinding = LaneFinding(0)
    # lanefinding.__test()
    lanefinding.test()