/*
 * Copyright (c) 2024 Tonix22
 * 
 * Permission is hereby granted, free of charge, to any person obtaining a copy
 * of this software and associated documentation files (the "Software"), to deal
 * in the Software without restriction, including without limitation the rights
 * to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
 * copies of the Software, and to permit persons to whom the Software is
 * furnished to do so, subject to the following conditions:
 * 
 * The above copyright notice and this permission notice shall be included in all
 * copies or substantial portions of the Software.
 * 
 * THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
 * IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
 * FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
 * AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
 * LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
 * OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
 * SOFTWARE.
 */
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
