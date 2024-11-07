#include <FreeRTOS.h>
#include "task.h"
#include "queue.h"
#include "semphr.h"
#include "event_groups.h"
#include "timers.h"

enum EventBits {
    TRAFFIC_UPDATE_BIT = (1 << 0),
    EMERGENCY_ALERT_BIT = (1 << 1),
    SYSTEM_ERROR_BIT = (1 << 2)
};

class TrafficInterface {
public:
    TrafficInterface();
    void transmitData(const uint8_t* data, size_t len);
    void receiveSensorData(uint8_t* buffer, size_t bufferSize);
private:
    SemaphoreHandle_t txSemaphore;
    SemaphoreHandle_t rxSemaphore;
};

class TrafficDataProcessor {
public:
    TrafficDataProcessor();
    void processData(const uint8_t* data, size_t len);
    void convertEndianness(uint8_t* data, size_t len);
};

void vTaskCollectData(void* pvParameters);
void vTaskCoordinateSignals(void* pvParameters);
void vTaskHandleEmergencies(void* pvParameters);
void vTimerCallback(TimerHandle_t xTimer);
void setupSystem();

int main() {
    setupSystem();
    vTaskStartScheduler();
    return 0;
}
