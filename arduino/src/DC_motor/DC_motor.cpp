#include "Arduino.h"
#include "DC_motor.h"

DC_motor::DC_motor(int M1Pin1, int M1Pin2, int E1Pin, int M2Pin1, int M2Pin2, int E2Pin)
{
    this->M1Pin1 = M1Pin1;
    this->M1Pin2 = M1Pin2;
    this->E1Pin = E1Pin;
    this->M2Pin1 = M2Pin1;
    this->M2Pin2 = M2Pin2;
    this->E2Pin = E2Pin;
}

void DC_motor::go_ahead(byte speed)
{
    digitalWrite(this->M1Pin1, HIGH);
    digitalWrite(this->M1Pin2, LOW);
    digitalWrite(this->M2Pin1, HIGH);
    digitalWrite(this->M2Pin2, LOW);
    analogWrite(this->E1Pin, speed);
    analogWrite(this->E2Pin, speed);
}

void DC_motor::back(byte speed)
{
    digitalWrite(this->M1Pin1, LOW);
    digitalWrite(this->M1Pin2, HIGH);
    digitalWrite(this->M2Pin1, LOW);
    digitalWrite(this->M2Pin2, HIGH);
    analogWrite(this->E1Pin, speed);
    analogWrite(this->E2Pin, speed);
}

void DC_motor::turn_right(byte speed)
{
    digitalWrite(this->M1Pin1, LOW);
    digitalWrite(this->M1Pin2, LOW);
    digitalWrite(this->M2Pin1, HIGH);
    digitalWrite(this->M2Pin2, LOW);
    analogWrite(this->E2Pin, speed);
}

void DC_motor::turn_left(byte speed)
{
    digitalWrite(this->M1Pin1, HIGH);
    digitalWrite(this->M1Pin2, LOW);
    digitalWrite(this->M2Pin1, LOW);
    digitalWrite(this->M2Pin2, LOW);
    analogWrite(this->E1Pin, speed);
}

void DC_motor::stop()
{
    digitalWrite(this->M1Pin1, LOW);
    digitalWrite(this->M1Pin2, LOW);
    digitalWrite(this->M2Pin1, LOW);
    digitalWrite(this->M2Pin2, LOW);
}