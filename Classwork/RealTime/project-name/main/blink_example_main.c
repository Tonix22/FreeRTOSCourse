#include <stdio.h>
#include "freertos/FreeRTOS.h"
#include "freertos/task.h"
#include "driver/gpio.h"
#include "esp_log.h"
#include "esp_timer.h"

static const char *TAG = "example";

#define BLINK_GPIO CONFIG_BLINK_GPIO
static uint8_t s_led_state = 0;
static long long current_time = 0;//2^64 us = 584,000 years
static long long time_elpased = 0;
static void blink_led(void *arg)
{
    time_elpased = esp_timer_get_time() - current_time;
    current_time = esp_timer_get_time();
    /* Set the GPIO level according to the state (LOW or HIGH) */
    gpio_set_level(BLINK_GPIO, s_led_state);
    printf("Time elpased: %lld us\n", time_elpased);
    printf("Current Time: %lld us\n", current_time);
    /* Toggle the LED state */
    s_led_state = !s_led_state;
}

static void configure_led(void)
{
    ESP_LOGI(TAG, "Configuring GPIO for LED Blink");
    gpio_reset_pin(BLINK_GPIO);
    gpio_set_direction(BLINK_GPIO, GPIO_MODE_OUTPUT);
}

void app_main(void)
{
    /* Configure the LED GPIO */
    configure_led();

    /* Initialize the ESP timer */
    esp_timer_create_args_t timerCreate = {
        .callback = blink_led,
        .arg = NULL,
        .name = "blink_timer",
        .dispatch_method = ESP_TIMER_TASK, // Use TASK instead of ISR for safer operations
    };

    esp_timer_handle_t handler;
    esp_err_t ret = esp_timer_create(&timerCreate, &handler);
    if (ret != ESP_OK) {
        ESP_LOGE(TAG, "Failed to create timer: %s", esp_err_to_name(ret));
        return;
    }
    //First time getting the real time.
    current_time = esp_timer_get_time();
    /* Start the timer with a periodic interval */
    ret = esp_timer_start_periodic(handler, 1000 * CONFIG_BLINK_PERIOD);
    if (ret != ESP_OK) {
        ESP_LOGE(TAG, "Failed to start timer: %s", esp_err_to_name(ret));
        return;
    }
    
    while (1) {
        ESP_LOGI(TAG, "LED is currently %s", s_led_state ? "ON" : "OFF");
        vTaskDelay(CONFIG_BLINK_PERIOD / portTICK_PERIOD_MS);
    }
}
