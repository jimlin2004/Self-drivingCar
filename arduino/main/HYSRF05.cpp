#include <Arduino.h>
#include "HYSRF05.h"

UltrasonicRanger::UltrasonicRanger(byte trigPin, byte echoPin)
{
    this->trigPin = trigPin;
    this->echoPin = echoPin;
    this->V = this->get_voice_speed();
}

float UltrasonicRanger::get_voice_speed()
{
    int T = 30;
    float V = (331 + 0.6 * T) / 10000;
    float t = 1 / V;
    return t * 2;
}

float UltrasonicRanger::get_distance()
{
    digitalWrite(this->trigPin, LOW);
    delayMicroseconds(5);
    digitalWrite(this->trigPin, HIGH);
    delayMicroseconds(10);
    digitalWrite(this->trigPin, LOW);
    float distance = pulseIn(this->echoPin, HIGH) / this->V;
    return distance;
}