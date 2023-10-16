import socket
import threading

# Constants
LISTEN_IP = 'localhost'
GROUND_TCP_PORT = 12348
GROUND_UDP_PORT = 12349
TUNNEL_PORT = 12347

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

def handle_tcp_tunnel(tunnel_sock):
    ground_sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    ground_sock.connect((LISTEN_IP, GROUND_TCP_PORT))
    threading.Thread(target=forward_data, args=(tunnel_sock, ground_sock)).start()
    threading.Thread(target=forward_data, args=(ground_sock, tunnel_sock)).start()

def tcp_proxy():
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as server_sock:
        server_sock.bind((LISTEN_IP, TUNNEL_PORT))
        server_sock.listen(5)
        while True:
            tunnel_sock, _ = server_sock.accept()
            threading.Thread(target=handle_tcp_tunnel, args=(tunnel_sock,)).start()

def udp_proxy():
    with socket.socket(socket.AF_INET, socket.SOCK_DGRAM) as server_sock:
        server_sock.bind((LISTEN_IP, TUNNEL_PORT))
        while True:
            data, proxy1_address = server_sock.recvfrom(4096)
            if data:
                ground_sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
                ground_sock.sendto(data, (LISTEN_IP, GROUND_UDP_PORT))

if __name__ == "__main__":
    threading.Thread(target=tcp_proxy).start()
    threading.Thread(target=udp_proxy).start()
