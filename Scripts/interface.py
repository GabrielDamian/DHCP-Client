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

        self.logging_data_state = 'disabled'
        self.host_name = StringVar()
        self.address_request = StringVar()
        self.client_id = StringVar()
        self.hardware_address = StringVar()
        self.client_ip_address = StringVar()
        self.subnet_mask = BooleanVar()
        self.router = BooleanVar()
        self.domain_server = BooleanVar()
        self.broadcast_address = BooleanVar()
        self.lease_time = BooleanVar()
        self.renewal_time = BooleanVar()
        self.subnet_mask_option = StringVar()
        self.router_option = StringVar()
        self.domain_server_option = StringVar()
        self.broadcast_address_option = StringVar()
        self.lease_time_option = StringVar()
        self.renewal_time_option = StringVar()
        self.logging_data = StringVar()
        self.lease_time_value = IntVar()
        self.renewal_time_value = IntVar()
        self.clock_value = StringVar()
        self.ip_curent_value = StringVar()

        self.subnet_mask_option.set('...')
        self.router_option.set('...')
        self.domain_server_option.set('...')
        self.broadcast_address_option.set('...')
        self.lease_time_option.set('...')
        self.renewal_time_option.set('...')
        self.ip_curent_value.set("None")
        self.lease_time_value.set(0)
        self.renewal_time_value.set(0)

        self.buton_connect = Button(self.window, text="CONNECT",
                                    command=lambda: threading.Thread(target=self.connect, args=()).start())
        self.buton_generare_default = Button(self.window, text="GEN. DEFAULT",
                                        command=lambda: threading.Thread(target=self.generate_default, args=()).start())
        self.buton_deconectare = Button(self.window, text="DISCONNECT",
                                        command=lambda: threading.Thread(target=self.disconnect, args=()).start())

        self.check_box_subnet_mask = Checkbutton(self.window, text='Subnet Mask', variable=self.subnet_mask, onvalue=1, offvalue=0)
        self.check_box_router = Checkbutton(self.window, text='Router', variable=self.router, onvalue=1, offvalue=0)
        self.check_box_domain_server = Checkbutton(self.window, text='Domain Server', variable=self.domain_server, onvalue=1,
                                              offvalue=0)
        self.check_box_broadcast_address = Checkbutton(self.window, text='Broadcast address', variable=self.broadcast_address,
                                                  onvalue=1, offvalue=0)
        self.check_box_lease_time = Checkbutton(self.window, text='Lease Time', variable=self.lease_time, onvalue=1, offvalue=0)
        self.check_box_renewal_time = Checkbutton(self.window, text='Renewal Time', variable=self.renewal_time, onvalue=1, offvalue=0)

        self.label_host_name = Label(self.window, text="HOST NAME", font=("Arial", 8))
        self.label_address_request = Label(self.window, text="ADDRESS REQUEST", font=("Arial", 8))
        self.label_client_id = Label(self.window, text="CLIENT ID", font=("Arial", 8))
        self.label_client_hardware_address = Label(self.window, text="MAC", font=("Arial", 8))
        self.label_client_ip_address = Label(self.window, text="CLIENT IP ADDRESS", font=("Arial", 8))
        self.label_subnet_mask = Label(self.window, textvariable=self.subnet_mask_option)
        self.label_router = Label(self.window, textvariable=self.router_option)
        self.label_domain_server_option = Label(self.window, textvariable=self.domain_server_option)
        self.label_broadcast_address_option = Label(self.window, textvariable=self.broadcast_address_option)
        self.label_lease_time_option = Label(self.window, textvariable=self.lease_time_option)
        self.label_renewal_time_option = Label(self.window, textvariable=self.renewal_time_option)
        self.label_logging = Label(self.window, text="Logging", font=("Arial", 10))
        self.label_separator_footer = Label(self.window, text="_" * 122, font=("Arial", 8))
        self.label_lease_time_value = Label(self.window, textvariable=self.lease_time_value)
        self.label_lease_time = Label(self.window, text="Lease time:")
        self.label_renewal_time_value = Label(self.window, textvariable=self.renewal_time_value)
        self.label_renewal_time = Label(self.window, text="Renewal time:")
        self.label_clock = Label(self.window, textvariable=self.clock_value)
        self.label_renew_date = Label(self.window, text="Renew date: ")
        self.label_istoric_ips = Label(self.window, text="Istoric ip-uri:")
        self.label_ip_curent = Label(text="Ip curent:")
        self.label_ip_curent_value = Label(self.window, textvariable=self.ip_curent_value)

        self.input_host_name = Entry(self.window, textvariable=self.host_name, font=('calibre', 10, 'normal'))
        self.input_address_request = Entry(self.window, textvariable=self.address_request, font=('calibre', 10, 'normal'))
        self.input_client_id = Entry(self.window, textvariable=self.client_id, font=('calibre', 10, 'normal'))
        self.input_client_hardware_address = Entry(self.window, textvariable=self.hardware_address, font=('calibre', 10, 'normal'))
        self.input_client_ip_address = Entry(self.window, textvariable=self.client_ip_address, font=('calibre', 10, 'normal'))

        self.text_logging = Text(self.window, height=30, width=49, state=self.logging_data_state)
        self.text_istoric_ips = Text(self.window, height=3, width=49)

    def set_widgets(self):
        self.buton_connect.place(x=20, y=20)
        self.buton_generare_default.place(x=100, y=20)
        self.buton_deconectare.place(x=203, y=20)

        self.check_box_subnet_mask.place(x=20, y=280)
        self.check_box_router.place(x=20, y=320)
        self.check_box_domain_server.place(x=20, y=360)
        self.check_box_broadcast_address.place(x=20, y=400)
        self.check_box_lease_time.place(x=20, y=440)
        self.check_box_renewal_time.place(x=20, y=480)

        self.label_host_name.place(x=20, y=70)
        self.label_address_request.place(x=20, y=110)
        self.label_client_id.place(x=20, y=150)
        self.label_client_hardware_address.place(x=20, y=190)
        self.label_client_ip_address.place(x=20, y=230)
        self.label_subnet_mask.place(x=150, y=280)
        self.label_router.place(x=150, y=320)
        self.label_domain_server_option.place(x=150, y=360)
        self.label_broadcast_address_option.place(x=150, y=400)
        self.label_lease_time_option.place(x=150, y=440)
        self.label_renewal_time_option.place(x=150, y=480)
        self.label_logging.place(x=400, y=46)
        self.label_separator_footer.place(x=20, y=570)
        self.label_lease_time_value.place(x=90, y=600)
        self.label_lease_time.place(x=20, y=600)
        self.label_renewal_time_value.place(x=106, y=631)
        self.label_renewal_time.place(x=20, y=630)
        self.label_clock.place(x=197, y=661)
        self.label_renew_date.place(x=20, y=660)
        self.label_ip_curent.place(x=400, y=690)
        self.label_ip_curent_value.place(x=453, y=690)
        self.label_istoric_ips.place(x=400, y=600)

        self.input_host_name.place(x=150, y=70, width=180, height=20)
        self.input_address_request.place(x=150, y=110, width=180, height=20)
        self.input_client_id.place(x=150, y=150, width=180, height=20)
        self.input_client_hardware_address.place(x=150, y=190, width=180, height=20)
        self.input_client_ip_address.place(x=150, y=230, width=180, height=20)

        self.text_logging.place(x=400, y=70)
        self.text_istoric_ips.place(x=400, y=630)

    def create_button(self, text: str, command: Callable, x_position: int, y_position: int) -> Button:
        button = Button(self.window, text=text, command=command)
        button.place(x=x_position, y=y_position)
        return button

    def create_entry(self, variable_type: Callable, x_position: int, y_position: int, width: int,
                     height: int, font: tuple = ('calibre', 10, 'normal')) -> (Entry, Variable):
        variable = variable_type()
        entry = Entry(self.window, textvariable=variable, font=font)
        entry.place(x=x_position, y=y_position, width=width, height=height)
        return entry, variable

    def create_label(self, x_pos: int, y_pos: int, text: str = None, variable_type=None) -> (Entry, Optional[Variable]):
        label: Label
        if variable_type:
            variable = variable_type()
            label = Label(self.window, textvariable=variable)
            label.place(x=x_pos, y=y_pos)
            return label, variable
        elif text:
            label = Label(self.window, text=text)
            label.place(x=x_pos, y=y_pos)
            return label

    def create_text(self, height: int, width: int, x_pos: int, y_pos: int, with_state: bool = False) -> (Text, Optional[str]):
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
        self.set_widgets()
        self.window.mainloop()


if __name__ == "__main__":
    app = Interface()
    app.start()