import serial

class Port(object):
    def __init__(self):
        self.com = serial.Serial("com3", 115200)
    def write(self, command):
        self.com.write(command)

if __name__ == "__main__":
    port = Port()
    while (True):
        try:
            command = input()
        except EOFError:
            break
        port.write(bytes(command.encode()))
        print(port.com.read())
    port.com.close()