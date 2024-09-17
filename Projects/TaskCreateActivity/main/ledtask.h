#ifndef LEDTASK
#define LEDTASK

#include "driver/gpio.h"
#include "freertos/FreeRTOS.h"
#include "freertos/task.h"
#include <stdio.h>

// Derived class for LED control
class LedTask : public Task
{
private:
    gpio_num_t ledPin;
    TickType_t delayMs;
    uint32_t current_level;

public:
    LedTask(const char* name, uint32_t stack, UBaseType_t prio, gpio_num_t pin, TickType_t delay) 
        : Task(name, stack, prio), ledPin(pin), delayMs(delay) 
        {
             printf("LED task create %s \n",name);
             current_level = 0;
        }

    // Override the task function to define LED blinking behavior
    void taskFunction() override
    {
        gpio_reset_pin(ledPin);

        gpio_set_direction(ledPin, GPIO_MODE_OUTPUT);
        
        printf("GPIO has been set %d \n",(int)ledPin);

        for (;;)
        {
            // Toggle the LED (pseudo-code)
            toggleLed(ledPin);
        }
    }

    // Simple LED toggle function (pseudo-code)
    void toggleLed(gpio_num_t pin)
    {
        current_level ^=1;
        printf("GPIO: %d , current_level %ld \n",(int)ledPin, current_level);
        gpio_set_level(pin, current_level);
        vTaskDelay(delayMs / portTICK_PERIOD_MS);
    }
};

#endif