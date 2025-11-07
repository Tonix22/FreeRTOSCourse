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
//#include "freertos/semaphore.h"
#include "delaytask.h"

using namespace std;
SemaphoreHandle_t xSemaphore;// use this sempahore as a controler between task
QueueHandle_t xQueue;

typedef struct twoValues
{
  long real;
  long imaginary;
}ComplexData;

//void* is a generic data type pointer
void vAlice(void *pvParameters)
{
  int UART_ready = 10;
  int cnt = 0;
  ComplexData complexValue;
  complexValue.real = 777;
  complexValue.imaginary = 888;
  
  xQueueSend (xQueue , &complexValue , 0);
  //xSemaphoreTake(xSemaphore, portMAX_DELAY);
  //take until Uart is done
  for(;;)
  {
    vTaskDelay(5000/portTICK_PERIOD_MS);
    complexValue.real++;
    complexValue.imaginary++;
    xQueueSend (xQueue , &complexValue , 0);
    //if(cnt == UART_ready)
    //{
    //  xSemaphoreGive(xSemaphore);
    //}
  }
}

void vBob(void *pvParameters)
{
  //xSemaphoreTake(xSemaphore, portMAX_DELAY);
  ComplexData recievedComplex;
  for(;;)
  {
    vTaskDelay(1000/portTICK_PERIOD_MS);
    xQueueReceive(xQueue , & recievedComplex , portMAX_DELAY );
    printf("Complex value: r:%ld,i:%ld\n",recievedComplex.real,recievedComplex.imaginary);
    //vTaskDelay(2000/portTICK_PERIOD_MS);
  }
}

// Main function
extern "C" void app_main()
{
  int* bobint = (int*)malloc(sizeof(int));// ask for one element
  *bobint = 3; //change value to that element

  xSemaphore = xSemaphoreCreateBinary();
  xQueue = xQueueCreate(3,sizeof(ComplexData));//160 bytes
  if(xQueue == NULL)
  {
    printf("Queue creation fail\n");
  }


  if(xSemaphore == NULL)
  {
    printf("We dont have heap space\n");
    //heap space dynamic memory allocation
    //dynamic alloaction wasn't possible
  }
  else
  {
    xSemaphoreGive(xSemaphore);
  }
  
  xTaskCreate(vAlice,"Alice",4096,NULL,3,NULL);
  xTaskCreate(vBob,"Bob",4096,bobint,2,NULL);//share 3 to the task
  
  while (1) 
  {
    vTaskDelay(100 / portTICK_PERIOD_MS);

  }
  // Create LED task
    /*
    LedTask ledTask1("LED Task 1", 4096, 3, GPIO_NUM_32, pdMS_TO_TICKS(2000)); // Blinks LED on pin 2 every 500ms
    ledTask1.start();

    LedTask ledTask2("LED Task 2", 4096, 4, GPIO_NUM_33, pdMS_TO_TICKS(3000)); // Blinks LED on pin 3 every 1000ms
    ledTask2.start();

    LedTask ledTask3("LED Task 3", 4096, 5, GPIO_NUM_2, pdMS_TO_TICKS(4000)); // Blinks LED on pin 3 every 1000ms
    ledTask3.start();
    */

    //DelayTask delay1(1000,"Delay Task 1");
    //DelayTask delay2(2000,"Delay Task 2");

    //delay1.start();
    //delay2.start();

  
}
