import time
from tkinter import *
from DHCP_Packet import *
from select import select
from threading import Thread


# initializare componente
istoric_ipuri = []
current_ip = None


SOURCE_ADDR = ("", 68)
DESTINATIN_ADDR = ('<broadcast>', 67)

sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
sock.setsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST, 1)
sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
sock.bind(SOURCE_ADDR)


class Clock(Thread):

    all_clocks = []

    @staticmethod
    def stop_all_clocks():

        for clock in Clock.all_clocks:
            clock.stop()
            Clock.all_clocks.remove(clock)

        time.sleep(1)
        clock_value.set(0)

    def __init__(self, time_variable: IntVar):
        Thread.__init__(self)
        self.time_variable = time_variable
        self.stop_flag = False

    def run(self):
        Clock.all_clocks.append(self)
        self.stop_flag = False
        while not self.stop_flag and self.time_variable.get() > 0:
            time.sleep(1)
            self.time_variable.set(self.time_variable.get() - 1)

        if self.time_variable.get() <= 0 and not self.stop_flag:
            reconnect()

    def stop(self):
        self.stop_flag = True

def inputs_to_packet():
    # host_name = StringVar()
    # address_request = StringVar()
    # client_id = StringVar()
    # hardware_address = StringVar()
    # client_ip_address = StringVar()

    coduri = []
    # for op in ['subnet_mask', 'router','domain_server', 'broadcast_address','lease_time','renewal_time' ]:
    #     if(globals()[op] == True):
    #         coduri.append(getattr(Optiuni_request, op.upper()))
    # print("CEVA:",coduri)

    if subnet_mask.get():
        coduri.append(Optiuni_request(1))
    if router.get():
        coduri.append(Optiuni_request(3))
    if domain_server.get():
        coduri.append(Optiuni_request(6))
    if broadcast_address.get():
        coduri.append(Optiuni_request(28))
    if lease_time.get():
        coduri.append(Optiuni_request(51))
    if renewal_time.get():
        coduri.append(Optiuni_request(58))
    print("CEVA:",coduri)

    newPacket = Packet(packet=None, requested_options=coduri)
    newPacket.host_name = host_name.get()
    newPacket.address_request = address_request.get() if address_request.get() != 'None' else '0.0.0.0'
    newPacket.client_id = client_id.get() if client_id.get() != 'None' else '1'
    newPacket.client_hardware_address = hardware_address.get()
    newPacket.client_ip_address = client_ip_address.get()

    return newPacket
# functions


def append_to_logging(text: str):
    global text_logging
    text_logging.config(state='normal')
    text_logging.insert(END, f" {text}\n")
    text_logging.config(state='disabled')


def generate_default():
    packet = Packet()

    host_name.set(packet.host_name)
    address_request.set(packet.address_request)
    client_id.set(packet.client_id)
    hardware_address.set(packet.client_hardware_address)
    client_ip_address.set(packet.client_ip_address)

    subnet_mask.set(True)
    router.set(False)
    domain_server.set(False)
    broadcast_address.set(False)
    lease_time.set(True)
    renewal_time.set(True)


def connect():

    # manageriere timer ( oprire thread vechi vechi daca avem unul )
    Clock.stop_all_clocks()

    # ca sa nu ajungem la stare defectuasa oprim butonul de connect pe durata conectarii
    buton_connect["state"] = DISABLED

    # construire packet DHCP Discover
    append_to_logging("Initializare packet...")
    packet = inputs_to_packet()
    # packet.opcode = Opcodes.REQUEST
    # packet.host_name = "salut"
    packet.dhcp_message_type = Tip_Mesaj.DISCOVER
    # packet.boot_flags = 1
    packet_bytes = packet.pregateste_packetul()
    append_to_logging("Packet initializat...")

    # trimitere DISCOVER
    append_to_logging("Trimitere DHCPDiscover...")
    sock.sendto(packet_bytes, DESTINATIN_ADDR)

    # primire mesaj OFFER
    append_to_logging("Asteptare DHCPOffer...")
    putem_citi, _, _ = select([sock], [], [], 5)
    bytes_offer = sock.recv(1024)
    packet_2 = Packet(bytes_offer) if putem_citi else None

    # verificare si trimitere request
    if packet_2 and packet_2.dhcp_message_type == Tip_Mesaj.OFFER:
        append_to_logging("Packet DHCPOffer primit...")
        packet_2.opcode = Opcodes.REQUEST
        packet_2.dhcp_message_type = Tip_Mesaj.REQUEST
        sock.sendto(packet_2.pregateste_packetul(), DESTINATIN_ADDR)
        append_to_logging("Trimitere DHCPRequest...")

        # asteptare packet ack
        putem_citi, _, _ = select([sock], [], [], 5)
        packet_ack = Packet(sock.recv(1024)) if putem_citi else None

        # afisare rezultate
        if packet_ack and packet_ack.dhcp_message_type == Tip_Mesaj.ACK:
            append_to_logging("Packet DHCPAck")

            clock_value.set(packet_ack.renewal_time if packet_ack.renewal_time else 10)
            append_to_logging(packet_ack)

            lease_time_value.set(packet_ack.lease_time)
            renewal_time_value.set(packet_ack.renewal_time)

            if packet_ack.your_ip_address not in istoric_ipuri:
                text_istoric_ips.config(state='normal')
                text_istoric_ips.insert(END, f" {packet_ack.your_ip_address}\n")
                text_istoric_ips.config(state='disabled')

            ip_curent_value.set(packet_ack.your_ip_address)

            istoric_ipuri.append(packet_ack.your_ip_address)

            # setare si pornire clock
            Clock(clock_value).start()

    # pornire inapoi a butonului connect
    buton_connect["state"] = NORMAL


def reconnect():
    global clock_value
    # manageriere timer
    Clock.stop_all_clocks()

    for ip in istoric_ipuri: # lista nu o sa fie niciodata goala la apelarea functiei reconnect
        append_to_logging(f"Incercare connectare cu {ip}...")
        # creare packet req
        packet_request = Packet()
        packet_request.address_request = ip
        packet_request.opcode = Opcodes.REQUEST
        packet_request.dhcp_message_type = Tip_Mesaj.REQUEST
        sock.sendto(packet_request.pregateste_packetul(), DESTINATIN_ADDR)
        putem_citi, _, _ = select([sock], [], [], 4)
        packet_ack = Packet(sock.recv(1024)) if putem_citi else None
        if packet_ack == None:
            append_to_logging(f"Nu s-a reusit reconnectarea cu {ip}")
            continue
        else:
            # reusit conectare cu ip vechi
            clock_value.set(packet_ack.renewal_time if packet_ack.renewal_time else 10)
            current_ip = packet_ack.your_ip_address

            lease_time_value.set(packet_ack.lease_time)
            renewal_time_value.set(packet_ack.renewal_time)

            if packet_ack.your_ip_address not in istoric_ipuri:
                text_istoric_ips.config(state='normal')
                text_istoric_ips.insert(END, f" {packet_ack.your_ip_address}\n")
                text_istoric_ips.config(state='disabled')

            ip_curent_value.set(packet_ack.your_ip_address)

            istoric_ipuri.append(packet_ack.your_ip_address)

            # setare si pornire clock
            Clock(clock_value).start()

            append_to_logging(f"Reusire reconectare cu ip {current_ip}")
            return

    # nu s-a reusit conectarea cu un ip mai vechi
    packet_request = Packet()
    sock.sendto(packet_request.pregateste_packetul(), DESTINATIN_ADDR)
    putem_citi, _, _ = select([sock], [], [], 2)
    packet_ack = Packet(sock.recv(1024)) if putem_citi else None
    if packet_ack == None:
        append_to_logging("Nu s-a putut reface conexiunea cu nici un server")
    else:
        current_ip = packet_ack.your_ip_address
        clock_value.set(packet_ack.renewal_time if packet_ack.renewal_time else 10)

        lease_time_value.set(packet_ack.lease_time)
        renewal_time_value.set(packet_ack.renewal_time)

        if packet_ack.your_ip_address not in istoric_ipuri:
            text_istoric_ips.config(state='normal')
            text_istoric_ips.insert(END, f" {packet_ack.your_ip_address}\n")
            text_istoric_ips.config(state='disabled')

        ip_curent_value.set(packet_ack.your_ip_address)

        istoric_ipuri.append(current_ip)

        # setare si pornire clock
        Clock(clock_value).start()


def disconnect():
    Clock.stop_all_clocks()
    append_to_logging("Resurse eliberate.")




window = Tk()
window.geometry("800x720")

host_name = StringVar()
address_request = StringVar()
client_id = StringVar()
hardware_address = StringVar()
client_ip_address = StringVar()

# creare widgeturi
buton_connect = Button(window, text="CONNECT", command=lambda: Thread(target=connect, args=()).start())
buton_generare_default = Button(window, text="GEN. DEFAULT",
                                command=lambda: Thread(target=generate_default, args=()).start())
buton_deconectare = Button(window, text="DISCONNECT", command=lambda: Thread(target=disconnect, args=()).start())

buton_connect.place(x=20, y=20)
buton_generare_default.place(x=100, y=20)
buton_deconectare.place(x=203,y=20)

label_host_name = Label(window, text="HOST NAME", font=("Arial", 8))
label_address_request = Label(window, text="ADDRESS REQUEST", font=("Arial", 8))
label_client_id = Label(window, text="CLIENT ID", font=("Arial", 8))
label_client_hardware_address = Label(window, text="MAC", font=("Arial", 8))
label_client_ip_address = Label(window, text="CLIENT IP ADDRESS", font=("Arial", 8))

label_host_name.place(x=20, y=70)
label_address_request.place(x=20, y=110)
label_client_id.place(x=20, y=150)
label_client_hardware_address.place(x=20, y=190)
label_client_ip_address.place(x=20, y=230)

input_host_name = Entry(window, textvariable=host_name, font=('calibre', 10, 'normal'))
input_address_request = Entry(window, textvariable=address_request, font=('calibre', 10, 'normal'))
input_client_id = Entry(window, textvariable=client_id, font=('calibre', 10, 'normal'))
input_client_hardware_address = Entry(window, textvariable=hardware_address, font=('calibre', 10, 'normal'))
input_client_ip_address = Entry(window, textvariable=client_ip_address, font=('calibre', 10, 'normal'))

input_host_name.place(x=150, y=70, width=180, height=20)
input_address_request.place(x=150, y=110, width=180, height=20)
input_client_id.place(x=150, y=150, width=180, height=20)
input_client_hardware_address.place(x=150, y=190, width=180, height=20)
input_client_ip_address.place(x=150, y=230, width=180, height=20)

# options
subnet_mask = BooleanVar()
router = BooleanVar()
domain_server = BooleanVar()
broadcast_address = BooleanVar()
lease_time = BooleanVar()
renewal_time = BooleanVar()

check_box_subnet_mask = Checkbutton(window, text='Subnet Mask', variable=subnet_mask, onvalue=1, offvalue=0)
check_box_router = Checkbutton(window, text='Router', variable=router, onvalue=1, offvalue=0)
check_box_domain_server = Checkbutton(window, text='Domain Server', variable=domain_server, onvalue=1, offvalue=0)
check_box_broadcast_address = Checkbutton(window, text='Broadcast address', variable=broadcast_address, onvalue=1,
                                          offvalue=0)
check_box_lease_time = Checkbutton(window, text='Lease Time', variable=lease_time, onvalue=1, offvalue=0)
check_box_renewal_time = Checkbutton(window, text='Renewal Time', variable=renewal_time, onvalue=1, offvalue=0)

check_box_subnet_mask.place(x=20, y=280)
check_box_router.place(x=20, y=320)
check_box_domain_server.place(x=20, y=360)
check_box_broadcast_address.place(x=20, y=400)
check_box_lease_time.place(x=20, y=440)
check_box_renewal_time.place(x=20, y=480)

# logging area
logging_data = StringVar()
logging_data_state = 'disabled'
text_logging = Text(window, height=30, width=45, state=logging_data_state)

text_logging.place(x=400, y=70)
label_logging = Label(window, text="Logging", font=("Arial", 10))
label_logging.place(x=400, y=46)

#footer gui
label_separator_footer = Label(window, text="__________________________________________________________________________________________________________________________", font=("Arial", 8))
label_separator_footer.place(x=20, y=570)

#Lease time area
lease_time_value = IntVar()
lease_time_value.set(0)

label_lease_time_value = Label(window, textvariable=lease_time_value)
label_lease_time_value.place(x=90,y=600)

label_lease_time = Label(window, text="Lease time:")
label_lease_time.place(x=20,y=600)



#Renewal time area
renewal_time_value = IntVar()
renewal_time_value.set(0)

label_renewal_time_value = Label(window, textvariable=renewal_time_value)
label_renewal_time_value.place(x=106,y=631)

label_renewal_time = Label(window, text="Renewal time:")
label_renewal_time.place(x=20,y=630)

#live clock area
clock_value = IntVar()
label_clock = Label(window, textvariable=clock_value)
label_clock.place(x=197, y=661)

label_timp_ramas = Label(window, text="Timp ramas (din renewal_time):")
label_timp_ramas.place(x=20,y=660)

#ip history area
label_istoric_ips = Label(window, text="Istoric ip-uri:")
label_istoric_ips.place(x=400,y=600)

text_istoric_ips =Text(window, height=3, width=45)
text_istoric_ips.place(x=400,y=630)

label_ip_curent = Label(text="Ip curent:")
label_ip_curent.place(x=400,y=690)


ip_curent_value = StringVar()
ip_curent_value.set(0)

label_ip_curent_value = Label(window, textvariable=ip_curent_value)
label_ip_curent_value.place(x=453,y=690)


if __name__ == "__main__":
    window.mainloop()
