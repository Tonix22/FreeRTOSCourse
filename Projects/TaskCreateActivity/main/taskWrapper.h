
#ifndef TASKWRAPPER
#define TASKWRAPPER

#include "freertos/FreeRTOS.h"
#include "freertos/task.h"
#include <stdio.h>
// Base class for all tasks
class Task
{
protected:
    const char* taskName;
    uint32_t stackSize;
    UBaseType_t priority;
    TaskHandle_t taskHandle;

public:
    Task(const char* name, uint32_t stack, UBaseType_t prio) 
        : taskName(name), stackSize(stack), priority(prio), taskHandle(nullptr) {}

    virtual ~Task() {}

    // Virtual function to define the task's behavior
    virtual void taskFunction() = 0;

    // Start the task
    void start()
    {
        printf("Before start\n");
        xTaskCreate([](void* obj) {
            static_cast<Task*>(obj)->taskFunction();
        }, taskName, stackSize, this, priority, &taskHandle);
        printf("After start\n");
    }

    // Stop the task
    void stop()
    {
        if (taskHandle != nullptr)
        {
            vTaskDelete(taskHandle);
            taskHandle = nullptr;
        }
    }
};

#endif