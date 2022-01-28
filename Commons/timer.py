import threading
from typing import Callable


class Timer:
    def __init__(self, interval: int, action: Callable):
        """

        :param interval: The time interval in seconds after which the action will be called
        :param action: The event that happens after the time interval
        """
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
