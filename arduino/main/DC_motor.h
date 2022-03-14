#include "Arduino.h"

#ifndef DC_MOTOR_H
#define DC_MOTOR_H

void test();

class DC_motor
{
private:
    int M1Pin1, M1Pin2, E1Pin, M2Pin1, M2Pin2, E2Pin;
public:
    byte speed;
    DC_motor(int M1Pin1, int M1Pin2, int E1Pin, int M2Pin1, int M2Pin2, int E2Pin);
    void turn_left();
    void turn_right();
    void right_and_forward(int turn);
    void left_and_forward(int turn);
    void forward();
    void back();
    void stop();
    void set_speed(byte speed);
};

#endif //DC_MOTOR_H