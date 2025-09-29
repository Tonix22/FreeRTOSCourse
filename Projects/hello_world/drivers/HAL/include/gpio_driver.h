#ifndef GPIO_DRIVER_H
#define GPIO_DRIVER_H

#include <stdio.h>
#include <string.h>
#include <stdlib.h>
#include <inttypes.h>
#include "freertos/FreeRTOS.h"
#include "freertos/task.h"
#include "freertos/queue.h"
#include "driver/gpio.h"

/**
 * Brief:
 * This test code shows how to configure gpio and how to use gpio interrupt.
 *
 * GPIO status:
 * GPIO_OUTPUT_IO_0: output
 * GPIO_OUTPUT_IO_1: output
 * GPIO_INPUT_IO_0:  input, pulled up, interrupt from rising edge and falling edge
 * GPIO_INPUT_IO_1:  input, pulled up, interrupt from rising edge.
 *
 * Note. You can check the default GPIO pins to be used in menuconfig, and the IOs can be changed.
 *
 * Test:
 * Connect GPIO_OUTPUT_IO_0 with GPIO_INPUT_IO_0
 * Connect GPIO_OUTPUT_IO_1 with GPIO_INPUT_IO_1
 * Generate pulses on GPIO_OUTPUT_IO_0/1, that triggers interrupt on GPIO_INPUT_IO_0/1
 *
 */

#define GPIO_OUTPUT_IO_0    CONFIG_GPIO_OUTPUT_0
#define GPIO_OUTPUT_IO_1    CONFIG_GPIO_OUTPUT_1
#define GPIO_OUTPUT_PIN_SEL  ((1ULL<<GPIO_OUTPUT_IO_0) | (1ULL<<GPIO_OUTPUT_IO_1))
/*
 * Let's say, GPIO_OUTPUT_IO_0=18, GPIO_OUTPUT_IO_1=19
 * In binary representation,
 * 1ULL<<GPIO_OUTPUT_IO_0 is equal to 0000000000000000000001000000000000000000 and
 * 1ULL<<GPIO_OUTPUT_IO_1 is equal to 0000000000000000000010000000000000000000
 * GPIO_OUTPUT_PIN_SEL                0000000000000000000011000000000000000000
 * */
#define GPIO_INPUT_IO_0     CONFIG_GPIO_INPUT_0
#define GPIO_INPUT_IO_1     CONFIG_GPIO_INPUT_1
#define GPIO_INPUT_PIN_SEL  ((1ULL<<GPIO_INPUT_IO_0) | (1ULL<<GPIO_INPUT_IO_1))

#define ESP_INTR_FLAG_DEFAULT 0

void IRAM_ATTR gpio_isr_handler(void* arg);
void gpio_task_example(void* arg);
void gpio_test(void);

#endif