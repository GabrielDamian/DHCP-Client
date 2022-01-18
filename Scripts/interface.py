from tkinter import IntVar, StringVar, BooleanVar, Variable
from tkinter import Tk, Button, Entry, Label, Text, Checkbutton, NORMAL, DISABLED, END
from Dhcp.packet import Packet
from Dhcp.server_options import ServerOptions
from Dhcp.message_type import MessageType
from Dhcp.opcodes import Opcodes
import threading
from Scripts import CLIENT_SOCKET, CLIENT_DESTINATIN_ADDR
from Dhcp.receivers import offer_receiver, ack_receiver
from Tools.timer import Timer
from typing import Optional, Callable, Literal
from datetime import datetime, timedelta


class Interface:
    def __init__(self):
        self.timer: Optional[Timer] = None
        self.last_packet_request: Optional[Packet] = None
        self.window = Tk()
        self.window.geometry("830x720")

        self.buton_connect = self.create_button(text="CONNECT",
                                                command=lambda: threading.Thread(target=self.connect, args=()).start(), x_position=20, y_position=20)
        self.buton_generare_default = self.create_button(text="GEN. DEFAULT",
                                                         command=lambda: threading.Thread(target=self.generate_default, args=()).start(), x_position=100, y_position=20)
        self.buton_deconectare = self.create_button(text="DISCONNECT",
                                                    command=lambda: threading.Thread(target=self.disconnect, args=()).start(), x_position=203, y_position=20)

        self.check_box_subnet_mask, self.subnet_mask = self.create_checkbutton(text='Subnet Mask', x_pos=20, y_pos=280)
        self.check_box_router, self.router = self.create_checkbutton(text="Router", x_pos=20, y_pos=320)
        self.check_box_domain_server, self.domain_server = self.create_checkbutton("Domain Server", 20, 360)
        self.check_box_broadcast_address, self.broadcast_address = self.create_checkbutton("Broadcast Address", 20, 400)
        self.check_box_lease_time, self.lease_time = self.create_checkbutton("Lease Time", 20, 440)
        self.check_box_renewal_time, self.renewal_time = self.create_checkbutton("Renewal Time", 20, 480)

        self.label_host_name = self.create_label(x_pos=20, y_pos=70, text="HOST NAME")
        self.label_address_request = self.create_label(20,110,text="ADDRESS REQUEST")
        self.label_client_id = self.create_label(20,150,text="CLIENT ID")
        self.label_client_hardware_address = self.create_label(20,190,text="MAC")
        self.label_client_ip_address = self.create_label(20,230,text="CLIENT IP ADDRESS")
        self.label_subnet_mask, self.subnet_mask_option = self.create_label(150,280,variable_type=StringVar)
        self.label_router, self.router_option = self.create_label(150,320,variable_type=StringVar)
        self.label_domain_server_option, self.domain_server_option = self.create_label(150,360,variable_type=StringVar)
        self.label_broadcast_address_option, self.broadcast_address_option = self.create_label(150,400,variable_type=StringVar)
        self.label_lease_time_option, self.lease_time_option = self.create_label(150,440,variable_type=StringVar)
        self.label_renewal_time_option, self.renewal_time_option = self.create_label(150,480,variable_type=StringVar)
        self.label_logging = self.create_label(400,46,text="Logging")
        self.label_separator_footer = self.create_label(20,570,text="_"*122)
        self.label_lease_time_value, self.lease_time_value = self.create_label(90,600,variable_type=IntVar)
        self.label_lease_time = self.create_label(20,600,text="Lease Time:")
        self.label_renewal_time_value, self.renewal_time_value = self.create_label(106,631,variable_type=IntVar)
        self.label_renewal_time = self.create_label(20,630,text="Renewal time:")
        self.label_clock, self.clock_value = self.create_label(197,661,variable_type=StringVar)
        self.label_renew_date = self.create_label(20,660,text="Renew date")
        self.label_ip_curent = self.create_label(400,690,text="IP curent")
        self.label_ip_curent_value, self.ip_curent_value = self.create_label(453,690, variable_type=StringVar)
        self.label_istoric_ips = self.create_label(400, 600, text="Istoric IP-uri")

        self.input_host_name, self.host_name = self.create_entry(x_position=150, y_position=70, width=180, height=20)
        self.input_address_request, self.address_request = self.create_entry(150,110,180,20)
        self.input_client_id, self.client_id = self.create_entry(150,150,180,20)
        self.input_client_hardware_address, self.hardware_address = self.create_entry(150,190,180,20)
        self.input_client_ip_address, self.client_ip_address = self.create_entry(150,230,180,20)

        self.text_logging, self.logging_data_state = self.create_text(x_pos=400,y_pos=70,height=30,width=49,with_state=True)
        self.text_istoric_ips = self.create_text(400,630,3,49)

    def create_button(self, text: str, command: Callable, x_position: int, y_position: int) -> Button:
        button = Button(self.window, text=text, command=command)
        button.place(x=x_position, y=y_position)
        return button

    def create_entry(self, x_position: int, y_position: int, width: int,
                     height: int, variable_type: Callable = StringVar, font: tuple = ('calibre', 10, 'normal')) -> (Entry, Variable):
        variable = variable_type()
        entry = Entry(self.window, textvariable=variable, font=font)
        entry.place(x=x_position, y=y_position, width=width, height=height)
        return entry, variable

    def create_label(self, x_pos: int, y_pos: int, text: str = None,
                     variable_type=None, font: tuple = ("Arial", 8)) -> (Entry, Optional[Variable]):
        label: Label
        if variable_type:
            variable: Variable = variable_type()
            variable.set("...") if variable_type == StringVar else variable.set(0)
            label = Label(self.window, textvariable=variable, font=font)
            label.place(x=x_pos, y=y_pos)
            return label, variable
        elif text:
            label = Label(self.window, text=text, font=font)
            label.place(x=x_pos, y=y_pos)
            return label

    def create_text(self, x_pos: int, y_pos: int, height: int, width: int, with_state: bool = False) -> (Text, Optional[str]):
        if with_state:
            state = "normal"
            text = Text(self.window, height=height, width=width, state=state)
            text.place(x=x_pos, y=y_pos)
            return text, state
        else:
            text = Text(self.window, height=height, width=width)
            text.place(x=x_pos, y=y_pos)
            return text

    def create_checkbutton(self, text: str, x_pos: int, y_pos: int) -> (Checkbutton, BooleanVar):
        variable = BooleanVar()
        checkbutton = Checkbutton(self.window, text=text, variable=variable, onvalue=1, offvalue=0)
        checkbutton.place(x=x_pos, y=y_pos)
        return Checkbutton, variable

    def inputs_to_packet(self):
        coduri = []

        if self.subnet_mask.get():
            coduri.append(ServerOptions(1))
        if self.router.get():
            coduri.append(ServerOptions(3))
        if self.domain_server.get():
            coduri.append(ServerOptions(6))
        if self.broadcast_address.get():
            coduri.append(ServerOptions(28))
        if self.lease_time.get():
            coduri.append(ServerOptions(51))
        if self.renewal_time.get():
            coduri.append(ServerOptions(58))

        new_packet = Packet(packet=None, requested_options=coduri)
        new_packet.host_name = self.host_name.get() if self.host_name.get() != 'None' else None
        new_packet.address_request = self.address_request.get() if self.address_request.get() != 'None' else None
        new_packet.client_id = self.client_id.get() if self.client_id.get() != 'None' else None
        new_packet.client_hardware_address = self.hardware_address.get() if self.hardware_address.get() != 'None' else None
        new_packet.client_ip_address = self.client_ip_address.get() if self.client_ip_address.get() != 'None' else None
        return new_packet

    def append_to_logging(self, text: str):
        self.text_logging.config(state='normal')
        self.text_logging.insert(END, f" {text}\n")
        self.text_logging.config(state='disabled')

    def no_response_from_server(self):
        self.buton_connect["state"] = NORMAL
        self.append_to_logging("\nNo response from the server.")

    def set_fields_from_dhcpack(self, packet_ack: Packet):
        next_request_datetime = datetime.now() + \
                                timedelta(seconds=packet_ack.renewal_time if packet_ack.renewal_time else
                                packet_ack.lease_time // 2 if packet_ack.lease_time else "None")

        self.clock_value.set(f"{next_request_datetime}")
        self.lease_time_value.set(packet_ack.lease_time if packet_ack.lease_time else "None")
        self.renewal_time_value.set(packet_ack.renewal_time if packet_ack.renewal_time else "None")

        self.subnet_mask_option.set(packet_ack.subnet_mask if packet_ack.subnet_mask else "None")
        self.router_option.set(packet_ack.router if packet_ack.router else "None")
        self.domain_server_option.set(packet_ack.domain_server if packet_ack.domain_server else "None")
        self.broadcast_address_option.set(packet_ack.broadcast_address if packet_ack.broadcast_address else "None")
        self.lease_time_option.set(str(packet_ack.lease_time) if packet_ack.lease_time else "None")
        self.renewal_time_option.set(str(packet_ack.renewal_time) if packet_ack.renewal_time else "None")
        self.ip_curent_value.set(packet_ack.your_ip_address)

    def generate_default(self):
        packet = Packet()

        self.host_name.set(packet.host_name)
        self.address_request.set(packet.address_request)
        self.client_id.set(packet.client_id)
        self.hardware_address.set(packet.client_hardware_address)
        self.client_ip_address.set(packet.client_ip_address)
        self.subnet_mask.set(True)
        self.router.set(False)
        self.domain_server.set(False)
        self.broadcast_address.set(False)
        self.lease_time.set(True)
        self.renewal_time.set(True)

    def connect(self):
        self.buton_connect["state"] = DISABLED

        self.append_to_logging("Initializing DHCPDiscover...")
        packet_discover = self.inputs_to_packet()
        packet_discover.opcode = Opcodes.REQUEST
        packet_discover.dhcp_message_type = MessageType.DISCOVER
        packet_bytes = packet_discover.encode()

        self.append_to_logging("Sending DHCPDiscover...")
        CLIENT_SOCKET.sendto(packet_bytes, CLIENT_DESTINATIN_ADDR)

        self.append_to_logging("Waiting for DHCPOffer...")
        packet_offer = offer_receiver(CLIENT_SOCKET)
        if packet_offer is None:
            self.no_response_from_server()
            return

        self.append_to_logging("DHCPOffer received...")
        packet_offer.make_request()
        self.last_packet_request = packet_offer

        self.append_to_logging("Sending DHCPRequest...")
        CLIENT_SOCKET.sendto(self.last_packet_request.encode(), CLIENT_DESTINATIN_ADDR)

        self.append_to_logging("Waiting for DHCPack...")
        packet_ack = ack_receiver(CLIENT_SOCKET)
        if packet_ack is None:
            self.no_response_from_server()
            return

        self.append_to_logging("DHCPAck received...")
        self.append_to_logging(str(packet_ack))

        self.set_fields_from_dhcpack(packet_ack=packet_ack)

        if packet_ack.get_renewal_time():
            self.timer = Timer(packet_ack.get_renewal_time(), self.reconnect)
            self.timer.start()

    def reconnect(self):
        self.append_to_logging("Sending DHCPRequest for renewal...")
        CLIENT_SOCKET.sendto(self.last_packet_request.encode(), CLIENT_DESTINATIN_ADDR)

        packet_ack = ack_receiver(CLIENT_SOCKET)
        if packet_ack is None:
            self.no_response_from_server()
            return

        self.set_fields_from_dhcpack(packet_ack=packet_ack)
        if packet_ack.get_renewal_time():
            self.timer.cancel()
            self.timer = Timer(packet_ack.get_renewal_time(), self.reconnect)
            self.timer.start()

    def disconnect(self):
        self.timer.cancel()
        packet_relese = self.last_packet_request
        packet_relese.dhcp_message_type = MessageType.RELEASE
        packet_relese.opcode = Opcodes.REQUEST
        CLIENT_SOCKET.sendto(packet_relese.encode(), CLIENT_DESTINATIN_ADDR)
        self.append_to_logging("Resurse eliberate.")
        self.buton_connect["state"] = NORMAL

    def start(self):
        self.window.mainloop()


if __name__ == "__main__":
    app = Interface()
    app.start()
