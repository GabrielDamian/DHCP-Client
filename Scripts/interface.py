import time
from tkinter import IntVar, StringVar, BooleanVar
from tkinter import Tk, Button, Entry, Label, Text, Checkbutton, NORMAL, DISABLED, END
from Dhcp.packet import Packet
from Dhcp.server_options import ServerOptions
from Dhcp.message_type import MessageType
from Dhcp.opcodes import Opcodes
from select import select
from threading import Thread
from Scripts import CLIENT_SOCKET, CLIENT_DESTINATIN_ADDR

# initializare componente
istoric_ipuri = []
current_ip = None


class Clock(Thread):
    all_clocks = []

    @staticmethod
    def stop_all_clocks(clock_variable):
        for clock in Clock.all_clocks:
            clock.stop()
            Clock.all_clocks.remove(clock)

        time.sleep(1)
        clock_variable.set(0)

    def __init__(self, time_variable: IntVar, action ):
        Thread.__init__(self)
        self.action = action
        self.time_variable = time_variable
        self.stop_flag = False

    def run(self):
        self.stop_flag = False
        Clock.all_clocks.append(self)
        while not self.stop_flag and self.time_variable.get() > 0:
            time.sleep(1)
            self.time_variable.set(self.time_variable.get() - 1)

        if self.time_variable.get() <= 0 and (not self.stop_flag):
            self.action()

    def stop(self):
        self.stop_flag = True


class Interface:
    def __init__(self):
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
        self.clock_value = IntVar()
        self.ip_curent_value = StringVar()

        self.subnet_mask_option.set('...')
        self.router_option.set('...')
        self.domain_server_option.set('...')
        self.broadcast_address_option.set('...')
        self.lease_time_option.set('...')
        self.renewal_time_option.set('...')
        self.ip_curent_value.set(0)
        self.lease_time_value.set(0)
        self.renewal_time_value.set(0)

        self.buton_connect = Button(self.window, text="CONNECT", command=lambda: Thread(target=self.connect, args=()).start())
        self.buton_generare_default = Button(self.window, text="GEN. DEFAULT",
                                        command=lambda: Thread(target=self.generate_default, args=()).start())
        self.buton_deconectare = Button(self.window, text="DISCONNECT",
                                   command=lambda: Thread(target=self.disconnect, args=()).start())

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
        self.label_timp_ramas = Label(self.window, text="Timp ramas (din renewal_time):")
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
        self.label_timp_ramas.place(x=20, y=660)
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
        Clock.stop_all_clocks(self.clock_value)
        self.buton_connect["state"] = DISABLED

        # construire packet Dhcp Discover
        self.append_to_logging("Initializare packet...")
        packet = self.inputs_to_packet()
        packet.opcode = Opcodes.REQUEST
        packet.dhcp_message_type = MessageType.DISCOVER

        packet_bytes = packet.encode()
        self.append_to_logging("Packet initializat...")

        # trimitere DISCOVER
        self.append_to_logging("Trimitere DHCPDiscover...")
        CLIENT_SOCKET.sendto(packet_bytes, CLIENT_DESTINATIN_ADDR)

        # primire mesaj OFFER
        self.append_to_logging("Asteptare DHCPOffer...")
        putem_citi, _, _ = select([CLIENT_SOCKET], [], [], 5)
        packet_2 = None
        if putem_citi:
            bytes_offer = CLIENT_SOCKET.recv(1024)
            packet_2 = Packet(bytes_offer)
        else:
            self.buton_connect["state"] = NORMAL
            self.append_to_logging("\nNu am primit raspuns de la server")

        # verificare si trimitere request
        if packet_2 and packet_2.dhcp_message_type == MessageType.OFFER:
            self.append_to_logging("Packet DHCPOffer primit...")
            packet_2.opcode = Opcodes.REQUEST
            packet_2.dhcp_message_type = MessageType.REQUEST
            CLIENT_SOCKET.sendto(packet_2.encode(), CLIENT_DESTINATIN_ADDR)
            self.append_to_logging("Trimitere DHCPRequest...")

            # asteptare packet ack
            putem_citi, _, _ = select([CLIENT_SOCKET], [], [], 5)
            packet_ack = Packet(CLIENT_SOCKET.recv(1024)) if putem_citi else None

            # afisare rezultate
            if packet_ack and packet_ack.dhcp_message_type == MessageType.ACK:
                self.append_to_logging("Packet DHCPAck")

                self.clock_value.set(packet_ack.renewal_time if packet_ack.renewal_time else 10)
                self.append_to_logging(str(packet_ack))

                self.lease_time_value.set(packet_ack.lease_time)
                self.renewal_time_value.set(packet_ack.renewal_time)

                if packet_ack.your_ip_address not in istoric_ipuri:
                    self.text_istoric_ips.config(state='normal')
                    self.text_istoric_ips.insert(END, f" {packet_ack.your_ip_address}\n")
                    self.text_istoric_ips.config(state='disabled')

                self.subnet_mask_option.set(packet_ack.subnet_mask)
                self.router_option.set(packet_ack.router)
                self.domain_server_option.set(packet_ack.domain_server)
                self.broadcast_address_option.set(packet_ack.broadcast_address)
                self.lease_time_option.set(packet_ack.lease_time)
                self.renewal_time_option.set(packet_ack.renewal_time)

                self.ip_curent_value.set(packet_ack.your_ip_address)
                if packet_ack.your_ip_address not in istoric_ipuri:
                    istoric_ipuri.append(packet_ack.your_ip_address)

                # setare si pornire clock
                Clock(self.clock_value, self.reconnect).start()
                self.buton_connect["state"] = NORMAL

    def reconnect(self):
        self.buton_connect["state"] = DISABLED

        Clock.stop_all_clocks(self.clock_value)

        packet_request = self.inputs_to_packet()
        packet_request.opcode = Opcodes.REQUEST
        packet_request.dhcp_message_type = MessageType.REQUEST

        for ip in istoric_ipuri:  # lista nu o sa fie niciodata goala la apelarea functiei reconnect
            self.append_to_logging(f"Incercare connectare cu {ip}...")
            # creare packet req
            packet_request.address_request = ip
            CLIENT_SOCKET.sendto(packet_request.encode(), CLIENT_DESTINATIN_ADDR)
            putem_citi, _, _ = select([CLIENT_SOCKET], [], [], 4)
            packet_ack = Packet(CLIENT_SOCKET.recv(1024)) if putem_citi else None
            if packet_ack is None:
                self.append_to_logging(f"Nu s-a reusit reconnectarea cu {ip}")
                continue
            else:
                # reusit conectare cu ip vechi
                self.clock_value.set(packet_ack.renewal_time if packet_ack.renewal_time else 10)
                current_ip = packet_ack.your_ip_address

                self.lease_time_value.set(packet_ack.lease_time)
                self.renewal_time_value.set(packet_ack.renewal_time)

                if packet_ack.your_ip_address not in istoric_ipuri:
                    self.text_istoric_ips.config(state='normal')
                    self.text_istoric_ips.insert(END, f" {packet_ack.your_ip_address}\n")
                    self.text_istoric_ips.config(state='disabled')

                self.subnet_mask_option.set(packet_ack.subnet_mask)
                self.router_option.set(packet_ack.router)
                self.domain_server_option.set(packet_ack.domain_server)
                self.broadcast_address_option.set(packet_ack.broadcast_address)
                self.lease_time_option.set(packet_ack.lease_time)
                self.renewal_time_option.set(packet_ack.renewal_time)

                self.ip_curent_value.set(packet_ack.your_ip_address)
                if packet_ack.your_ip_address not in istoric_ipuri:
                    istoric_ipuri.append(packet_ack.your_ip_address)

                Clock(self.clock_value, self.reconnect).start()
                self.buton_connect["state"] = NORMAL
                self.append_to_logging(f"Reusire reconectare cu ip {current_ip}")
                return

        # nu s-a reusit conectarea cu un ip mai vechi
        packet_request.address_request = '0.0.0.0'
        CLIENT_SOCKET.sendto(packet_request.encode(), CLIENT_DESTINATIN_ADDR)
        putem_citi, _, _ = select([CLIENT_SOCKET], [], [], 2)
        packet_ack = Packet(CLIENT_SOCKET.recv(1024)) if putem_citi else None
        if packet_ack is None:
            Clock.stop_all_clocks(self.clock_value)
            time.sleep(1)
            self.append_to_logging("Nu s-a putut reface conexiunea cu nici un server")
        else:
            current_ip = packet_ack.your_ip_address
            self.clock_value.set(packet_ack.renewal_time if packet_ack.renewal_time else 10)

            self.lease_time_value.set(packet_ack.lease_time)
            self.renewal_time_value.set(packet_ack.renewal_time)

            if packet_ack.your_ip_address not in istoric_ipuri:
                self.text_istoric_ips.config(state='normal')
                self.text_istoric_ips.insert(END, f" {packet_ack.your_ip_address}\n")
                self.text_istoric_ips.config(state='disabled')

            self.subnet_mask_option.set(packet_ack.subnet_mask)
            self.router_option.set(packet_ack.router)
            self.domain_server_option.set(packet_ack.domain_server)
            self.broadcast_address_option.set(packet_ack.broadcast_address)
            self.lease_time_option.set(packet_ack.lease_time)
            self.renewal_time_option.set(packet_ack.renewal_time)

            self.ip_curent_value.set(packet_ack.your_ip_address)
            if current_ip not in istoric_ipuri:
                istoric_ipuri.append(current_ip)

            self.append_to_logging(f"Reusire reconectare cu ip {current_ip}")

            self.buton_connect["state"] = NORMAL
            Clock(self.clock_value, self.reconnect).start()

    def disconnect(self):
        Clock.stop_all_clocks(self.clock_value)
        self.append_to_logging("Resurse eliberate.")
        self.buton_connect["state"] = NORMAL

    def start(self):
        self.set_widgets()
        self.window.mainloop()


if __name__ == "__main__":
    app = Interface()
    app.start()