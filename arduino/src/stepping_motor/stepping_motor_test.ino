#include <Unistep2.h>

Unistep2 stepper(8, 9 ,10, 11, 4096, 1000);

void setup()
{

}

void loop()
{
    stepper.run();

    if (stepper.stepsToGo() == 0)
    {
        delay(500);
        stepper.move(4096);
    }
}