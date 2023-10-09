import json
import socket

# Define the message to be sent
message = {"value": "hello world"}

# Create a socket object
client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

# Set the IP address and port number of the GroundControl
host = "127.0.0.1"  # Change this to the IP address of the GroundControl
port = 12345       # Change this to the port number you want to use

# Connect to the GroundControl
client_socket.connect((host, port))

# Send the message as JSON
message_json = json.dumps(message)
client_socket.send(message_json.encode('utf-8'))

# Receive the response from GroundControl
response = client_socket.recv(1024)

# Print the received response
print("Received response from GroundControl:", response.decode('utf-8'))

# Close the socket
client_socket.close()