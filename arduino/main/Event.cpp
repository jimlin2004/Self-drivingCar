#include "Event.h"
Event::Event()
{
    this->command = 0;
    /*
    0 -> 直線
    1 -> 外彎
    2 -> 內彎
    */
    this->turn = 1;
}