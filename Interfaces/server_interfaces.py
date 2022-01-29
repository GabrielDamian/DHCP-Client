from tkinter import Tk, StringVar, END
from Interfaces.base_interface import BaseInterface
from Commons.receivers import Receivers
from threading import Thread


class ServerInterface(BaseInterface):
    def __init__(self):
        super().__init__()
        self._window = Tk()
        self._window.geometry("830x720")

        self._create_button(text="START SERVER", command=lambda: Thread(target=self._start_server).start(),
                            x_position=20, y_position=20)
        self._create_button(text="GEN. DEFAULT", command=lambda: Thread(target=self._generate_default).start(),
                            x_position=120, y_position=20)
        self._create_button(text="STOP SERVER", command=lambda: Thread(target=self._stop_server).start(),
                            x_position=220, y_position=20)

        self._create_label(x_pos=20, y_pos=100, text="Server Name:", font=("Arial", 10))
        self._create_label(x_pos=20, y_pos=150, text="Router:", font=("Arial", 10))
        self._create_label(x_pos=20, y_pos=200, text="DNS:", font=("Arial", 10))
        self._create_label(x_pos=20, y_pos=250, text="Lease Time:", font=("Arial", 10))
        self._create_label(x_pos=20, y_pos=300, text="Renewal Time:", font=("Arial", 10))
        self._create_label(x_pos=20, y_pos=350, text="Network Ip Address:", font=("Arial", 10))
        self._create_label(x_pos=20, y_pos=400, text="Subnet Mask:", font=("Arial", 10))
        self._create_label(x_pos=20, y_pos=450, text="Address Pool View:", font=("Arial", 10))
        self._create_label(x_pos=400, y_pos=20, text="Logging:", font=("Arial", 10))

        _, self._server_name_variable = self._create_entry(x_position=160, y_position=100, width=200, height=25,
                                                           variable_type=StringVar)
        _, self._router_variable = self._create_entry(x_position=160, y_position=150, width=200, height=25,
                                                      variable_type=StringVar)
        _, self._dns_variable = self._create_entry(x_position=160, y_position=200, width=200, height=25,
                                                   variable_type=StringVar)
        _, self._lease_time_variable = self._create_entry(x_position=160, y_position=250, width=200, height=25,
                                                          variable_type=StringVar)
        _, self._renewal_time_variable = self._create_entry(x_position=160, y_position=300, width=200, height=25,
                                                            variable_type=StringVar)
        _, self._network_ip_address_variable = self._create_entry(x_position=160, y_position=350, width=200, height=25,
                                                                  variable_type=StringVar)
        _, self._subnet_mask_variable = self._create_entry(x_position=160, y_position=400, width=200, height=25,
                                                           variable_type=StringVar)

        self._address_pool_view_text, _ = self._create_text(x_pos=20, y_pos=475, height=14, width=98, with_state=True)
        self._logging_text, _ = self._create_text(x_pos=400, y_pos=100, height=20, width=50, with_state=True)

    def _start_server(self):
        pass

    def _stop_server(self):
        pass

    def _generate_default(self):
        pass

    def _append_to_logging(self, text: str):
        """Writes text to logging window

        :param text: Text to be written
        """
        self._logging_text.config(state='normal')
        self._logging_text.insert(END, f" {text}\n")
        self._logging_text.config(state='disabled')

    def _update_address_pool_view(self, text: str):
        """Writes text to logging window

        :param text: Text to be written
        """
        self._address_pool_view_text.config(state='normal')
        self._address_pool_view_text.insert(END, f" {text}\n")
        self._address_pool_view_text.config(state='disabled')


if __name__ == "__main__":
    ServerInterface().start()
