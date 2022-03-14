#include <Unistep2.h>

Unistep2 stepper1(10, 11, 12, 13, 4096, 900);
Unistep2 stepper2(1, 2, 3, 4, 4096, 900);

void setup()
{

}

void loop()
{
	stepper1.run();
    stepper2.run();
    if (stepper1.stepsToGo() == 0 && stepper2.stepsToGo() == 0)
    {
        stepper1.move(4096);
        stepper2.move(4096);
    }
}
