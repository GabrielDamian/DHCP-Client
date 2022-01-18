import threading
import time
from typing import Callable


class Timer:
    def __init__(self, interval: int, action: Callable):
        self.interval = interval
        self.action = action
        self.stop_event = threading.Event()
        self.thread = threading.Thread(target=self._mechanism)

    def is_running(self):
        return not self.stop_event.is_set()

    def _mechanism(self):
        while not self.stop_event.wait(timeout=self.interval):
            self.action()
            break
        self.stop_event.set()

    def start(self):
        self.thread.start()

    def cancel(self):
        self.stop_event.set()


if __name__ == "__main__":
    t = Timer(2, lambda: print('s'))
    t.start()
    print(t.is_running())
    time.sleep(3)
    print(t.is_running())