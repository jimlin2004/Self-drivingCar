import socket
import cv2 
import pickle
import struct
import os

class Server(object):
    def __init__(self, host: str, port: int):
        self.__host = host
        self.__port = port
        self.server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.server.bind((self.__host, self.__port))
        self.server.listen(5)
        print("\033[1;32;1m [INFO] Listening on {}:{} \033[0m\n".format(self.__host, self.__port))
    def listen_and_recv(self):
        while (1):
            conn, addr = self.server.accept()
            print("\033[1;32;1m [INFO] Connected by {} \033[0m\n".format(addr))
            while (1):
                data = str(conn.recv(1024), encoding = "utf-8")
                # data = conn.recv(1024)
                print("Client recv data: {}".format(data))
                if (data == 'q'):
                    conn.send("881".encode())
                    break
                conn.send("got it".encode())
            break
        conn.close()
    def listen_and_show(self):
        conn, addr = self.server.accept()
        print("\033[1;32;1m [INFO] Connected by {} \033[0m\n".format(addr))
        data = b""
        payload_size = struct.calcsize("Q")
        while (1):
            while (len(data) < payload_size):
                data += conn.recv(4096)
            packed_msg_size = data[:payload_size]
            data = data[payload_size:]
            msg_size = struct.unpack("Q", packed_msg_size)[0]
            while (len(data) < msg_size):
                data += conn.recv(4096)
            frame_data = data[:msg_size]
            data = data[msg_size:]
            frame = pickle.loads(frame_data, fix_imports=True, encoding="bytes")
            frame = cv2.imdecode(frame, cv2.IMREAD_COLOR)
            cv2.imshow("frame", frame)
            key = cv2.waitKey(1)
            if (key == ord('q')):
                cv2.destroyWindow("frame")
                break
        conn.close()
    def recv_data(self):
        conn, addr = self.server.accept()
        print("\033[1;32;1m [INFO] Connected by {} \033[0m\n".format(addr))
        data = b""
        payload_size = struct.calcsize("Q")
        with open("data/data.csv", "w") as f:
            while (1):
                while (len(data) < payload_size):
                    data += conn.recv(4096)
                packed_msg_size = data[:payload_size]
                data = data[payload_size:]
                msg_size = struct.unpack("Q", packed_msg_size)[0]
                while (len(data) < msg_size):
                    data += conn.recv(4096)
                pickle_data = data[:msg_size]
                data = data[msg_size:]
                pickle_data = pickle.loads(pickle_data)
                frame = cv2.imdecode(pickle_data["image"], cv2.IMREAD_COLOR)
                img_num = len(os.listdir("data/images"))
                cv2.imwrite("data/images/{}.jpg".format(img_num), frame)
                f.write("{},{},{},{}\n".format("images/{}.jpg".format(img_num), pickle_data["command"], pickle_data["speed"], pickle_data["turn"]))
                cv2.imshow("frame", frame)
                key = cv2.waitKey(1)
                # print(pickle_data)
                if key == ord('q'):
                    break
            cv2.destroyWindow("frame")
        conn.close()

if __name__ == "__main__":
    server = Server("192.168.168.15", 8000)
    # server.listen_and_recv()
    # server.listen_and_show()
    server.recv_data()