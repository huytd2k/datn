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
        

if __name__ == "__main__":
    cli()
        
        