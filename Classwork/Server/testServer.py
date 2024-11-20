import socket
from zeroconf import ServiceBrowser, Zeroconf
import threading

# Define the service type your ESP32 is advertising
SERVICE_TYPE = "_espchat._tcp.local."

class MyListener:

    def __init__(self):
        self.server_ip = None
        self.server_port = None
        self.event = threading.Event()

    def remove_service(self, zeroconf, type, name):
        pass  # Not handling service removal

    def add_service(self, zeroconf, type, name):
        info = zeroconf.get_service_info(type, name)
        if info:
            # Decode the service name
            service_name = info.name
            if "ESP32_TCP_Server" in service_name:
                # Extract IP address and port
                addr = socket.inet_ntoa(info.addresses[0])
                port = info.port
                print(f"Found ESP32 server at {addr}:{port}")
                self.server_ip = addr
                self.server_port = port
                self.event.set()  # Signal that we have found the service

def chat_with_esp(ip, port):
    # Create a TCP/IP socket
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client_socket.connect((ip, port))
    print(f"Connected to ESP32 server at {ip}:{port}")
    
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
    except Exception as e:
        print(f"An error occurred: {e}")
    finally:
        # Close the socket
        client_socket.close()
        print("Connection closed.")

def find_esp32_service():
    zeroconf = Zeroconf()
    listener = MyListener()
    browser = ServiceBrowser(zeroconf, SERVICE_TYPE, listener)

    print("Searching for ESP32 service...")

    # Wait until the service is found or timeout after 10 seconds
    if listener.event.wait(timeout=10):
        # Service found
        zeroconf.close()
        return listener.server_ip, listener.server_port
    else:
        # Service not found
        zeroconf.close()
        print("ESP32 service not found.")
        return None, None

if __name__ == "__main__":
    ip, port = find_esp32_service()
    if ip and port:
        chat_with_esp(ip, port)
    else:
        print("Could not find ESP32 server via mDNS.")
