import socket
import threading

# Constants
LISTEN_IP = '0.0.0.0'
DRONE_TCP_PORT = 12345
DRONE_UDP_PORT = 12346
PROXY2_IP = 'localhost'  # Change to Proxy2's IP
PROXY2_PORT = 12347  # Tunnel to Proxy2

def forward_data(src_sock, dest_sock):
    try:
        data = src_sock.recv(4096)
        while data:
            dest_sock.send(data)
            data = src_sock.recv(4096)
    except:
        pass
    finally:
        src_sock.close()
        dest_sock.close()

def handle_tcp_client(client_sock, tunnel_sock):
    threading.Thread(target=forward_data, args=(client_sock, tunnel_sock)).start()
    threading.Thread(target=forward_data, args=(tunnel_sock, client_sock)).start()

def tcp_tunnel():
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as server_sock:
        server_sock.bind((LISTEN_IP, DRONE_TCP_PORT))
        server_sock.listen(5)
        while True:
            client_sock, _ = server_sock.accept()
            tunnel_sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            tunnel_sock.connect((PROXY2_IP, PROXY2_PORT))
            threading.Thread(target=handle_tcp_client, args=(client_sock, tunnel_sock)).start()

def udp_tunnel():
    with socket.socket(socket.AF_INET, socket.SOCK_DGRAM) as server_sock:
        server_sock.bind((LISTEN_IP, DRONE_UDP_PORT))
        while True:
            data, drone_address = server_sock.recvfrom(4096)
            if data:
                tunnel_sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
                tunnel_sock.sendto(data, (PROXY2_IP, PROXY2_PORT))

if __name__ == "__main__":
    threading.Thread(target=tcp_tunnel).start()
    threading.Thread(target=udp_tunnel).start()
