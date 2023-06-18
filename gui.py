import tkinter as tk
from tkinter import messagebox
from piWrapper import Board

class PiGUI:
    def __init__(self, board: Board):
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


        self._info_box = None
        self._active_button_config_elements = []
        self._column_amount = 20 # This is beacause of the 20 pins on each row
        self._max_row_length = 30
        self._buttons = []
        self._button_states = {} # Button states
        self._current_pressed_button = None
        self._create_buttons() # Create buttons for each pin

    def _on_window_configure(self, event):
        # Update font size when the window is resized
        self._update_font()

    def _create_buttons(self):
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

        if self._board.__check_active_pin__(pin+1):
            _selected_option = self._board.pin(pin+1)._output
            _state_var = tk.BooleanVar(value=False)
            if _selected_option:
                output_radio = tk.Radiobutton(
                    self._main_frame, 
                    text="On",
                    bg=self._primary_colour,
                    variable=_state_var,
                    value=True,
                    command=lambda : self._change_state_of_pin(pin+1,True)
                )
                input_radio = tk.Radiobutton(
                    self._main_frame, 
                    text="Off",
                    bg=self._primary_colour,
                    variable=_state_var,
                    value=False,
                    command=lambda : self._change_state_of_pin(pin+1,False)
                )
            else:
                pass
            output_radio.grid(row=4, column=8, padx=5, pady=5)
            input_radio.grid(row=5, column=8, padx=5, pady=5)
            
            self._active_button_config_elements.append(output_radio)
            self._active_button_config_elements.append(input_radio)
        else:
            output_button = tk.Button(
                self._main_frame,
                text= f"Setup pin {pin+1} for output",
                bg = "red",
                command=lambda : self._setup_pin(pin, True)
            )
            output_button.grid(row=4, column=5, columnspan=4)
            input_button = tk.Button(
                self._main_frame,
                text= f"Setup pin {pin+1} for input",
                bg="cyan",
                command=lambda : self._setup_pin(pin, False)
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
        localPin = self._board.pin(pinNumber)
        if output:
            localPin.turnOn()
            self._buttons[40-pinNumber].configure(bg="lime green")
        else:
            localPin.turnOff()
            self._buttons[40-pinNumber].configure(bg="red")

    def _on_window_close(self):
        self._board.cleanup()
        self._parent.destroy()

    def _show_info(self, event, pin):
        if pin:
            self._info_box = tk.Label(
            self._main_frame,
                text="Info will pop up here",
                bg="misty rose"
            )
            self._info_box.config(text=self._board._banned_pins[pin])
            self._info_box.place(x=self._buttons[pin].winfo_x(), y=-self._buttons[pin].winfo_y())
        else:
            pass
    
    def _clear_info(self, event):
        if self._info_box:
            self._info_box.destroy()

    def run(self):
        self._parent.mainloop()


# Create an instance of PiGUI and run the application

pi_gui = PiGUI(Board())
pi_gui.run()
