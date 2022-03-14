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
    // this->speed = (byte)((255 - 110)*(60.0/100.0) + 110);
    this->speed = 200;
}

void DC_motor::forward()
{
    digitalWrite(this->M1Pin1, HIGH);
    digitalWrite(this->M1Pin2, LOW);
    digitalWrite(this->M2Pin1, HIGH);
    digitalWrite(this->M2Pin2, LOW);
    analogWrite(this->E1Pin, this->speed);
    analogWrite(this->E2Pin, this->speed);
}

void DC_motor::back()
{
    digitalWrite(this->M1Pin1, LOW);
    digitalWrite(this->M1Pin2, HIGH);
    digitalWrite(this->M2Pin1, LOW);
    digitalWrite(this->M2Pin2, HIGH);
    analogWrite(this->E1Pin, this->speed);
    analogWrite(this->E2Pin, this->speed);
}

void DC_motor::turn_right()
{
    digitalWrite(this->M1Pin1, LOW);
    digitalWrite(this->M1Pin2, LOW);
    digitalWrite(this->M2Pin1, HIGH);
    digitalWrite(this->M2Pin2, LOW);
    analogWrite(this->E2Pin, this->speed);
}

void DC_motor::turn_left()
{
    digitalWrite(this->M1Pin1, HIGH);
    digitalWrite(this->M1Pin2, LOW);
    digitalWrite(this->M2Pin1, LOW);
    digitalWrite(this->M2Pin2, LOW);
    analogWrite(this->E1Pin, this->speed);
}

void DC_motor::right_and_forward(int turn)
{
    if (turn == 1)
    {
        digitalWrite(this->M1Pin1, HIGH);
        digitalWrite(this->M1Pin2, LOW);
        digitalWrite(this->M2Pin1, HIGH);
        digitalWrite(this->M2Pin2, LOW);
        // analogWrite(this->E1Pin, (int)(this->speed / 1.8));
        analogWrite(this->E1Pin, 120);
        analogWrite(this->E2Pin, 200);
    }
    else if (turn == 2)
    {
        digitalWrite(this->M1Pin1, HIGH);
        digitalWrite(this->M1Pin2, LOW);
        digitalWrite(this->M2Pin1, HIGH);
        digitalWrite(this->M2Pin2, LOW);
        // analogWrite(this->E1Pin, (int)(this->speed / 4));
        analogWrite(this->E1Pin, 120);
        analogWrite(this->E2Pin, 200);
    }
}

void DC_motor::left_and_forward(int turn)
{
    if (turn == 1)
    {
        digitalWrite(this->M1Pin1, HIGH);
        digitalWrite(this->M1Pin2, LOW);
        digitalWrite(this->M2Pin1, HIGH);
        digitalWrite(this->M2Pin2, LOW);
        analogWrite(this->E1Pin, 200);
        analogWrite(this->E2Pin, 120);
    }
    else if (turn == 2)
    {
        digitalWrite(this->M1Pin1, HIGH);
        digitalWrite(this->M1Pin2, LOW);
        digitalWrite(this->M2Pin1, HIGH);
        digitalWrite(this->M2Pin2, LOW);
        analogWrite(this->E1Pin, 200);
        analogWrite(this->E2Pin, 120);
    }
}

void DC_motor::stop()
{
    digitalWrite(this->M1Pin1, LOW);
    digitalWrite(this->M1Pin2, LOW);
    digitalWrite(this->M2Pin1, LOW);
    digitalWrite(this->M2Pin2, LOW);
}

void DC_motor::set_speed(byte speed)
{
    this->speed = (byte)((255 - 110) * (speed / 100.0) + 110);
}