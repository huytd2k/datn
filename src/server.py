import socketserver
import os, sys

from lsm_tree import LSMTree
import click

file_directory = sys.path[0]
path = file_directory + '/segments/'
engine = LSMTree('test_file-1', path, 'bkup')

def get_folder_size(folder_path, exclude):
    total_size = 0
    try:
        # Iterate through all files in the directory
        for dirpath, dirnames, filenames in os.walk(folder_path):
            for file in filenames:
                if file == exclude:
                    continue
                # Get the path of the file
                filepath = os.path.join(dirpath, file)
                # Get the file size and add it to the total size
                total_size += os.path.getsize(filepath)

        # Convert size to bytes, KB, MB or GB as appropriate    
        if total_size < 1024:
            size = str(total_size)+' Bytes'
        elif total_size >= 1024 and total_size < (1024*1024):
            size = str(round(total_size/1024, 2))+' KB'
        elif total_size >= (1024*1024) and total_size < (1024*1024*1024):
            size = str(round(total_size/(1024*1024), 2))+' MB'
        else:
            size = str(round(total_size/(1024*1024*1024), 2))+' GB'

        return size
    except Exception as e:
        print(e)
        return None


class MyTCPRequestHandler(socketserver.StreamRequestHandler):
    def handle(self):
        while True:
            # print("Recieved one request from {}".format(self.client_address[0]))
            msg = self.rfile.readline().strip().decode()
            if not msg:
                break

            command, *args = msg.split(" ")
            if command.lower() == "diskusage":
                size = get_folder_size(engine.segments_directory, engine.wal_basename)
                self.wfile.write(size.encode())
            elif command.lower() == "getall":
                result = []
                for arg in args:
                    value = engine.db_get(arg)
                    if value is not None:
                        result.append(value.encode())
                    else:
                        result.append("null".encode())
                self.wfile.write("^".join(result.encode()))
            elif command.lower() == "get":
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
            elif command.lower() == "flush":
                try:
                    engine.flush_memtable_to_disk(engine.current_segment_path())
                    self.wfile.write("Done flushing".encode())
                except Exception as e:
                    self.wfile.write(f"Error while flushing {str(e)}".encode())
            elif command.lower() == "compact":
                try:
                    engine.compact()
                    self.wfile.write("Done compacting".encode())
                except Exception as e:
                    self.wfile.write(f"Error while compacting {str(e)}".encode())
            else:
                self.wfile.write(f"Unknown command".encode())


@click.option("--address", "-a", default="127.0.0.1")
@click.option("--port", "-p", default=8080)
@click.option("--memtable-threshold", "-t", default=3000)
@click.command()
def start_server(address: str, port: int, memtable_threshold):
    engine.set_threshold(memtable_threshold)
    db_server = socketserver.ThreadingTCPServer((address, port), MyTCPRequestHandler)
    print("Starting DB Server")
    try:
        db_server.serve_forever()
    except KeyboardInterrupt:
        print("Backing up metadata...")
        engine.flush_memtable_to_disk(engine.current_segment_path())
        engine.save_metadata()


if __name__ == "__main__":
    start_server()
