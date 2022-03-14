import socket
import cv2
import numpy as np
import pickle
import struct

class Client(object):
    def __init__(self, host: str, port: int):
        try:
            self.__host = host
            self.__port = port
            self.client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            self.client.connect((self.__host, self.__port))
        except socket.error as e:
            print("\033[1;32;1m [Error] \033[0m\n", e)
    def run(self):
        while (1):
            msg = input("please input msg: ")
            self.client.send(msg.encode())
            server_msg = str(self.client.recv(1024), encoding="utf-8")
            print("Sever: {}".format(server_msg))
            if (msg == 'q'):
                break
        self.client.close()
    def sent_webcam_frame(self, frame: np.ndarray):
        encode_param = [int(cv2.IMWRITE_JPEG_QUALITY), 90]
        try:
            frame = cv2.resize(frame, (320, 320))
            result, img_encode = cv2.imencode(".jpg", frame, encode_param)
            data = pickle.dumps(img_encode, 0)
            size = len(data)
            self.client.sendall(struct.pack("Q", size) + data)
            # cv2.imshow("client", frame)
            # cv2.waitKey(0)
            return True
        except socket.error as e:
            print(e)
            return False
    def test(self):
        encode_param = [int(cv2.IMWRITE_JPEG_QUALITY), 90]
        frame = cv2.imread("tools/lim60-0.png")
        try:
            frame = cv2.resize(frame, (320, 320))
            frame = cv2.flip(frame, 180)
            result, img_encode = cv2.imencode(".jpg", frame, encode_param)
            data = pickle.dumps(img_encode, 0)
            print(data)
            # size = len(data)
            self.client.sendall(data)
            # cv2.imshow("client", frame)
            # cv2.waitKey(0)
            return True
        except socket.error as e:
            print(e)
            return False
    def sent_data(self, data, size):
        try:
            self.client.sendall(struct.pack("Q", size) + data)
            return True
        except socket.error as e:
            print(e)
            return False

if __name__ == "__main__":
    client = Client("127.0.0.1", 8000)
    client.test()