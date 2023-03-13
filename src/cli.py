from concurrent.futures import ThreadPoolExecutor
import datetime
from functools import partial
import random
import click

from client import DbException, LSMDbClient


@click.group()
def cli():
    pass


@click.option("--address", "-a", default="127.0.0.1")
@click.option("--port", "-p", default=8080)
@cli.command()
def repl(address: str, port: int):
    client = LSMDbClient(address, port)
    print(f"Welcome to LSMDB. Connected database at {address}:{port}")
    while True:
        print("> ", end="")
        command, *args = input().split(" ")
        try:
            if command.lower() == "get":
                value = client.get(args[0])
                print(f"{args[0]}={value}")
            elif command.lower() == "diskusage":
                value = client.disk_usage()
                print(value)
            elif command.lower() == "compact":
                value = client.compact()
                print(value)
            elif command.lower() == "flush":
                value = client.flush()
                print(value)
            elif command.lower() == "set":
                if len(args) != 2:
                    print("Invalid args", args)
                else:
                    msg = client.set(args[0], args[1])
                    print(msg)
            elif command.lower() == "ping":
                response = client.ping()
                print(response)
            else:
                print(f"Unknown command {command}!")
        except DbException as dbe:
            print(str(dbe))
        

        
@click.option("--address", "-a", default="127.0.0.1")
@click.option("--port", "-p", default=8080)
@click.option("--nthread", "-n", default=10)
@click.option("--key", "-k", default="test_threading")
@click.option("--unique", "-u", is_flag=True)
@cli.command()
def multiple_thread(address: str, port: int, nthread: int, key: str, unique: bool):
    def _in_thread(address, port, key, unique, thread_id):
        if unique:
            key = key + f"_{thread_id}"
        client = LSMDbClient(address, port)
        # now = datetime.datetime.now().strftime("%Y-%m-%d-%H:%M:%S")
        for i in range(20):
            value = f"value_from_thread_{thread_id}_{i}"
            # value = f"value_from_thread_{thread_id}_{now}"
            client.set(key, value)
            print(f"In thread {thread_id}: wrote {key}={value}")

    with ThreadPoolExecutor(nthread) as p:
        keys = list(range(nthread))
        p.map(partial(_in_thread, address, port, key, unique), keys)
    client = LSMDbClient(address, port)
    client.flush()

if __name__ == "__main__":
    cli()
        