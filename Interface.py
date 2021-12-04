from tkinter import Tk, Button, Label,Entry
from threading import Thread

window = Tk()
window.geometry("600x600")

host_name = ''
address_request = ''
client_id = ''
hardware_address = ''
client_ip_address = ''


# creare widgeturi
buton_connect = Button(window, text="CONNECT")
buton_generare_default = Button(window, text="GEN. DEFAULT")

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

if __name__ == "__main__":

    window.mainloop()