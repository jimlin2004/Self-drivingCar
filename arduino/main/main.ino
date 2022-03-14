#include "DC_motor.h"
#include "HYSRF05.h"
#include "Event.h"

#define M1Pin1 4
#define M1Pin2 5
#define M2Pin1 6
#define M2Pin2 7
#define E1Pin 3
#define E2Pin 9
#define trigPin 13
#define echoPin 12

DC_motor dc_motor(M1Pin1, M1Pin2, E1Pin, M2Pin1, M2Pin2, E2Pin);
char command;

UltrasonicRanger ultrasonic_ranger(trigPin, echoPin);
float distance;

// int event = 1;
Event event;

void setup()
{
    Serial.begin(115200);
    pinMode(M1Pin1, OUTPUT);
    pinMode(M1Pin2, OUTPUT);
    pinMode(M2Pin1, OUTPUT);
    pinMode(M2Pin2, OUTPUT);
    pinMode(E1Pin, OUTPUT);
    pinMode(E2Pin, OUTPUT);
    pinMode(trigPin, OUTPUT);
    pinMode(echoPin, INPUT);
}

void loop()
{
    distance = ultrasonic_ranger.get_distance();
    if (Serial.available())
    {
        command = Serial.read();
        if (command == '0')
        {
            dc_motor.stop();
            event.command = 0;
        }
        else if (command == '1')
        {
            if (distance > 15)
            {
                dc_motor.forward();
                event.command = 1;
            }
            else
            {
                dc_motor.stop();
                event.command = 0;
            }
        }
        else if (command == '2')
        {
            dc_motor.back();
            event.command = 2;
        }
        else if (command == '3')
        {
            // dc_motor.turn_right();
            dc_motor.right_and_forward(event.turn);
            event.command = 3;
        }
        else if (command == '4')
        {
            // dc_motor.turn_left();
            dc_motor.left_and_forward(event.turn);
            event.command = 4;
        }
        //換速
        else if (command == 'A')
        {
            dc_motor.set_speed(40);
        }
        else if (command == 'B')
        {
            dc_motor.set_speed(60);
        }
        else if (command == 'C')
        {
            dc_motor.set_speed(100);
        }

        //內灣->I/外彎->O
        else if (command == 'I')
        {
            event.turn = 2;
        }
        else if (command == 'O')
        {
            event.turn = 1;
        }

        else
        {
            dc_motor.stop();
            event.command = 0;
        }
    }
    else if ((event.command == 1 || event.command == 3 || event.command == 4) && distance <= 15)
    {
        dc_motor.stop();
        event.command = 0;
    }
}