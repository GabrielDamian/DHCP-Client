from tkinter import Tk, StringVar, END
from Interfaces.base_interface import BaseInterface
from Commons.receivers import Receivers
from threading import Thread
from Interfaces import SERVER_SOCKET, SUBNET_MASKS, NETWORK_SIZES, SERVER_BROADCAST_ADDR
from Dhcp.packet import Packet
import ipaddress
from Dhcp.address_table import AddressTable
from typing import Optional
from Dhcp.message_type import MessageType
from Dhcp.opcodes import Opcodes
from datetime import datetime, timedelta


class ServerInterface(BaseInterface):
    def __init__(self):
        super().__init__()

        self._address_table: Optional[AddressTable] = None

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

        self._subnet_mask_variable.trace_add(mode="write", callback=lambda x, y, z: Thread(target=self._set_new_address_table).start())
        self._network_ip_address_variable.trace_add(mode="write", callback=lambda x, y, z: Thread(target=self._set_new_address_table).start())

    def _start_server(self):
        self._append_to_logging("Listening for discover packets...")
        discover_packet = Receivers.discover_receiver(SERVER_SOCKET, 5)
        if discover_packet is None:
            self._append_to_logging("No response from client.")
            return

        self._append_to_logging("Discover received...")
        unallocated_ip_address = self._address_table.get_unallocated_address()
        discover_packet.your_ip_address = str(unallocated_ip_address)
        discover_packet.subnet_mask = self._address_table.get_subnet_mask()
        discover_packet.router = self._router_variable.get()
        discover_packet.domain_server = self._dns_variable.get()
        discover_packet.lease_time = int(self._lease_time_variable.get())
        discover_packet.renewal_time = int(self._renewal_time_variable.get())
        discover_packet.dhcp_message_type = MessageType.OFFER
        discover_packet.opcode = Opcodes.REPLY

        self._append_to_logging("Sending offer...")
        SERVER_SOCKET.sendto(discover_packet.encode(), SERVER_BROADCAST_ADDR)
        request_packet = Receivers.request_receiver(SERVER_SOCKET, timeout=5)
        if request_packet is None:
            self._append_to_logging("No response from client.")
            return

        self._append_to_logging("Request received...")
        request_packet.your_ip_address = str(unallocated_ip_address)
        request_packet.dhcp_message_type = MessageType.ACK
        request_packet.opcode = Opcodes.REPLY

        self._append_to_logging("Sending ack...")
        SERVER_SOCKET.sendto(request_packet.encode(), SERVER_BROADCAST_ADDR)

        self._address_table.give_address(unallocated_ip_address, request_packet.client_hardware_address,
                                         request_packet.client_id, datetime.now() + timedelta(seconds=int(self._lease_time_variable.get())))

        self._update_address_pool_view()

    def _stop_server(self):
        self._append_to_logging("Stopping...")

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

    def _set_new_address_table(self):
        try:
            ip = f'{self._network_ip_address_variable.get()}{self._subnet_mask_variable.get()}'
            network_ip = ipaddress.ip_network(address=ip, strict=False)
            self._address_table = AddressTable(network_ip)
        except Exception as ex:
            return

    def _update_address_pool_view(self):
        """Updates the address pool view with the current inputs"""
        self._address_pool_view_text.config(state='normal')
        self._address_pool_view_text.delete('1.0', END)
        self._address_pool_view_text.insert(END, f" {str(self._address_table)}\n")
        self._address_pool_view_text.config(state='disabled')


if __name__ == "__main__":
    ServerInterface().start()
