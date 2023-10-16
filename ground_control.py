import json
import socket

# Create a socket object
server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

# Set the IP address and port number to listen on
host = "localhost"  # You can change this to a specific IP address or use "0.0.0.0" for all available interfaces
port = 12345       # Choose the same port number used in Drone.py

# Bind the socket to the specified address and port
server_socket.bind((host, port))

# Listen for incoming connections (1 is the maximum number of queued connections)
server_socket.listen(1)

print("GroundControl is waiting for a connection...")

while True:
    # Accept a connection from Drone
    client_socket, addr = server_socket.accept()

    print("Connection from:", addr)

    try:
        # Receive the message from Drone
        message = client_socket.recv(1024)

        # Parse the received JSON message
        received_message = json.loads(message.decode('utf-8'))

        # Print the received message
        print("Received message from Drone:", received_message)

        # Send a response back to Drone
        response_message = {"value": "received"}
        response_json = json.dumps(response_message)
        client_socket.send(response_json.encode('utf-8'))

    finally:
        # Close the socket for this connection
        client_socket.close()
