import threading
import time
from typing import Callable


class Timer:
    def __init__(self, interval: int, action: Callable):
        self.__interval = interval
        self.__action = action
        self.__stop_event = threading.Event()
        self.__thread = threading.Thread(target=self.__mechanism)

    def is_running(self):
        return not self.__stop_event.is_set()

    def __mechanism(self):
        while not self.__stop_event.wait(timeout=self.__interval):
            self.__action()
            break
        self.__stop_event.set()

    def start(self):
        self.__thread.start()

    def cancel(self):
        self.__stop_event.set()
