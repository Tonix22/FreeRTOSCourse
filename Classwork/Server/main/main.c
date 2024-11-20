#include <stdio.h>
#include <string.h>
#include <sys/param.h>
#include "freertos/FreeRTOS.h"
#include "freertos/task.h"
#include "esp_system.h"
#include "esp_log.h"
#include "nvs_flash.h"
#include "esp_netif.h"
#include "esp_event.h"
#include "esp_wifi.h"
#include "lwip/sockets.h"
#include "lwip/netdb.h"

#include "sdkconfig.h"
#include "mdns.h"  // Include mDNS header

//#define WIFI_SSID "Tonix"
//#define WIFI_PASS "typewriter"
#define WIFI_SSID CONFIG_WIFI_SSID
#define WIFI_PASS CONFIG_WIFI_PASSWORD
#define PORT 12345  // Server port

static const char *TAG = "ESP32_CHAT_SERVER";

// Forward declaration of tcp_server_task
static void tcp_server_task(void *pvParameters);

// Wi-Fi event handler function
static void wifi_event_handler(void* arg, esp_event_base_t event_base,
                               int32_t event_id, void* event_data) {
    if (event_base == WIFI_EVENT) {
        switch(event_id) {
            case WIFI_EVENT_STA_START:
                esp_wifi_connect();
                ESP_LOGI(TAG, "Connecting to Wi-Fi...");
                break;
            case WIFI_EVENT_STA_DISCONNECTED:
                ESP_LOGI(TAG, "Disconnected from Wi-Fi");
                esp_wifi_connect();
                ESP_LOGI(TAG, "Retrying connection...");
                break;
            default:
                break;
        }
    } else if (event_base == IP_EVENT) {
        switch(event_id) {
            case IP_EVENT_STA_GOT_IP:
                ip_event_got_ip_t* event = (ip_event_got_ip_t*) event_data;
                ESP_LOGI(TAG, "Got IP Address: " IPSTR, IP2STR(&event->ip_info.ip));

                // Initialize mDNS
                ESP_ERROR_CHECK(mdns_init());
                ESP_ERROR_CHECK(mdns_hostname_set("esp32-device"));  // Set your desired hostname
                ESP_ERROR_CHECK(mdns_instance_name_set("ESP32 Chat Server"));

                // Add a TCP service to advertise
                ESP_ERROR_CHECK(mdns_service_add("ESP32_TCP_Server", "_tcp", "_local", PORT, NULL, 0));

                // Add a TCP service to advertise with a specific service type
                ESP_ERROR_CHECK(mdns_service_add("ESP32_TCP_Server", "_espchat", "_tcp", PORT, NULL, 0));

                // Start the TCP server after initializing mDNS
                xTaskCreate(tcp_server_task, "tcp_server", 4096, NULL, 5, NULL);
                break;
            default:
                break;
        }
    }
}

static void wifi_init(void) {
    // Initialize network interface
    esp_netif_init();
    // Create default event loop
    esp_event_loop_create_default();
    // Create default Wi-Fi station
    esp_netif_create_default_wifi_sta();
    // Initialize Wi-Fi with default configurations
    wifi_init_config_t cfg = WIFI_INIT_CONFIG_DEFAULT();
    esp_wifi_init(&cfg);

    // Register event handler for Wi-Fi and IP events
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

    // Configure Wi-Fi connection settings
    wifi_config_t wifi_config = {
        .sta = {
            .ssid = WIFI_SSID,
            .password = WIFI_PASS,
            // Adjust authmode if necessary
            .threshold.authmode = WIFI_AUTH_WPA2_PSK,
            // Optional: PMF settings
            .pmf_cfg = {
                .capable = true,
                .required = false
            },
        },
    };

    // Set Wi-Fi mode to station
    esp_wifi_set_mode(WIFI_MODE_STA);
    // Apply the Wi-Fi configuration
    esp_wifi_set_config(WIFI_IF_STA, &wifi_config);
    // Start Wi-Fi
    esp_wifi_start();
}

static void tcp_server_task(void *pvParameters) {
    char addr_str[128];
    int addr_family = AF_INET;
    int ip_protocol = IPPROTO_IP;
    struct sockaddr_in dest_addr;
    
    dest_addr.sin_addr.s_addr = htonl(INADDR_ANY);
    dest_addr.sin_family = AF_INET;
    dest_addr.sin_port = htons(PORT);
    
    int listen_sock = socket(addr_family, SOCK_STREAM, ip_protocol);
    if (listen_sock < 0) {
        ESP_LOGE(TAG, "Unable to create socket: errno %d", errno);
        vTaskDelete(NULL);
        return;
    }
    bind(listen_sock, (struct sockaddr *)&dest_addr, sizeof(dest_addr));
    listen(listen_sock, 1);

    while (1) {
        ESP_LOGI(TAG, "Waiting for client to connect...");
        struct sockaddr_in source_addr;
        socklen_t addr_len = sizeof(source_addr);
        int sock = accept(listen_sock, (struct sockaddr *)&source_addr, &addr_len);
        
        if (sock < 0) {
            ESP_LOGE(TAG, "Unable to accept connection: errno %d", errno);
            continue;
        }
        
        inet_ntoa_r(source_addr.sin_addr, addr_str, sizeof(addr_str) - 1);
        ESP_LOGI(TAG, "Client connected from %s", addr_str);
        
        char rx_buffer[128];
        while (1) {
            int len = recv(sock, rx_buffer, sizeof(rx_buffer) - 1, 0);
            if (len < 0) {
                ESP_LOGE(TAG, "Receive failed: errno %d", errno);
                break;
            } else if (len == 0) {
                ESP_LOGI(TAG, "Connection closed");
                break;
            } else {
                rx_buffer[len] = '\0';  // Null-terminate the received data
                ESP_LOGI(TAG, "Received: %s", rx_buffer);

                // Send the received message back to client
                send(sock, rx_buffer, len, 0);
            }
        }

        close(sock);
        ESP_LOGI(TAG, "Client disconnected");
    }
    vTaskDelete(NULL);
}

void app_main(void) {
    // Initialize NVS (Non-Volatile Storage)
    esp_err_t ret = nvs_flash_init();
    if (ret == ESP_ERR_NVS_NO_FREE_PAGES ||
        ret == ESP_ERR_NVS_NEW_VERSION_FOUND) {
        // Erase NVS if necessary and retry
        ESP_ERROR_CHECK(nvs_flash_erase());
        ret = nvs_flash_init();
    }
    ESP_ERROR_CHECK(ret);

    // Initialize Wi-Fi
    wifi_init();

    // Note: Do not start tcp_server_task here; it will start after getting IP
}
