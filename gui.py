import tkinter as tk
from tkinter import messagebox
from piWrapper import Board

class PiGUI:
    def __init__(self, board: Board):
        # NOTE: When working with pins, the Board class expects true pin value (starts at 1), where this class uses true index (starts at 0)

        # Board config
        self._board = board
        
        # Colours and fonts
        self._primary_colour = "grey"
        self._secondary_colour = "light grey"
        self._primary_font = ('', 40)
        self._secondary_font = ('', 30)

        # Parent config
        self._parent = tk.Tk()
        self._parent.title("Pi GUI")
        self._parent.configure(bg=self._primary_colour)
        try:
            self._parent.attributes('-zoomed', True)  # Linux
        except Exception:
            self._parent.state('zoomed')  # Windows, for debugging
        
        self._parent.protocol("WM_DELETE_WINDOW", self._on_window_close)

        # Main frame
        self._main_frame = tk.Frame(self._parent)
        self._main_frame.config(bg=self._primary_colour)
        self._main_frame.pack(fill=tk.BOTH, expand=True)  # Fill entire window

        # Bind the Configure event of the parent window
        self._parent.bind("<Configure>", self._on_window_configure)

        self._info_box = tk.Label(
            self._main_frame,
            bg="misty rose"
        )

        self._active_button_config_elements = []
        self._active_pin_selected = 0
        self._column_amount = 20 # This is beacause of the 20 pins on each row
        self._max_row_length = 30
        self._buttons = []
        self._button_states = {} # Button states
        self._current_pressed_button = None
        self._init_main_widgets() # Creates all the main widgets

    def _on_window_configure(self, event):
        # Update font size when the window is resized
        self._update_font()

    def _init_main_widgets(self):
        # Create buttons for each pin
        num_pins = 40
        max_pin_label_length = len(str(num_pins))  # Calculate the length of the longest pin label
        
        for i in range(num_pins-1, -1, -1):
            pin = i + 1
            row = i % 2
            col = (num_pins - i - 1) // 2

            button = tk.Button(
                self._main_frame,
                text= f"Pin {pin}",
                width= max_pin_label_length + 5,  # Set the fixed width for the button
                command= lambda p=i: self._config_selected_pin(p)  # Pass pin as an argument to the command function
            )
            button.grid(row=row, column=col, padx=3, pady=3)
            self._button_states[i] = False  # Initialize button state to False
            self._buttons.append(button)      # Add the button to the list

            if pin in self._board.getBannedPins():
                button.configure(state=tk.DISABLED, bg="red4")

                button.bind("<Enter>", lambda event, p=pin: self._show_info(event, p))
                button.bind("<Leave>", self._clear_info)

            else:
                button.configure(bg="orange")

        for i in range(self._column_amount):
            self._main_frame.columnconfigure(i, weight=1)
        for i in range(self._max_row_length):
            self._main_frame.columnconfigure(i, weight=1)
        
        self._pin_states_label = tk.Label(
            self._main_frame,
            text="",
            width=20,
            height=5
        )
        self._pin_states_label.grid(row=3, column=17, columnspan=3, rowspan=20)

    def _config_selected_pin(self, pin):
        if self._active_button_config_elements:
            for obj in self._active_button_config_elements:
                obj.destroy()
            self._active_button_config_elements.clear()

        label = tk.Label(
                self._main_frame,
                text=f"Now configuring pin {pin+1}",
                bg = self._primary_colour
        )
        label.grid(
            row=3 ,
            column=0,
            columnspan=self._column_amount-3,
            padx=3,
            pady=30
        )
        self._active_button_config_elements.append(label)

        self._active_pin_selected = pin

        if self._board.__check_active_pin__(pin+1):
            _selected_option = self._board.pin(pin+1)._output
            if _selected_option:
                # Output
                self._state_var = tk.BooleanVar(value=False)
                on_radio = tk.Radiobutton(
                    self._main_frame, 
                    text="On",
                    bg=self._primary_colour,
                    variable=self._state_var,
                    value=True,
                    command=lambda p=pin: self._change_state_of_pin(p,True)
                )
                off_radio = tk.Radiobutton(
                    self._main_frame, 
                    text="Off",
                    bg=self._primary_colour,
                    variable=self._state_var,
                    value=False,
                    command=lambda p=pin: self._change_state_of_pin(p,False)
                )
                on_radio.grid(row=4, column=8, padx=5, pady=5)
                off_radio.grid(row=5, column=8, padx=5, pady=5)
                
                self._active_button_config_elements.append(on_radio)
                self._active_button_config_elements.append(off_radio)
            else:
                # Input
                pass
        else:
            output_button = tk.Button(
                self._main_frame,
                text= f"Setup pin {pin+1} for output",
                bg = "red",
                command=lambda p=pin: self._setup_pin(p, True)
            )
            output_button.grid(row=4, column=5, columnspan=4)
            input_button = tk.Button(
                self._main_frame,
                text= f"Setup pin {pin+1} for input",
                bg="cyan",
                command=lambda p=pin: self._setup_pin(p, False)
            )
            input_button.grid(row=4, column=8, columnspan=4)
            self._active_button_config_elements.append(output_button)
            self._active_button_config_elements.append(input_button)

    def _update_font(self):
        # Calculate font size based on the available space
        window_width = self._parent.winfo_width()
        window_height = self._parent.winfo_height()
        max_button_width = window_width // 20  # Assuming 20 buttons per row
        max_button_height = window_height // 2  # Assuming 2 rows
        max_font_size = round(min(max_button_width // 6.5, max_button_height // 3.5))

        # Update font size for all buttons
        for button in self._buttons:
            button.configure(font=('Arial', max_font_size))
        for obj in self._active_button_config_elements:
            if obj.cget("font") != "":
                obj.configure(font=('Arial', max_font_size))
    
    def _setup_pin(self, pinNumber, output):
        self._board.setupPin(pinNumber+1, output)
        self._config_selected_pin(pinNumber)
    
    def _change_state_of_pin(self, pinNumber, output):
        localPin = self._board.pin(pinNumber+1)
        if output:
            localPin.turnOn()
            self._buttons[39-pinNumber].configure(bg="lime green")
        else:
            localPin.turnOff()
            self._buttons[39-pinNumber].configure(bg="red")

    def _on_window_close(self):
        self._board.cleanup()
        self._parent.destroy()

    def _show_info(self, event, pin):
        if pin:
            self._info_box.config(text=self._board._banned_pins[pin])
            button = event.widget

            button_width = button.winfo_width()
            button_height = button.winfo_height()

            label_x = button.winfo_x() + button_width // 2 - self._info_box.winfo_reqwidth() // 2
            label_y = button.winfo_y() + self._info_box.winfo_height() * 2.1

            self._info_box.place(x=label_x, y=label_y)
            self._info_box.lift()
        else:
            pass
        
    def _clear_info(self, event):
        self._info_box.place_forget()
    
    def _display_pin_states(self):

        self._pin_states_label.after(100, self._display_pin_states)

    def run(self):
        self._parent.mainloop()


# Create an instance of PiGUI and run the application

pi_gui = PiGUI(Board())
pi_gui.run()
