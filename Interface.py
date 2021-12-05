from tkinter import *
from threading import Thread

window = Tk()
window.geometry("800x600")

host_name = StringVar()
address_request = StringVar()
client_id =StringVar()
hardware_address = StringVar()
client_ip_address = StringVar()


def GenerateDefault():
    host_name.set('ceva')
    global text_logging
    global logging_data_state
    text_logging.config(state='normal')
    text_logging.insert(END,'\nceva')
    text_logging.config(state='disabled')



# creare widgeturi
buton_connect = Button(window, text="CONNECT")
buton_generare_default = Button(window, text="GEN. DEFAULT", command=GenerateDefault)

buton_connect.place(x=20,y=20)
buton_generare_default.place(x=100,y=20)

label_host_name = Label(window, text="HOST NAME",font=("Arial", 8))
label_address_request = Label(window, text="ADDRESS REQUEST",font=("Arial", 8))
label_client_id = Label(window, text="CLIENT ID",font=("Arial", 8))
label_client_hardware_address = Label(window, text="MAC",font=("Arial", 8))
label_client_ip_address = Label(window, text="CLIENT IP ADDRESS",font=("Arial", 8))

label_host_name.place(x=20, y=70)
label_address_request.place(x=20,y=110)
label_client_id.place(x=20,y=150)
label_client_hardware_address.place(x=20,y=190)
label_client_ip_address.place(x=20,y=230)

input_host_name = Entry(window, textvariable = host_name, font = ('calibre',10,'normal'))
input_address_request = Entry(window, textvariable = address_request, font = ('calibre',10,'normal'))
input_client_id = Entry(window, textvariable = client_id, font = ('calibre',10,'normal'))
input_client_hardware_address = Entry(window, textvariable = hardware_address, font = ('calibre',10,'normal'))
input_client_ip_address = Entry(window, textvariable = client_ip_address, font = ('calibre',10,'normal'))

input_host_name.place(x=150,y=70,width=180, height=20)
input_address_request.place(x=150, y=110, width=180,height=20)
input_client_id.place(x=150,y=150,width=180,height=20)
input_client_hardware_address.place(x=150,y=190,width=180,height=20)
input_client_ip_address.place(x=150,y=230,width=180,height=20)

#options
subnet_mask = BooleanVar()
router = BooleanVar()
domain_server = BooleanVar()
broadcast_address = BooleanVar()
lease_time = BooleanVar()
renewal_time = BooleanVar()


check_box_subnet_mask = Checkbutton(window, text='Subnet Mask',variable=subnet_mask, onvalue=1, offvalue=0)
check_box_router = Checkbutton(window, text='Router',variable=router, onvalue=1, offvalue=0)
check_box_domain_server = Checkbutton(window, text='Domain Server',variable=domain_server, onvalue=1, offvalue=0)
check_box_broadcast_address = Checkbutton(window, text='Broadcast address',variable=broadcast_address, onvalue=1, offvalue=0)
check_box_lease_time = Checkbutton(window, text='Lease Time',variable=lease_time, onvalue=1, offvalue=0)
check_box_renewal_time = Checkbutton(window, text='Renewal Time',variable=renewal_time, onvalue=1, offvalue=0)

check_box_subnet_mask.place(x=20,y=280)
check_box_router.place(x=20,y=320)
check_box_domain_server.place(x=20,y=360)
check_box_broadcast_address.place(x=20,y=400)
check_box_lease_time.place(x=20,y=440)
check_box_renewal_time.place(x=20,y=480)

#logging area
logging_data = StringVar()
logging_data_state= 'disabled'
text_logging = Text(window, height=30,width=45,state=logging_data_state)

text_logging.place(x=400,y=70)
label_logging = Label(window, text="Logging",font=("Arial", 10))
label_logging.place(x=400,y=46)




if __name__ == "__main__":
    window.mainloop()