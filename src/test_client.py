from client import LSMDbClient

client = LSMDbClient("127.0.0.1", 8080)
client.set("foo", "bar")
value = client.get("foo")
print(value)
# import socket

# # Define the host and port of the server
# host = 'localhost'
# port = 8080

# # Connect to the server
# sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
# sock.connect((host, port))

# # Define the set and get functions
# def set(key, value):
#     # Send the "set" command and key-value pair to the server
#     message = f'set {key} {value}\n'
#     sock.sendall(message.encode('utf-8'))
    
#     # Receive the response from the server
#     response = sock.recv(1024).decode('utf-8')
#     print(response)

# def get(key):
#     # Send the "get" command and key to the server
#     message = f'get {key}\n'
#     sock.sendall(message.encode('utf-8'))

#     # Receive the response from the server
#     response = sock.recv(1024).decode('utf-8')
#     print(response)

# # Test the set and get functions
# set('foo', 'bar')
# get('foo')

# # Close the connection
# sock.close()