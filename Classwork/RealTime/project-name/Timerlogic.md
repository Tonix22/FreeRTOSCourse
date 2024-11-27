# Logic for Master-Slave Trigger System

## Overview
The system consists of one master (server) and multiple slaves (clients). The master sends a future timestamp \( T+N \) to the slaves using Wi-Fi sockets. The slaves schedule their operations to execute precisely at \( T+N \) using high-resolution timers.

---

## Master Logic
1. **Obtain Current Time:**
   - Use `esp_timer_get_time()` to get the current time since boot in microseconds.

2. **Calculate Trigger Time:**
   - Add the desired offset \( N \) to the current time to compute the trigger time \( T+N \).

3. **Send Trigger Time to Slaves:**
   - Use UDP sockets to broadcast \( T+N \) to all connected slaves.
   - Each message contains the computed \( T+N \) as a string.

4. **Handle Communication Errors:**
   - Retry or log errors if the message fails to send.

---

## Slave Logic
1. **Initialize UDP Listener:**
   - Bind a UDP socket to listen for trigger messages from the master.

2. **Receive Trigger Time:**
   - Parse the \( T+N \) timestamp received from the master.

3. **Calculate Delay:**
   - Use `esp_timer_get_time()` to get the current time.
   - Compute the remaining time until \( T+N \) by subtracting the current time from \( T+N \).

4. **Schedule Timer:**
   - If the remaining time is positive, use `esp_timer_start_once()` to schedule the task.
   - If the remaining time is negative, log an error or handle missed timing.

5. **Execute Task:**
   - When the timer triggers, execute the task (e.g., toggling GPIO, starting a sequence).

---

## Pseudo-Code

### Master
```plaintext
function master_trigger_signal():
    current_time = get_current_time()  # Get current time in microseconds
    trigger_time = current_time + OFFSET  # Compute T+N

    for slave in slave_addresses:
        send_udp_message(slave, trigger_time)  # Send T+N to each slave
```

### Slave
```plaintext
function slave_wait_for_trigger():
    trigger_time = receive_udp_message()  # Receive T+N from master
    current_time = get_current_time()  # Get current time
    delay = trigger_time - current_time  # Calculate delay

    if delay > 0:
        set_timer(delay, task_to_execute)  # Schedule task at T+N
    else:
        log_error("Missed trigger time!")
```