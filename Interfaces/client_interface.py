from tkinter import StringVar
from tkinter import Tk, NORMAL, DISABLED, END
from Dhcp.packet import Packet
from Dhcp.server_options import ServerOptions
from Dhcp.message_type import MessageType
from Dhcp.opcodes import Opcodes
from threading import Thread
from Interfaces import CLIENT_SOCKET, CLIENT_DESTINATIN_ADDR
from Commons.receivers import Receivers
from Commons.timer import Timer
from typing import Optional
from datetime import datetime, timedelta
from Interfaces.base_interface import BaseInterface


class ClientInterface(BaseInterface):
    def __init__(self):
        super().__init__()
        self.__timer: Optional[Timer] = None
        self.__last_request_packet: Optional[Packet] = None
        self.__ip_history_list = []
        self._window = Tk()
        self._window.geometry("830x720")

        self.__connect_button = self._create_button(text="CONNECT", x_position=20, y_position=20,
                                                    command=lambda: Thread(target=self.__connect, args=()).start())
        self._create_button(text="GEN. DEFAULT", x_position=100, y_position=20,
                            command=lambda: Thread(target=self.__generate_default, args=()).start())
        self._create_button(text="DISCONNECT", command=lambda: Thread(target=self.__disconnect, args=()).start(),
                            x_position=203, y_position=20)

        _, self.__subnet_mask_option = self._create_checkbutton(text='Subnet Mask', x_pos=20, y_pos=280)
        _, self.__router_option = self._create_checkbutton(text="Router", x_pos=20, y_pos=320)
        _, self.__domain_server_option = self._create_checkbutton("Domain Server", 20, 360)
        _, self.__broadcast_address_option = self._create_checkbutton("Broadcast Address", 20, 400)
        _, self.__lease_time_option = self._create_checkbutton("Lease Time", 20, 440)
        _, self.__renewal_time_option = self._create_checkbutton("Renewal Time", 20, 480)

        self._create_label(x_pos=20, y_pos=70, text="HOST NAME")
        self._create_label(20, 110, text="ADDRESS REQUEST")
        self._create_label(20, 150, text="CLIENT ID")
        self._create_label(20, 190, text="MAC")
        self._create_label(20, 230, text="CLIENT IP ADDRESS")
        _, self.__subnet_mask_value = self._create_label(150, 280, variable_type=StringVar)
        _, self.__router_value = self._create_label(150, 320, variable_type=StringVar)
        _, self.__domain_server_value = self._create_label(150, 360, variable_type=StringVar)
        _, self.__broadcast_address_value = self._create_label(150, 400, variable_type=StringVar)
        _, self.__lease_time_value = self._create_label(150, 440, variable_type=StringVar)
        _, self.__renewal_time_value = self._create_label(150, 480, variable_type=StringVar)
        self._create_label(400, 46, text="Logging")
        self._create_label(20, 570, text="_" * 122)
        _, self.__renew_datetime_value = self._create_label(150, 650, variable_type=StringVar)
        self._create_label(20, 650, text="Renew date")
        self._create_label(400, 690, text="Current IP")
        _, self.__current_ip_value = self._create_label(453, 690, variable_type=StringVar)
        self._create_label(400, 600, text="Ip history")

        _, self.__host_name_value = self._create_entry(x_position=150, y_position=70, width=180, height=20)
        _, self.__address_request_value = self._create_entry(150, 110, 180, 20)
        _, self.__client_id_value = self._create_entry(150, 150, 180, 20)
        _, self.__hardware_address_value = self._create_entry(150, 190, 180, 20)
        _, self.__client_ip_address_value = self._create_entry(150, 230, 180, 20)

        self.__logging_text, _ = self._create_text(x_pos=400, y_pos=70, height=30, width=49, with_state=True)
        self.__ip_history_text = self._create_text(400, 630, 3, 49)

    def __inputs_to_packet(self) -> Packet:
        """Creates a packet from inputs

        :return: Packet
        """
        server_options = []
        if self.__subnet_mask_option.get():
            server_options.append(ServerOptions(1))
        if self.__router_option.get():
            server_options.append(ServerOptions(3))
        if self.__domain_server_option.get():
            server_options.append(ServerOptions(6))
        if self.__broadcast_address_option.get():
            server_options.append(ServerOptions(28))
        if self.__lease_time_option.get():
            server_options.append(ServerOptions(51))
        if self.__renewal_time_option.get():
            server_options.append(ServerOptions(58))

        new_packet = Packet(packet=None)
        new_packet.server_options = server_options
        new_packet.host_name = self.__host_name_value.get() if self.__host_name_value.get() != 'None' else None
        new_packet.address_request = self.__address_request_value.get() if self.__address_request_value.get() != 'None' else None
        new_packet.client_id = self.__client_id_value.get() if self.__client_id_value.get() != 'None' else None

        mac = self.__hardware_address_value.get()
        if mac != "None":
            new_packet.client_hardware_address = self.__hardware_address_value.get()

        cia = self.__client_ip_address_value.get()
        if cia != "None":
            new_packet.client_ip_address = self.__client_ip_address_value.get()
        return new_packet

    def __append_to_logging(self, text: str):
        """Writes text to logging window

        :param text: Text to be written
        """
        self.__logging_text.config(state='normal')
        self.__logging_text.insert(END, f" {text}\n")
        self.__logging_text.config(state='disabled')

    def __add_ip_in_history(self, ip: str):
        """Adds an ip to the history

        :param ip: Added ip address
        """
        if ip not in self.__ip_history_list:
            self.__ip_history_list.append(ip)
            self.__ip_history_text.config(state=NORMAL)
            self.__ip_history_text.insert(END, f" {ip}\n")
            self.__ip_history_text.config(state=DISABLED)

    def __no_response_from_server(self):
        self.__connect_button["state"] = NORMAL
        self.__append_to_logging("\nNo response from the server.")

    def __set_fields_from_dhcpack(self, packet_ack: Packet):
        """Fills the widgets with the ino from ack pack

        :param packet_ack: packet from which to read
        """
        next_request_datetime = datetime.now() + \
                                timedelta(seconds=packet_ack.renewal_time if packet_ack.renewal_time else
                                          packet_ack.lease_time // 2 if packet_ack.lease_time else "None")

        self.__renew_datetime_value.set(f"{next_request_datetime}")
        self.__subnet_mask_value.set(packet_ack.subnet_mask if packet_ack.subnet_mask else "None")
        self.__router_value.set(packet_ack.router if packet_ack.router else "None")
        self.__domain_server_value.set(packet_ack.domain_server if packet_ack.domain_server else "None")
        self.__broadcast_address_value.set(packet_ack.broadcast_address if packet_ack.broadcast_address else "None")
        self.__lease_time_value.set(packet_ack.lease_time if packet_ack.lease_time else "None")
        self.__renewal_time_value.set(packet_ack.renewal_time if packet_ack.renewal_time else
                                      packet_ack.lease_time//2 if packet_ack.lease_time else "None")
        self.__current_ip_value.set(packet_ack.your_ip_address)

    def __reset_fields(self):
        """Fills widgets with '...'"""
        self.__renew_datetime_value.set("...")
        self.__subnet_mask_value.set("...")
        self.__router_value.set("...")
        self.__domain_server_value.set("...")
        self.__broadcast_address_value.set("...")
        self.__lease_time_value.set("...")
        self.__renewal_time_value.set("...")
        self.__current_ip_value.set("...")

    def __generate_default(self):
        """Fills the inputs with default values"""
        self.__host_name_value.set("None")
        self.__address_request_value.set("None")
        self.__client_id_value.set("None")
        self.__hardware_address_value.set("None")
        self.__client_ip_address_value.set("None")
        self.__subnet_mask_option.set(True)
        self.__router_option.set(True)
        self.__domain_server_option.set(True)
        self.__broadcast_address_option.set(True)
        self.__lease_time_option.set(True)
        self.__renewal_time_option.set(True)

    def __connect(self):
        """Connects to a DHCP Server"""
        self.__connect_button["state"] = DISABLED

        self.__append_to_logging("Initializing DHCPDiscover...")
        packet_discover = self.__inputs_to_packet()
        packet_discover.opcode = Opcodes.REQUEST
        packet_discover.dhcp_message_type = MessageType.DISCOVER

        self.__append_to_logging("Sending DHCPDiscover...")
        CLIENT_SOCKET.sendto(packet_discover.encode(), CLIENT_DESTINATIN_ADDR)

        self.__append_to_logging("Waiting for DHCPOffer...")
        offer_packet = Receivers.offer_receiver(CLIENT_SOCKET)
        if offer_packet is None:
            self.__no_response_from_server()
            return

        self.__append_to_logging("DHCPOffer received...")
        self.__last_request_packet = Packet.make_request_packet(offer_packet=offer_packet)

        self.__append_to_logging("Sending DHCPRequest...")
        CLIENT_SOCKET.sendto(self.__last_request_packet.encode(), CLIENT_DESTINATIN_ADDR)

        self.__append_to_logging("Waiting for DHCPack...")
        packet_ack = Receivers.ack_receiver(CLIENT_SOCKET)
        if packet_ack is None:
            self.__no_response_from_server()
            return

        self.__append_to_logging("DHCPAck received...")
        self.__append_to_logging(str(packet_ack))

        self.__set_fields_from_dhcpack(packet_ack=packet_ack)
        self.__add_ip_in_history(packet_ack.your_ip_address)

        self.__append_to_logging("DHCPACK received...")
        if packet_ack.get_renewal_time():
            self.__timer = Timer(packet_ack.get_renewal_time(), self.__reconnect)
            self.__timer.start()

    def __reconnect(self):
        """Reconnects to the same server"""
        self.__append_to_logging("Sending DHCPRequest for renewal...")
        CLIENT_SOCKET.sendto(self.__last_request_packet.encode(), CLIENT_DESTINATIN_ADDR)

        packet_ack = Receivers.ack_receiver(CLIENT_SOCKET)
        if packet_ack is None:
            self.__no_response_from_server()
            return

        self.__append_to_logging("DHCPACK received...")
        self.__set_fields_from_dhcpack(packet_ack=packet_ack)
        if packet_ack.get_renewal_time():
            self.__timer.cancel()
            self.__timer = Timer(packet_ack.get_renewal_time(), self.__reconnect)
            self.__timer.start()

    def __disconnect(self):
        """Disconnects from the current server"""
        if self.__timer:
            self.__timer.cancel()
        packet_release = self.__last_request_packet
        packet_release.dhcp_message_type = MessageType.RELEASE
        packet_release.opcode = Opcodes.REQUEST
        self.__append_to_logging("Sending DHCPRELEASE...")
        CLIENT_SOCKET.sendto(packet_release.encode(), CLIENT_DESTINATIN_ADDR)
        self.__reset_fields()
        self.__connect_button["state"] = NORMAL


if __name__ == "__main__":
    ClientInterface().start()
