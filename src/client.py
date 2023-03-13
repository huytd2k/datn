import socket

import click


class DbException(Exception):
    pass


class LSMDbClient:
    def __init__(self, server_ip: str, port: int) -> None:
        self.server_ip = server_ip
        self.port = port
        # Create a socket object 
        self.client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.client_socket.connect((server_ip, port))
        
    def get(self, key):
        self.client_socket.sendall(f"GET {key}\n".encode())
        result = self.client_socket.recv(1024).decode()
        if not result.startswith("ERROR:"):
            return result
        else:
            raise DbException(f"Error while getting key {key}: {result[6:]}")

    def getall(self, *keys):
        self.client_socket.sendall(f"GETALL {' '.join(keys)}\n".encode())
        result = self.client_socket.recv(1024).decode()
        if not result.startswith("ERROR:"):
            return result
        else:
            raise DbException(f"Error while getting keys {keys}: {result[6:]}")
    
    def set(self, key, value):
        self.client_socket.sendall(f"SET {key} {value}\n".encode())
        msg = self.client_socket.recv(1024).decode()
        return msg

    def disk_usage(self):
        self.client_socket.sendall("DISKUSAGE\n".encode())
        msg = self.client_socket.recv(1024).decode()
        return msg

    def ping(self):
        self.client_socket.sendall("PING\n".encode())
        msg = self.client_socket.recv(1024).decode()
        return msg

    def compact(self):
        self.client_socket.sendall("COMPACT\n".encode())
        msg = self.client_socket.recv(1024).decode()
        return msg

    def flush(self):
        self.client_socket.sendall("flush\n".encode())
        msg = self.client_socket.recv(1024).decode()
        return msg


@click.group()
def client():
    pass

@click.option("--address", "-a", default="127.0.0.1")
@click.option("--port", "-p", default=8080)
@client.command()
def ping(address, port):
    client = LSMDbClient(address, port)
    print(client.ping())
    

if __name__ == "__main__":
    client()