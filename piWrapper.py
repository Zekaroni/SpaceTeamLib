import RPi.GPIO as localGPIO

class Board: # This is here to not throw a defintion error, ignore this
    pass

class Pin:
    """
    Creates a class for a pin using the GPIO library.
    Interfaces with the custom class Board made below.
    """
    def __init__(self, pinNumber: int, output: bool, parent: Board):
        self._pin_number = pinNumber                                                # Assigns a local pin number based on passed pin number
        self._output = output                                                       # True is Ouput and False is Input
        self._parent = parent                                                       # Best not to mess with this, it is getting into nested classes
        self.isOn = False
        localGPIO.setup(pinNumber, localGPIO.OUT if output else localGPIO.IN)       # Sets up pin
    
    def turnOn(self) -> None:
        """
        Turns the pin on, sets to HIGH/3.3V
        """
        # TODO: Thow errors there if the pin isn't output, same with turnOff
        if self._output:
            localGPIO.output(self._pin_number, localGPIO.HIGH)
            self.isOn = True

    def turnOff(self) -> None:
        """
        Turns the pin off, sets to LOW/0V
        """
        if self._output:
            localGPIO.output(self._pin_number, localGPIO.LOW)
            self.isOn = False

    def read(self) -> bool:
        """
        Return the value of the pin, True or False, 1 or 0

        return: bool of pin state
        """
        if not self._output:
            return localGPIO.input(self._pin_number)

    def number(self) -> int:
        """
        Returns the pin number

        return: pin number
        """
        return self._pin_number

    def __check_parent_for_pin__(self) -> None:
        """
        An internal check to see if the pin was set up properly
        """
        if not self._pin_number in self._parent._active_pins.keys(): # Adds a redundant check for less points of failure
            raise ReferenceError("Pin is not setup [CALLED FROM PIN CLASS]")

class Board:
    """
    Idk what to put here, it's a board
    """
    def __init__(self):
        localGPIO.setmode(localGPIO.BOARD) # This tells the API you are using pin number based on the physical board
        localGPIO.setwarnings(False)       # This just removes those annoying warning, no one likes those...
        self._banned_pins = {
            1 : "3.3V",
            2 : "5V" ,
            4 : "5V" ,
            6 : "Ground" ,
            9 : "Ground" ,
            14 : "Ground" ,
            17 : "3.3V" ,
            20 : "Ground" ,
            25 : "Ground" ,
            27 : "EEprom" ,
            28 : "EEprom" ,
            30 : "Ground" ,
            34 : "Ground" ,
            39 : "Ground" ,
        }
        self._active_pins = {
            # pinNumber : Pin object
        }

    def setupPin(self, pinNumber: int, output: bool) -> None:
        """
        Sets up a pin for use with the piWrapper

        pinNumber: int of the pin you wish to setup
        output: bool True for output, False for input
        """
        if self.__check_pin_index__(pinNumber): pass                # Checks to make sure pin number is a valid pin
        if not self.__check_active_pin__(pinNumber): pass           # Checks to make sure the pin isn't already active

        self._active_pins[pinNumber] = Pin(pinNumber, output, self) # Creates an object and stores it in the active pin dict
    
    def pin(self, pinNumber: int) -> Pin:
        """
        This can be called to assign a specific pin to a custom variable

        pinNumber: pin number wished to access
        return: Pin object that can be stored in a variable and referenced to make things easier to use
        """
        if self.__check_pin_index__(pinNumber): pass # Checks to make sure pin number is a valid pin
        if self.__check_active_pin__(pinNumber):     # Checks if the pin is active
            return self._active_pins[pinNumber]      # Reuturns Pin object
        else:
            raise ReferenceError("Pin not setup")    # Thows an error if the pin isn't set up yey

    def getBannedPins(self) -> list:
        """
        Returns a list of banned pins stored in a list

        return: list of banned pins as ints
        """
        return list(self._banned_pins.keys())

    def printBannedPins(self) -> None:
        """
        Prints the banned pins and why they are banned
        """
        print(''.join([f"{pin}: {self._banned_pins[pin]}\n" for pin in self._banned_pins]))
    
    def cleanup(self) -> None:
        """"
        Resets all pins to low and cleans up
        """
        for pin in self._active_pins:
            if pin._output:
                pin.turnOff()
        localGPIO.cleanup()
    
    @staticmethod
    def getCPUTemperature() -> str:
        """
        Returns the temperature of the CPU in C as a string

        return: string temperature of CPU
        """
        with open('/sys/class/thermal/thermal_zone0/temp', 'r') as f:
            temp = round(int(f.read().strip()) / 1000.0,1)
        return str(temp)

    # NOTE: Removed the gpu temp check since it currently requires a subprocess import, going for optimizations here

    def __check_pin_index__(self, pinNumber) -> bool:
        """
        For error checking internally if a pin index is OutOfBounds

        pinNumber: pin number to be checked
        return: bool based on if the number is 1-40
        """
        if pinNumber < 1 or pinNumber > 40:
            raise IndexError("Pin number out of index")
        else:
            return True
    
    def __check_active_pin__(self, pinNumber) -> bool:
        """
        For checking internally if a pin is active

        pinNumber: pin number to be checked
        return: bool based on if the pin number is in the active pins or not
        """
        return pinNumber in self._active_pins.keys()

if __name__ == "__main__":
    # Example script. Dont forget to turn the pin off after running this.
    from time import sleep
    pi = Board()
    pi.setupPin(3,True)

    print(pi._active_pins.keys())

    pin3 = pi.pin(3)

    print(pin3.number())

    pin3.turnOn()
    sleep(3)
    pin3.turnOff()
    
    pi.printBannedPins()