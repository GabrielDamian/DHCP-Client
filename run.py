from DHCP_Client.server_test import run_server
from DHCP_Client.Interface import window
from tkinter import Tk

if __name__ == "__main__":
    run_server()
    window.mainloop()