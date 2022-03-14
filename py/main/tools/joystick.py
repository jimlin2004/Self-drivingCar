import pygame as pg 
try:
    from port import Port
except:
    from tools.port import Port

class Event(object):
    def __init__(self, command, speed, turn):
        self.command = command
        self.speed = speed
        self.turn = turn

class Joystick(object):
    def __init__(self, joystick: int):
        pg.init()
        pg.joystick.init()
        self.joystick = pg.joystick.Joystick(0)
        self.joystick.init()
        self.__axes = {}
        self.__button = {}
        self.__hat = {}
        for i in range(self.joystick.get_numaxes()):
            self.__axes[i] = 0.0
        for i in range(self.joystick.get_numaxes()):
            self.__button[i] = False
        for i in range(self.joystick.get_numhats()):
            self.__hat[i] = False
        self.port = Port()
        self.event = Event(0, 60, 0)

    def listen(self):
        for event in pg.event.get():
            if (event.type == pg.JOYBUTTONDOWN):
                print(event)
                if (event.button == 11):
                    """
                    forward
                    """
                    self.port.write(bytes('1'.encode()))
                    self.event.command = 1
                elif (event.button == 14):
                    """
                    turn right
                    """
                    self.port.write(bytes('3'.encode()))
                    self.event.command = 3
                elif (event.button == 12):
                    """
                    back
                    """
                    self.port.write(bytes('2'.encode()))
                    self.event.command = 2
                elif (event.button == 13):
                    """
                    turn left
                    """
                    self.port.write(bytes('4'.encode()))
                    self.event.command = 4

                elif (event.button == 0):
                    """
                    set speed 40
                    """
                    self.port.write(bytes('A'.encode()))
                    self.event.speed = 40
                elif (event.button == 2):
                    """
                    set speed 60
                    """
                    self.port.write(bytes('B'.encode()))
                    self.event.speed = 60
                elif (event.button == 10):
                    """
                    set speed 100
                    """
                    self.port.write(bytes('C'.encode()))
                    self.event.speed = 100
                elif (event.button == 6):
                    """
                    set 外彎
                    """
                    self.port.write(bytes('O'.encode()))
                    self.event.turn = 1
                elif (event.button == 4):
                    """
                    set 內彎
                    """
                    self.port.write(bytes('I'.encode()))
                    self.event.turn = 2

            if (event.type == pg.JOYBUTTONUP):
                if (event.button == 11 or event.button == 12 or event.button == 13 or event.button == 14):
                    self.port.write(bytes('0'.encode()))
                    self.event.command = 0

    def test(self):
        run = True
        while (run):
            for event in pg.event.get():
                if (event.type == pg.JOYBUTTONDOWN):
                    print(event)

class Virtual_joystick(Joystick):
    def __init__(self):
        try:
            self.port = Port()
        except:
            pass
        self.event = Event(0, 60, 0)

    def listen(self, command: str):
        if (command == "forward"):
            """
            forward
            """
            self.port.write(bytes('1'.encode()))
            self.event.command = 1
        elif (command == "stop"):
            """
            stop
            """
            self.port.write(bytes('0'.encode()))
            self.event.command = 0
        elif (command == "turn_right"):
            """
            turn right
            """
            self.port.write(bytes('3'.encode()))
            self.event.command = 3
        elif (command == "back"):
            """
            back
            """
            self.port.write(bytes('2'.encode()))
            self.event.command = 2
        elif (command == "turn_left"):
            """
            turn left
            """
            self.port.write(bytes('4'.encode()))
            self.event.command = 4

        elif (command == "set_speed_40"):
            """
            set speed 40
            """
            self.port.write(bytes('A'.encode()))
            self.event.speed = 40
        elif (command == "set_speed_60"):
            """
            set speed 60
            """
            self.port.write(bytes('B'.encode()))
            self.event.speed = 60
        elif (command == "set_speed_100"):
            """
            set speed 100
            """
            self.port.write(bytes('C'.encode()))
            self.event.speed = 100
        elif (command == "set_outside_turn"):
            """
            set 外彎
            """
            self.port.write(bytes('O'.encode()))
            self.event.turn = 1
        elif (command == "set_inside_turn"):
            """
            set 內彎
            """
            self.port.write(bytes('I'.encode()))
            self.event.turn = 2

if __name__ == "__main__":
    obj = Joystick(0)
    while (True):
        obj.listen()