from tkinter import Tk, StringVar, END
from Interfaces.base_interface import BaseInterface
from Commons.receivers import Receivers
from threading import Thread
from Interfaces import SERVER_SOCKET, SUBNET_MASKS, NETWORK_SIZES
from Dhcp.packet import Packet
import ipaddress


class ServerInterface(BaseInterface):
    def __init__(self):
        super().__init__()

        self._network_ip: ipaddress.IPv4Network

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

        self._subnet_mask_variable.trace_add(mode="write", callback=lambda x, y, z: Thread(target=self._update_address_pool_view).start())
        self._network_ip_address_variable.trace_add(mode="write", callback=lambda x, y, z: Thread(target=self._update_address_pool_view).start())

    def _start_server(self):
        self._append_to_logging("Starting...")

        discover_packet = Receivers.discover_receiver(SERVER_SOCKET, 5)
        if discover_packet is None:
            self._append_to_logging("No response from client.")
            return

    def _stop_server(self):
        self._append_to_logging("Stopping...")

    def _generate_default(self):
        self._append_to_logging("Default...")

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
        # IP MAC CLIENT_ID LEASE
        try:
            ip = f'{self._network_ip_address_variable.get()}{self._subnet_mask_variable.get()}'
            self._network_ip = ipaddress.ip_network(address=ip, strict=False)
        except Exception as ex:
            return
        output = "IP       MAC       Client Id       Lease Time"

        self._logging_text.insert(END, f" {output}\n")
        self._address_pool_view_text.config(state='disabled')


if __name__ == "__main__":
    ServerInterface().start()
