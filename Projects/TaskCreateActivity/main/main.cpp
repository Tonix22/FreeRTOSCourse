#include "taskWrapper.h"
#include "ledtask.h"
#include "freertos/FreeRTOS.h"

using namespace std;


// Main function
extern "C" void app_main()
{
    // Create LED task
    LedTask ledTask1("LED Task 1", 4096, 3, GPIO_NUM_32, pdMS_TO_TICKS(2000)); // Blinks LED on pin 2 every 500ms
    ledTask1.start();

    LedTask ledTask2("LED Task 2", 4096, 4, GPIO_NUM_33, pdMS_TO_TICKS(3000)); // Blinks LED on pin 3 every 1000ms
    ledTask2.start();

    LedTask ledTask3("LED Task 3", 4096, 5, GPIO_NUM_2, pdMS_TO_TICKS(4000)); // Blinks LED on pin 3 every 1000ms
    ledTask3.start();

      while (1) {
        vTaskDelay(1000 / portTICK_PERIOD_MS);
    }
}
