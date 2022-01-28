from tkinter import Tk
from Interfaces.base_interface import BaseInterface
from Commons.receivers import Receivers


class ServerInterface(BaseInterface):
    def __init__(self):
        super().__init__()
        self._window = Tk()
        self._window.geometry("830x720")


if __name__ == "__main__":
    ServerInterface().start()
