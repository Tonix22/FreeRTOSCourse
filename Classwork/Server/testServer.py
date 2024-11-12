import socket

# ESP32 server IP address and port (replace with your ESP32 IP)
ESP32_IP = '192.168.224.209'  # Replace with the IP address of your ESP32
ESP32_PORT = 12345

def chat_with_esp():
    # Create a TCP/IP socket
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client_socket.connect((ESP32_IP, ESP32_PORT))
    print(f"Connected to ESP32 server at {ESP32_IP}:{ESP32_PORT}")
    
    try:
        while True:
            # Get user input and send it to the server
            message = input("Enter message to send to ESP32 (or 'exit' to quit): ")
            if message.lower() == 'exit':
                print("Exiting chat.")
                break
            
            # Send the message to the ESP32
            client_socket.sendall(message.encode())
            
            # Receive and print the server's response
            response = client_socket.recv(1024).decode()
            print(f"ESP32 replied: {response}")

    except KeyboardInterrupt:
        print("Chat interrupted.")
    finally:
        # Close the socket
        client_socket.close()
        print("Connection closed.")

if __name__ == "__main__":
    chat_with_esp()
