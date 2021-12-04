from tkinter import Tk, Button, Label
from threading import Thread

window = Tk()

# creare widgeturi
buton_connect = Button(window, text="CONNECT")
buton_generare_default = Button(window, text="GEN. DEFAULT")

label_host_name = Label(window, text="HOST NAME")
label_address_request = Label(window, text="ADDRESS REQUEST")
label_client_id = Label(window, text="CLIENT ID")


if __name__ == "__main__":
    window.mainloop()