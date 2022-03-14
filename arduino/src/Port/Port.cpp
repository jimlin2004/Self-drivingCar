#include "Port.h"
#include <Arduino.h>
#include "..\\DC_motor\\DC_motor.h"

/*go_ahead -> 0
stop -> 1
back -> 2
turn_right -> 3
turn_left -> 4
*/

Port::Port(DC_motor dc_motor)
{
    this->dc_motor = dc_motor;
}

void Port::read()
{
    this->command = Serial.read();
}

void Port::activate(byte speed)
{
    if (this->command == 0)
        this->dc_motor.go_ahead(speed);
    else if (this->command == 1)
        this->dc_motor.stop();
    else if (this->command == 2)
        this->dc_motor.back(speed);
    else if (this->command == 3)
        this->dc_motor.turn_right(speed);
    else if (this->command == 4)
        this->dc_motor.turn_left(speed);
}