// app_main.c
#include <time.h>
#include <stdio.h>
#include "freertos/FreeRTOS.h"
#include "freertos/task.h"
#include "esp_system.h"
#include "esp_event.h"
#include "nvs_flash.h"
#include "esp_wifi.h"
#include "mqtt_client.h"
#include "esp_log.h"

#define WIFI_SSID       "Tonix"
#define WIFI_PASS       "typewriter"

#define MQTT_BROKER_URI "mqtt://io.adafruit.com:1883"
#define MQTT_USERNAME   "EmilioTonix"
#define MQTT_PASSWORD   "8281440a417b4e16be3b67ba126247d0"
#define MQTT_TOPIC      "EmilioTonix/feeds/humidity"

static const char *TAG = "MQTT_EXAMPLE";

#include <stdlib.h> // For rand() and srand()
#include <time.h>   // For time()
#include <limits.h> // For INT_MAX
#include <assert.h> // For assert()

// Function to publish messages periodically
static void mqtt_publish_task(void *pvParameters)
{
    esp_mqtt_client_handle_t client = (esp_mqtt_client_handle_t)pvParameters;
    int msg_id;
    char message[5];

    // Seed the random number generator once
    srand(time(NULL));

    while (1)
    {
        // Generate a random number between 0 and 100
        int random_number = rand() % 101;
        
        // Ensure random_number is within 0 to 100
        assert(random_number >= 0 && random_number <= 100);

        // Create the message payload with leading zeros
        snprintf(message, sizeof(message), "%03d", random_number);

        // Publish the message
        msg_id = esp_mqtt_client_publish(client, MQTT_TOPIC, message, 0, 1, 0);
        ESP_LOGI(TAG, "Sent publish message, msg_id=%d, message=%s", msg_id, message);

        // Delay for 5 seconds
        vTaskDelay(pdMS_TO_TICKS(5000));
    }
}



static void mqtt_event_handler(void *handler_args, esp_event_base_t base, int32_t event_id, void *event_data)
{
    esp_mqtt_event_handle_t event = event_data;
    esp_mqtt_client_handle_t client = event->client;

    switch (event->event_id) {
        case MQTT_EVENT_CONNECTED:
            ESP_LOGI(TAG, "MQTT_EVENT_CONNECTED");
            // Subscribe to the topic
            esp_mqtt_client_subscribe(client, MQTT_TOPIC, 0);

            // Start the publishing task
            xTaskCreate(mqtt_publish_task, "mqtt_publish_task", 4096, client, 5, NULL);
            break;

        case MQTT_EVENT_DATA:
            ESP_LOGI(TAG, "MQTT_EVENT_DATA");
            printf("Received data on topic: %.*s\r\n", event->topic_len, event->topic);
            printf("Message: %.*s\r\n", event->data_len, event->data);
            break;

        default:
            ESP_LOGI(TAG, "Other MQTT event id:%d", event->event_id);
            break;
    }
}

void mqtt_app_start(void)
{
    esp_mqtt_client_config_t mqtt_cfg = {
        .broker = {
            .address = {
                .uri = MQTT_BROKER_URI,
            },
        },
        .credentials = {
            .username = MQTT_USERNAME,
            .authentication = {
                .password = MQTT_PASSWORD,
            },
        },
    };

    esp_mqtt_client_handle_t client = esp_mqtt_client_init(&mqtt_cfg);

    esp_mqtt_client_register_event(client, ESP_EVENT_ANY_ID, mqtt_event_handler, NULL);
    esp_mqtt_client_start(client);
}

static void wifi_event_handler(void* arg, esp_event_base_t event_base, int32_t event_id, void* event_data)
{
    if (event_id == WIFI_EVENT_STA_START) {
        esp_wifi_connect();

    } else if (event_id == WIFI_EVENT_STA_DISCONNECTED) {
        esp_wifi_connect();
        ESP_LOGI(TAG, "Retrying Wi-Fi connection...");

    } else if (event_id == IP_EVENT_STA_GOT_IP) {
        ESP_LOGI(TAG, "Wi-Fi connected!");
        mqtt_app_start(); // Start MQTT after Wi-Fi is connected
    }
}

void wifi_init_sta(void)
{
    esp_netif_init();
    esp_event_loop_create_default();
    esp_netif_t *netif = esp_netif_create_default_wifi_sta();
    assert(netif);

    wifi_init_config_t cfg = WIFI_INIT_CONFIG_DEFAULT();
    esp_wifi_init(&cfg);

    // Register Wi-Fi event handler
    esp_event_handler_instance_t instance_any_id;
    esp_event_handler_instance_t instance_got_ip;
    esp_event_handler_instance_register(WIFI_EVENT,
                                        ESP_EVENT_ANY_ID,
                                        &wifi_event_handler,
                                        NULL,
                                        &instance_any_id);
    esp_event_handler_instance_register(IP_EVENT,
                                        IP_EVENT_STA_GOT_IP,
                                        &wifi_event_handler,
                                        NULL,
                                        &instance_got_ip);

    wifi_config_t wifi_config = {
        .sta = {
            .ssid = WIFI_SSID,
            .password = WIFI_PASS,
            .threshold.authmode = WIFI_AUTH_WPA2_PSK,
        },
    };

    esp_wifi_set_mode(WIFI_MODE_STA);
    esp_wifi_set_config(WIFI_IF_STA, &wifi_config);
    esp_wifi_start();
}

void app_main(void)
{
    // Initialize NVS (Non-Volatile Storage)
    esp_err_t ret = nvs_flash_init();
    if (ret == ESP_ERR_NVS_NO_FREE_PAGES || ret == ESP_ERR_NVS_NEW_VERSION_FOUND) {
        // NVS partition was truncated, erase and retry
        ESP_ERROR_CHECK(nvs_flash_erase());
        ret = nvs_flash_init();
    }
    ESP_ERROR_CHECK(ret);

    // Initialize Wi-Fi
    wifi_init_sta();
}
