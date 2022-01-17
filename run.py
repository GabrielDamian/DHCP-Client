from subprocess import Popen
from Scripts import interface, server_test
from sys import executable
from time import sleep


if __name__ == "__main__":
    interface_process: Popen
    #server_process: Popen

    try:
        interface_process = Popen([executable, interface.__file__])
        #server_process = Popen([executable, server_test.__file__])
        sleep(1)
        input()
    except KeyboardInterrupt:
        print("keyboard interrupt")
        interface_process.kill()
        #server_process.kill()
    else:
        interface_process.kill()
        #server_process.kill()
