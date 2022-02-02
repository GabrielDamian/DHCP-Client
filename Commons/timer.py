import threading
from typing import Callable


class Timer:
    def __init__(self, interval: float, action: Callable):
        """
        :param interval: The time interval in seconds after which the action will be called
        :param action: The event that happens after the time interval
        """
        self._interval = interval
        self._action = action
        self._stop_event = threading.Event()
        self._thread = None

    def is_running(self):
        return not self._stop_event.is_set()

    def _mechanism(self):
        while not self._stop_event.wait(timeout=self._interval):
            self._action()
        #     break
        # self.__stop_event.set()

    def start(self):
        self._thread = threading.Thread(target=self._mechanism)
        self._thread.start()

    def cancel(self):
        self._stop_event.set()
