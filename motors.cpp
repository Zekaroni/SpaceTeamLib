#include <iostream>
#include <pigpio.h>

int main() {
    if (gpioInitialise() < 0)
    {
        std::cerr << "GPIO initialization failed." << std::endl;
        return 1;
    }

    const int servoPin = 18;
    const int nativePulse = 2000;

    gpioSetMode(servoPin, PI_OUTPUT);

    while (true)
    {
        for (int angle = 0; angle <= 180; angle += 10)
        {
            int pulseWidth = nativePulse + angle * 10;
            gpioServo(servoPin, pulseWidth);
            time_sleep(0.5);
        };
        for (int angle = 180; angle >= 0; angle -= 10)
        {
            int pulseWidth = nativePulse + angle * 10;
            gpioServo(servoPin, pulseWidth);
            time_sleep(0.5);
        };
    };

    gpioTerminate();
    return 0;
}