#ifndef HYSRF05_H
#define HYSRF05_H

#include <Arduino.h>
class UltrasonicRanger
{
private:
    byte trigPin, echoPin, speakerPin;
    float V;
    float get_voice_speed();
public:
    UltrasonicRanger(byte trigPin, byte echoPin);
    float get_distance();
};

#endif