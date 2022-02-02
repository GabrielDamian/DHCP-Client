from time import sleep
from tkinter import Tk, StringVar, END
from Interfaces.base_interface import BaseInterface
from Interfaces import SUBNET_MASKS
from typing import Optional
from Backend.server import Server
from Commons.timer import Timer
from threading import Thread
from queue import Queue


class ServerInterface(BaseInterface):
    def __init__(self):
        super().__init__()

        self._server: Optional[Server] = None
        self._logging_queue = Queue()
        self._address_pool_updater = Timer(interval=1/20, action=self._update_address_pool_view)
        self._logging_updater = Timer(interval=1/20, action=self._handle_logging)

        self._window = Tk()
        self._window.geometry("830x720")

        self._create_button(text="START SERVER", command=lambda: Thread(target=self._start_server).start(),
                            x_position=20, y_position=20)
        self._create_button(text="GEN. DEFAULT", command=lambda: Thread(target=self._generate_default).start(),
                            x_position=120, y_position=20)
        self._create_button(text="STOP SERVER", command=lambda: Thread(target=self._stop_server).start(),
                            x_position=220, y_position=20)

        self._create_label(x_pos=20, y_pos=100, text="Server Name:", font=("Arial", 10))
        self._create_label(x_pos=20, y_pos=150, text="Router:", font=("Arial", 10))
        self._create_label(x_pos=20, y_pos=200, text="DNS:", font=("Arial", 10))
        self._create_label(x_pos=20, y_pos=250, text="Lease Time:", font=("Arial", 10))
        self._create_label(x_pos=20, y_pos=300, text="Renewal Time:", font=("Arial", 10))
        self._create_label(x_pos=20, y_pos=350, text="Network Ip Address:", font=("Arial", 10))
        self._create_label(x_pos=20, y_pos=400, text="Subnet Mask:", font=("Arial", 10))
        self._create_label(x_pos=20, y_pos=450, text="Address Pool View:", font=("Arial", 10))
        self._create_label(x_pos=400, y_pos=20, text="Logging:", font=("Arial", 10))

        _, self._server_name_variable = self._create_entry(x_position=160, y_position=100, width=200, height=25, variable_type=StringVar)
        _, self._router_variable = self._create_entry(x_position=160, y_position=150, width=200, height=25, variable_type=StringVar)
        _, self._dns_variable = self._create_entry(x_position=160, y_position=200, width=200, height=25, variable_type=StringVar)
        _, self._lease_time_variable = self._create_entry(x_position=160, y_position=250, width=200, height=25, variable_type=StringVar)
        _, self._renewal_time_variable = self._create_entry(x_position=160, y_position=300, width=200, height=25, variable_type=StringVar)
        _, self._network_ip_address_variable = self._create_entry(x_position=160, y_position=350, width=200, height=25, variable_type=StringVar)
        _, self._subnet_mask_variable = self._create_combobox(options=SUBNET_MASKS, x_pos=160, y_pos=400, width=30)

        self._address_pool_view_text, _ = self._create_text(x_pos=20, y_pos=475, height=14, width=98, with_state=True)
        self._logging_text, _ = self._create_text(x_pos=400, y_pos=100, height=20, width=50, with_state=True)

    def _start_server(self):
        self._append_to_logging("Listening for discover packets...")
        self._server = Server(network_ip_address=self._network_ip_address_variable.get(),
                              mask=self._subnet_mask_variable.get(),
                              router=self._router_variable.get(),
                              dns=self._dns_variable.get(),
                              lease_time=int(self._lease_time_variable.get()),
                              renewal_time=int(self._renewal_time_variable.get()),
                              logging_queue=self._logging_queue)
        self._server.start()
        self._address_pool_updater.start()
        self._logging_updater.start()

    def _stop_server(self):
        self._append_to_logging("Stopping...")
        self._server.stop()
        self._address_pool_updater.cancel()

    def _generate_default(self):
        self._server_name_variable.set("DHCP Server")
        self._router_variable.set('255.25.5.0')
        self._dns_variable.set('0.5.25.255')
        self._lease_time_variable.set('100')
        self._renewal_time_variable.set('50')
        self._network_ip_address_variable.set("20.20.20.20")
        self._subnet_mask_variable.set('/29')

    def _append_to_logging(self, text: str):
        """Writes text to logging window
        :param text: Text to be written
        """
        self._logging_text.config(state='normal')
        self._logging_text.insert(END, f" {text}\n")
        self._logging_text.config(state='disabled')

    def _update_address_pool_view(self):
        """Updates the address pool view with the current inputs"""
        self._address_pool_view_text.config(state='normal')
        self._address_pool_view_text.delete('1.0', END)
        self._address_pool_view_text.insert(END, f" {str(self._server)}\n")
        self._address_pool_view_text.config(state='disabled')

    def _handle_logging(self):
        message = self._logging_queue.get()
        if message:
            self._append_to_logging(message)

    def __del__(self):
        self._address_pool_updater.cancel()
        self._address_pool_updater.cancel()


if __name__ == "__main__":
    ServerInterface().start()
