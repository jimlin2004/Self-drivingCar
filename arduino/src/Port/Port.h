#ifndef Port_h
#define Port_h

#include <Arduino.h>
#include "..\\DC_motor\\DC_motor.h"

/*go_ahead -> 0
stop -> 1
back -> 2
turn_right -> 3
turn_left -> 4
*/

class Port
{
private:
    byte command;
    DC_motor dc_motor;
public:
    Port(DC_motor dc_motor);
    void read();
    void activate(byte speed);
};

#endif //Port_h