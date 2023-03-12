import socketserver
import sys

from lsm_tree import LSMTree
import click

file_directory = sys.path[0]
path = file_directory + '/segments/'
engine = LSMTree('test_file-1', path, 'bkup')


class MyTCPRequestHandler(socketserver.StreamRequestHandler):
    def handle(self):
        while True:
            print("Recieved one request from {}".format(self.client_address[0]))
            msg = self.rfile.readline().strip().decode()
            if not msg:
                break

            command, *args = msg.split(" ")
            if command.lower() == "getall":
                result = []
                for arg in args:
                    value = engine.db_get(arg)
                    if value is not None:
                        result.append(value.encode())
                    else:
                        result.append("null".encode())
                self.wfile.write("^".join(result.encode()))
            if command.lower() == "get":
                value = engine.db_get(args[0])
                if value is not None:
                    self.wfile.write(value.encode())
                else:
                    self.wfile.write(f"ERROR: Key {args[0]} does not exist!".encode())
            elif command.lower() == "set":
                key, value = args
                engine.db_set(key, value)
                self.wfile.write(f"Wrote {key}={value}".encode())
            elif command.lower() == "ping":
                self.wfile.write("Pong!".encode())
            else:
                self.wfile.write(f"Unknown command".encode())


@click.option("--address", "-a", default="127.0.0.1")
@click.option("--port", "-p", default=8080)
@click.command()
def start_server(address: str, port: int):
    db_server = socketserver.TCPServer((address, port), MyTCPRequestHandler)
    print("Starting DB Server")
    try:
        db_server.serve_forever()
    except KeyboardInterrupt:
        print("Backing up metadata...")
        engine.flush_memtable_to_disk(engine.current_segment_path())
        engine.save_metadata()


if __name__ == "__main__":
    start_server()
