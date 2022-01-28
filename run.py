from subprocess import Popen
from Interfaces import client_interface
from sys import executable
from time import sleep


if __name__ == "__main__":
    client_interface_process: Popen
    try:
        client_interface_process = Popen([executable, client_interface.__file__])
        sleep(1)
        input()
    except KeyboardInterrupt:
        print("keyboard interrupt")
        client_interface_process.kill()
    else:
        client_interface_process.kill()

