from tkinter import Tk, Button, StringVar, Entry, Variable, Label, Text, NORMAL, Checkbutton, BooleanVar
from tkinter.ttk import Combobox
from typing import Callable, Optional, List


class BaseInterface:
    def __init__(self):
        self._window: Optional[Tk] = None

    def _create_button(self, text: str, command: Callable, x_position: int, y_position: int) -> Button:
        """Creates a button

        :param text: Button label text
        :param command: Command to be executed on button pressed
        :param x_position: x position of the button
        :param y_position: y position of the button
        :return: Button widget
        """
        button = Button(self._window, text=text, command=command)
        button.place(x=x_position, y=y_position)
        return button

    def _create_entry(self, x_position: int, y_position: int, width: int, height: int,
                      variable_type: Callable = StringVar, font: tuple = ('calibre', 10, 'normal')) -> (Entry, Variable):
        """Creates an entry

        :param x_position: x position of the entry widget
        :param y_position: y position of the entry widget
        :param width: width of the entry widget
        :param height: height of the entry widget
        :param variable_type: The type of variable to be paired to the entry widget
        :param font: The font to be set. ( family, size, weight )
        :return: A pair of (Entry Widget, Variable paired to the widget)
        """
        variable = variable_type()
        entry = Entry(self._window, textvariable=variable, font=font)
        entry.place(x=x_position, y=y_position, width=width, height=height)
        return entry, variable

    def _create_label(self, x_pos: int, y_pos: int, text: str = None,
                      variable_type=None, font: tuple = ("Arial", 8)) -> (Label, Optional[Variable]):
        """Creates a label

        :param x_pos: x position of the label widget
        :param y_pos: y position of the label widget
        :param text: Text to be placed inside the widget
        :param variable_type: The type of variable to be paired to the label widget
        :param font: The font to be set. ( family, size, weight )
        :return: A Label if variable_type is not set, else (Label, Variable paired to label)
        """
        label: Label
        if variable_type:
            variable: Variable = variable_type()
            variable.set("...") if variable_type == StringVar else variable.set(0)
            label = Label(self._window, textvariable=variable, font=font)
            label.place(x=x_pos, y=y_pos)
            return label, variable
        elif text:
            label = Label(self._window, text=text, font=font)
            label.place(x=x_pos, y=y_pos)
            return label

    def _create_text(self, x_pos: int, y_pos: int, height: int, width: int,
                     with_state: bool = False) -> (Text, Optional[str]):
        """Creates a text field

        :param x_pos: x position of the widget
        :param y_pos: x position of the widget
        :param height: height of the widget
        :param width: width of the widget
        :param with_state: true if the widget must have a state, false otherwise
        :return: A text field if with_state is not set, else (Text, State paired to label)
        """
        if with_state:
            state = NORMAL
            text = Text(self._window, height=height, width=width, state=state)
            text.place(x=x_pos, y=y_pos)
            return text, state
        else:
            text = Text(self._window, height=height, width=width)
            text.place(x=x_pos, y=y_pos)
            return text

    def _create_checkbutton(self, text: str, x_pos: int, y_pos: int) -> (Checkbutton, BooleanVar):
        """Creates a checkbutton

        :param text: Text that will be shown next to the checkbox
        :param x_pos: x position of the widget
        :param y_pos: y position of the widget
        :return: (Checkbutton, Variable paired to the widget)
        """
        variable = BooleanVar()
        checkbutton = Checkbutton(self._window, text=text, variable=variable, onvalue=1, offvalue=0)
        checkbutton.place(x=x_pos, y=y_pos)
        return Checkbutton, variable

    def _create_combobox(self, options: List[str], x_pos: int, y_pos: int, width: int) -> (Combobox, StringVar):
        """Creates a combobox

        :param options: List of options
        :param x_pos: x position of the widget
        :param y_pos: y position of the widget
        :param width: width of the widget
        :return: ( Combobox_Widget, Variable paired to the widget )
        """
        variable = StringVar()
        widget = Combobox(master=self._window, textvariable=variable, values=options, width=width)
        widget.place(x=x_pos, y=y_pos)
        return widget, variable

    def start(self):
        """Starts the mainloop"""
        self._window.mainloop()
