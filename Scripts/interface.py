from tkinter import IntVar, StringVar, BooleanVar, Variable
from tkinter import Tk, Button, Entry, Label, Text, Checkbutton, NORMAL, DISABLED, END
from Dhcp.packet import Packet
from Dhcp.server_options import ServerOptions
from Dhcp.message_type import MessageType
from Dhcp.opcodes import Opcodes
from threading import Thread
from Scripts import CLIENT_SOCKET, CLIENT_DESTINATIN_ADDR
from Dhcp.receivers import offer_receiver, ack_receiver
from Tools.timer import Timer
from typing import Optional, Callable
from datetime import datetime, timedelta


class Interface:
    def __init__(self):
        self._timer: Optional[Timer] = None
        self.__last_request_packet: Optional[Packet] = None
        self.__window = Tk()
        self.__window.geometry("830x720")

        self.__connect_button = self.__create_button(text="CONNECT",
                                                     command=lambda: Thread(target=self.__connect, args=()).start(),
                                                     x_position=20, y_position=20)
        self.__generate_default_button = self.__create_button(text="GEN. DEFAULT",
                                                              command=lambda: Thread(target=self.__generate_default, args=()).start(),
                                                              x_position=100, y_position=20)
        self.__disconnect_button = self.__create_button(text="DISCONNECT",
                                                        command=lambda: Thread(target=self.__disconnect, args=()).start(), x_position=203,
                                                        y_position=20)

        self.__subnet_mask_checkbox, self.__subnet_mask_option = self.__create_checkbutton(text='Subnet Mask', x_pos=20, y_pos=280)
        self.__router_checkbox, self.__router_option = self.__create_checkbutton(text="Router", x_pos=20, y_pos=320)
        self.__domain_server_checkbox, self.__domain_server_option = self.__create_checkbutton("Domain Server", 20, 360)
        self.__broadcast_address_checkbox, self.__broadcast_address_option = self.__create_checkbutton("Broadcast Address", 20, 400)
        self.__lease_time_checkbox, self.__lease_time_option = self.__create_checkbutton("Lease Time", 20, 440)
        self.__renewal_time_checkbox, self.__renewal_time_option = self.__create_checkbutton("Renewal Time", 20, 480)

        self.__host_name_label = self.__create_label(x_pos=20, y_pos=70, text="HOST NAME")
        self.__address_request_label = self.__create_label(20, 110, text="ADDRESS REQUEST")
        self.__client_id_label = self.__create_label(20, 150, text="CLIENT ID")
        self.__client_hardware_address_label = self.__create_label(20, 190, text="MAC")
        self.__client_ip_address_label = self.__create_label(20, 230, text="CLIENT IP ADDRESS")
        self.__subnet_mask_label, self.__subnet_mask_value = self.__create_label(150, 280, variable_type=StringVar)
        self.__router_label, self.__router_value = self.__create_label(150, 320, variable_type=StringVar)
        self.__domain_server_label, self.__domain_server_value = self.__create_label(150, 360, variable_type=StringVar)
        self.__broadcast_address_label, self.__broadcast_address_value = self.__create_label(150, 400, variable_type=StringVar)
        self.__lease_time_label, self.__lease_time_value = self.__create_label(150, 440, variable_type=StringVar)
        self.__renewal_time_label, self.__renewal_time_value = self.__create_label(150, 480, variable_type=StringVar)
        self.__logging_label = self.__create_label(400, 46, text="Logging")
        self.__separator_footer_label = self.__create_label(20, 570, text="_" * 122)
        self.__next_request_datetime_label, self.__next_request_datetime_value = self.__create_label(197, 661, variable_type=StringVar)
        self.__renew_date_label = self.__create_label(20, 660, text="Renew date")
        self.__current_ip_label = self.__create_label(400, 690, text="IP curent")
        self.__current_ip_value_label, self.ip_curent_value = self.__create_label(453, 690, variable_type=StringVar)
        self.ip_history_label = self.__create_label(400, 600, text="Istoric IP-uri")

        self.__host_name_input, self.__host_name_value = self.__create_entry(x_position=150, y_position=70, width=180, height=20)
        self.__address_request_input, self.__address_request_value = self.__create_entry(150, 110, 180, 20)
        self.__client_id_input, self.__client_id_value = self.__create_entry(150, 150, 180, 20)
        self.__client_hardware_address_input, self.__hardware_address_value = self.__create_entry(150, 190, 180, 20)
        self.__client_ip_address_input, self.__client_ip_address_value = self.__create_entry(150, 230, 180, 20)

        self.__logging_text, self.__logging_text_value = self.__create_text(x_pos=400, y_pos=70, height=30, width=49, with_state=True)
        self.__ip_history_text = self.__create_text(400, 630, 3, 49)

    def __create_button(self, text: str, command: Callable, x_position: int, y_position: int) -> Button:
        button = Button(self.__window, text=text, command=command)
        button.place(x=x_position, y=y_position)
        return button

    def __create_entry(self, x_position: int, y_position: int, width: int,
                       height: int, variable_type: Callable = StringVar, font: tuple = ('calibre', 10, 'normal')) -> (Entry, Variable):
        variable = variable_type()
        entry = Entry(self.__window, textvariable=variable, font=font)
        entry.place(x=x_position, y=y_position, width=width, height=height)
        return entry, variable

    def __create_label(self, x_pos: int, y_pos: int, text: str = None,
                       variable_type=None, font: tuple = ("Arial", 8)) -> (Entry, Optional[Variable]):
        label: Label
        if variable_type:
            variable: Variable = variable_type()
            variable.set("...") if variable_type == StringVar else variable.set(0)
            label = Label(self.__window, textvariable=variable, font=font)
            label.place(x=x_pos, y=y_pos)
            return label, variable
        elif text:
            label = Label(self.__window, text=text, font=font)
            label.place(x=x_pos, y=y_pos)
            return label

    def __create_text(self, x_pos: int, y_pos: int, height: int, width: int, with_state: bool = False) -> (Text, Optional[str]):
        if with_state:
            state = NORMAL
            text = Text(self.__window, height=height, width=width, state=state)
            text.place(x=x_pos, y=y_pos)
            return text, state
        else:
            text = Text(self.__window, height=height, width=width)
            text.place(x=x_pos, y=y_pos)
            return text

    def __create_checkbutton(self, text: str, x_pos: int, y_pos: int) -> (Checkbutton, BooleanVar):
        variable = BooleanVar()
        checkbutton = Checkbutton(self.__window, text=text, variable=variable, onvalue=1, offvalue=0)
        checkbutton.place(x=x_pos, y=y_pos)
        return Checkbutton, variable

    def __inputs_to_packet(self):
        coduri = []

        if self.__subnet_mask_option.get():
            coduri.append(ServerOptions(1))
        if self.__router_option.get():
            coduri.append(ServerOptions(3))
        if self.__domain_server_option.get():
            coduri.append(ServerOptions(6))
        if self.__broadcast_address_option.get():
            coduri.append(ServerOptions(28))
        if self.__lease_time_option.get():
            coduri.append(ServerOptions(51))
        if self.__renewal_time_option.get():
            coduri.append(ServerOptions(58))

        new_packet = Packet(packet=None, requested_options=coduri)
        new_packet.host_name = self.__host_name_value.get() if self.__host_name_value.get() != 'None' else None
        new_packet.address_request = self.__address_request_value.get() if self.__address_request_value.get() != 'None' else None
        new_packet.client_id = self.__client_id_value.get() if self.__client_id_value.get() != 'None' else None
        new_packet.client_hardware_address = self.__hardware_address_value.get() if self.__hardware_address_value.get() != 'None' else None
        new_packet.client_ip_address = self.__client_ip_address_value.get() if self.__client_ip_address_value.get() != 'None' else None
        return new_packet

    def __append_to_logging(self, text: str):
        self.__logging_text.config(state='normal')
        self.__logging_text.insert(END, f" {text}\n")
        self.__logging_text.config(state='disabled')

    def __no_response_from_server(self):
        self.__connect_button["state"] = NORMAL
        self.__append_to_logging("\nNo response from the server.")

    def __set_fields_from_dhcpack(self, packet_ack: Packet):
        next_request_datetime = datetime.now() + \
                                timedelta(seconds=packet_ack.renewal_time if packet_ack.renewal_time else
                                packet_ack.lease_time // 2 if packet_ack.lease_time else "None")

        self.__next_request_datetime_value.set(f"{next_request_datetime}")
        self.__subnet_mask_value.set(packet_ack.subnet_mask if packet_ack.subnet_mask else "None")
        self.__router_value.set(packet_ack.router if packet_ack.router else "None")
        self.__domain_server_value.set(packet_ack.domain_server if packet_ack.domain_server else "None")
        self.__broadcast_address_value.set(packet_ack.broadcast_address if packet_ack.broadcast_address else "None")
        self.__lease_time_value.set(str(packet_ack.lease_time) if packet_ack.lease_time else "None")
        self.__renewal_time_value.set(str(packet_ack.renewal_time) if packet_ack.renewal_time else "None")
        self.ip_curent_value.set(packet_ack.your_ip_address)

    def __generate_default(self):
        packet = Packet()

        self.__host_name_value.set(packet.host_name)
        self.__address_request_value.set(packet.address_request)
        self.__client_id_value.set(packet.client_id)
        self.__hardware_address_value.set(packet.client_hardware_address)
        self.__client_ip_address_value.set(packet.client_ip_address)
        self.__subnet_mask_option.set(True)
        self.__router_option.set(False)
        self.__domain_server_option.set(False)
        self.__broadcast_address_option.set(False)
        self.__lease_time_option.set(True)
        self.__renewal_time_option.set(True)

    def __connect(self):
        self.__connect_button["state"] = DISABLED

        self.__append_to_logging("Initializing DHCPDiscover...")
        packet_discover = self.__inputs_to_packet()
        packet_discover.opcode = Opcodes.REQUEST
        packet_discover.dhcp_message_type = MessageType.DISCOVER
        packet_bytes = packet_discover.encode()

        self.__append_to_logging("Sending DHCPDiscover...")
        CLIENT_SOCKET.sendto(packet_bytes, CLIENT_DESTINATIN_ADDR)

        self.__append_to_logging("Waiting for DHCPOffer...")
        packet_offer = offer_receiver(CLIENT_SOCKET)
        if packet_offer is None:
            self.__no_response_from_server()
            return

        self.__append_to_logging("DHCPOffer received...")
        self.__last_request_packet = Packet.make_request_packet(offer_packet=packet_offer)

        self.__append_to_logging("Sending DHCPRequest...")
        CLIENT_SOCKET.sendto(self.__last_request_packet.encode(), CLIENT_DESTINATIN_ADDR)

        self.__append_to_logging("Waiting for DHCPack...")
        packet_ack = ack_receiver(CLIENT_SOCKET)
        if packet_ack is None:
            self.__no_response_from_server()
            return

        self.__append_to_logging("DHCPAck received...")
        self.__append_to_logging(str(packet_ack))

        self.__set_fields_from_dhcpack(packet_ack=packet_ack)

        if packet_ack.get_renewal_time():
            self._timer = Timer(packet_ack.get_renewal_time(), self.__reconnect)
            self._timer.start()

    def __reconnect(self):
        self.__append_to_logging("Sending DHCPRequest for renewal...")
        CLIENT_SOCKET.sendto(self.__last_request_packet.encode(), CLIENT_DESTINATIN_ADDR)

        packet_ack = ack_receiver(CLIENT_SOCKET)
        if packet_ack is None:
            self.__no_response_from_server()
            return

        self.__set_fields_from_dhcpack(packet_ack=packet_ack)
        if packet_ack.get_renewal_time():
            self._timer.cancel()
            self._timer = Timer(packet_ack.get_renewal_time(), self.__reconnect)
            self._timer.start()

    def __disconnect(self):
        self._timer.cancel()
        packet_relese = self.__last_request_packet
        packet_relese.dhcp_message_type = MessageType.RELEASE
        packet_relese.opcode = Opcodes.REQUEST
        CLIENT_SOCKET.sendto(packet_relese.encode(), CLIENT_DESTINATIN_ADDR)
        self.__append_to_logging("Resurse eliberate.")
        self.__connect_button["state"] = NORMAL

    def start(self):
        self.__window.mainloop()


if __name__ == "__main__":
    app = Interface()
    app.start()
