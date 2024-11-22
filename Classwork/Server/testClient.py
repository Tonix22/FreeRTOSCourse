from zeroconf import ServiceInfo, Zeroconf
import socket
import threading

def start_mdns_service(service_name, service_type, port):
    hostname = socket.gethostname()
    print(hostname)
    ip_address = socket.gethostbyname(hostname)
    addresses = [socket.inet_aton(ip_address)]

    service_info = ServiceInfo(
        type_=service_type,
        name=f"{service_name}.{service_type}",
        addresses=addresses,
        port=port,
        properties={"description": "Socket server service"},
        server=f"{hostname}.local."
    )

    zeroconf = Zeroconf()
    try:
        print(f"Registering mDNS service: {service_name}")
        zeroconf.register_service(service_info)
        return zeroconf, service_info
    except Exception as e:
        print(f"Failed to register mDNS service: {e}")
        zeroconf.close()
        raise

def socket_server(host, port):
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.bind((host, port))
    server_socket.listen(5)
    print(f"Socket server listening on {host}:{port}")

    try:
        while True:
            client_socket, client_address = server_socket.accept()
            print(f"Client connected: {client_address}")
            threading.Thread(target=handle_client, args=(client_socket,)).start()
    except KeyboardInterrupt:
        print("\nShutting down the server...")
    finally:
        server_socket.close()

def handle_client(client_socket):
    try:
        client_socket.sendall(b"Welcome to the socket server!\n")
        while True:
            data = client_socket.recv(1024)
            if not data:
                break
            print(f"Received: {data.decode().strip()}")
            client_socket.sendall(data)
    except ConnectionResetError:
        print("Client disconnected abruptly.")
    finally:
        client_socket.close()
        print("Client connection closed.")

def main():
    service_name = "tonix-laptop"
    service_type = "_espchat._tcp.local."
    port = 12345

    try:
        zeroconf, service_info = start_mdns_service(service_name, service_type, port)
    except Exception as e:
        print(f"Error starting mDNS service: {e}")
        return

    try:
        socket_server("0.0.0.0", port)
    finally:
        print("Unregistering mDNS service...")
        zeroconf.unregister_service(service_info)
        zeroconf.close()

if __name__ == "__main__":
    main()
