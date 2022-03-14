#include "DC_motor.h"

#define M1Pin1 4
#define M1Pin2 5
#define M2Pin1 6
#define M2Pin2 7
#define E1Pin 3
#define E2Pin 9

DC_motor dc_motor(M1Pin1, M1Pin2, E1Pin, M2Pin1, M2Pin2, E2Pin);

void setup()
{
    pinMode(M1Pin1, OUTPUT);
    pinMode(M1Pin2, OUTPUT);
    pinMode(E1Pin, OUTPUT);
    pinMode(M2Pin1, OUTPUT);
    pinMode(M2Pin2, OUTPUT);
    pinMode(E2Pin, OUTPUT);
}

void loop()
{
    dc_motor.go_ahead(255);
    delay(2000);
    dc_motor.back(255);
    delay(2000);
    dc_motor.turn_left(255);
    delay(2000);
    dc_motor.turn_right(255);
    delay(2000);
    dc_motor.stop();
    delay(2000);
}
