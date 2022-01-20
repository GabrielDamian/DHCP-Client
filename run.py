from subprocess import Popen
from Scripts import interface
from sys import executable
from time import sleep


if __name__ == "__main__":
    interface_process: Popen
    try:
        interface_process = Popen([executable, interface.__file__])
        sleep(1)
        input()
    except KeyboardInterrupt:
        print("keyboard interrupt")
        interface_process.kill()
    else:
        interface_process.kill()

