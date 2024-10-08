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

#pragma once
#include "freertos/FreeRTOS.h"
#include "freertos/task.h"
#include <stdio.h>
#include <string>

class ConsumerTask : public Task 
{
    private:
    int sampling_period;
    QueueHandle_t communication_pipe;
    int receivedValue ;

    public:
    
    ConsumerTask(int sampling_period, QueueHandle_t queue) : Task("ConsumerTask",4096,4), sampling_period(sampling_period), communication_pipe(queue) {}

    void taskFunction() override
    {
        for(;;)
        {
            vTaskDelay(sampling_period / portTICK_PERIOD_MS);
            if ( xQueueReceive ( communication_pipe , & receivedValue , portMAX_DELAY ))
            {
                printf("Successfully received data from queue: %d\n",receivedValue);
            }
        }
    }
};