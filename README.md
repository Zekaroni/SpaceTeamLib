# piWrapper

This is a wrapper for the GPIO on the RaspberryPi Model 3 B's used by the BRCTC Space Team.

## Table of Contents
- [Installation](#installation)
  - [Cloning the Repository](#cloning-the-repository)
  - [Manual Download](#manual-download)
- [Usage](#usage)
  - [`Board`](#board)
    - [`setupPin`](#setuppinpinnumber-int-output-bool---none)
    - [`pin`](#pinpinnumber-int---pin)
    - [`getBannedPins`](#getbannedpins---list)
    - [`printBannedPins`](#printbannedpins---none)
    - [`getCPUTemperature`](#getcputemperature---str)
    - [`cleanup`](#cleanup---none)
  - [`Pin`](#pin)
    - [`turnOn`](#turnon---none)
    - [`turnOff`](#turnoff---none)
    - [`read`](#read---bool)
    - [`number`](#number---int)
- [Notes and Troubleshooting](#notes-and-troubleshooting)
  - [Banned Pins](#banned-pins)
  - [HIGH and LOW](#high-and-low)
  - [Initializing Board](#initializing-board)
  - [Common Errors](#common-errors)
  - [Example Code](#example-code)


## Installation

### Cloning the Repository

To install this package by cloning the repository, follow these steps:

1. Open a terminal.
2. Run the following command to clone the repository:

   ```
   git clone https://github.com/Zekaroni/SpaceTeamLib.git
   ```

   This will create a local copy of the repository on your machine.

3. Once the cloning process is complete, you can use the library in your projects by importing it.

### Manual Download

If you prefer to manually download the library, follow these steps:

1. Visit the library's GitHub page at [https://github.com/Zekaroni/SpaceTeamLib.git](https://github.com/Zekaroni/SpaceTeamLib.git).
2. Click on the "Code" button and select "Download ZIP" to download the repository as a ZIP file.
3. Extract the downloaded ZIP file to a convenient location on your machine.
4. Once the extraction is complete, you can use the library in your projects by importing it.

Note: If you encounter any issues while using `git` for cloning, make sure you have `git` installed on your system. If it's not installed, you can install it by running the command `sudo apt install git` in the terminal.


## Usage

### `Board`

This creates a variable of the class `Board` that allows for interfacing with the GPIO using Python script. (See [`Initializing Board`](#initializing-board) to learn more.)

```python
import piWrapper

board = piWrapper.Board()
```

#### `setupPin(pinNumber: int, output: bool) -> None`

The function `setupPin` is used to initialize a pin for use with the Python script. Two arguments are needed when calling this function, `pinNumber` and `output`. The first one, `pinNumber`, it is the pin number that will be setup (as an `int`). The second one, `output`, is what decides if the pin is output or input; `True` will make the pin output, and `False` will make the pin input. Output will allow you to set the pin `HIGH` or `LOW` ([more information](#high-and-low)), and input will allow you to monitor an read the current voltage being supplied to the pin.<br>
Note that trying to set up a [banned pin](#banned-pins) will throw an error.

```python
board.setupPin(3, True)  # Sets up pin 3 as Output.
board.setupPin(5, False) # Sets up pin 5 as Input.
```

#### `pin(pinNumber: int) -> Pin`

This function returns a [`Pin` object](#pin) that is connected to the `int` passed in as the parameter. Note that this will throw an error if the pin has not be set up before being called.

```python
myPin = board.pin(3) # This will return an object connected to pin 3.
```

#### `getBannedPins() -> list`

This function returns a list of all pins that are disabled in the format of `int`. ([See why some pins are banned.](#banned-pins))

```python
bannedPins = board.getBannedPins()
```

#### `printBannedPins() -> None`

Prints a list of [pins that are banned](#banned-pins) along with why they are banned to the console.

```python
board.printBannedPins()
```

#### `getCPUTemperature() -> str`

This function that outputs the current temperature of the Pi's CPU in `str` format. Note that the temperature is in centigrade.

```python
print(board.getCPUTemperature())
```

#### `cleanup() -> None`

This function resets and releases the GPIO pins used by the program, returning them to a default state and preventing conflicts with other applications or subsequent runs of your program. **YOU SHOULD ALWAYS PUT THIS AT THE END OF YOUR CODE!**

```py
board.cleanup() # This will reset all pins to normal states
```

### `Pin`

```python
import piWrapper

board = piWrapper.Board() # Creates the main board object
board.setupPin(3, True)   # Sets up pin 3 for use with output
pin3 = board.pin(3)       # Creates a varible that is connected to pin 3
```

#### `turnOn() -> None`

This function turns on the pin, setting the voltage to [HIGH](#high-and-low). Note that this will raise an error if called on a pin registered to output.

```python
pin3.turnOn() # This will turn on pin 3
```
or you can call it directly without creating a variable
```python
board = piWrapper.Board() # Creates the main board object
board.setupPin(3, True)   # Sets up pin 3 to be ready to use with output
board.pin(3).turnOn()     # Turn on pin 3
```

#### `turnOff() -> None`

This function turns off the pin, setting the voltage to [LOW](#high-and-low). Note that this will raise an error if called on a pin registered to output.

```python
pin3.turnOff() # This will turn off pin 3
```
or you can call it directly without creating a variable
```python
board = piWrapper.Board() # Creates the main board object
board.setupPin(3, True)   # Sets up pin 3 to be ready to use with output
board.pin(3).turnOff()    # Turn off pin 3
```


#### `read() -> bool`

This function returns the value of the pin number being read from. The value returned is a boolean value `True` or `False`, `1` or `0`. Note that calling this on a pin setup for output will raise an error.

```python
board = piWrapper.Board() # Creates the main board object
board.setupPin(3, False)  # Sets up pin 3 to read the voltage (input)
pin3 = board.pin(3)       # Assigns pin 3 to a variable
pinValue = pin3.read()    # Assigns the value of the pin the a variable
```

#### `number() -> int`

This function returns the pin number.

```python
pinNumber = myPin.number()
```

## Notes and Troubleshooting

### Banned Pins

The following pins are banned due to specific reasons:

| Pin Number | Reason                      |
|------------|-----------------------------|
| 1          | Provides 3.3V power supply  |
| 2          | Provides 5V power supply    |
| 4          | Provides 5V power supply    |
| 6          | Connected to ground (GND)   |
| 9          | Connected to ground (GND)   |
| 14         | Connected to ground (GND)   |
| 17         | Provides 3.3V power supply  |
| 20         | Connected to ground (GND)   |
| 25         | Connected to ground (GND)   |
| 27         | Connected to EEPROM         |
| 28         | Connected to EEPROM         |
| 30         | Connected to ground (GND)   |
| 34         | Connected to ground (GND)   |
| 39         | Connected to ground (GND)   |

These pins are disabled and should not be used for other purposes. Using them for unintended connections or operations could result in short circuits, voltage exceedance, unintended interference, or other undesirable consequences.

It is highly recommended to keep these pins in the banned list to prevent potential damage or unwanted side effects on the Raspberry Pi.

### `HIGH` and `LOW`
When a pin is "high" it means it is outputting it's max voltage. In the case of the RaspberryPi's used by the Space Team, as well many other other microcontrollers, this voltage is 3.3V.<br>
When a pin is "low" it means that the voltage is being pulled down to 0V (technically close to 0V, but it is still perceived as off).<br>
With most microcontrollers and software the team will be using, these states are represented as `1` or `0`, `True` or `False`. So keeping this in mind, when writing programs that use the [`read`](#read---bool) function, always remember that the output will be `True` or `False` based on `On` or `Off`.

### Initializing `Board`
When writing a program with this wrapper, you only need one instance of `Board`. The variable can also be named anything, it doesn't have to be `board`. Bellow is an example of different ways to import and named the initial object.
```py
import piWrapper

board = piWrapper.Board()
```
```py
from piWrapper import Board

raspPi = Board()
```

### Common Errors
These are some errors I think might be common when first working with this wrapper.
- **Calling a pin that hasn't been setup.** If you try to call a pin you haven't first set up, you will run into an error. Always be sure to initialize any pin before calling it. The code below is how you _should_ set up a pin before using it:
    ```py
    board = piWrapper.Board()
    board.setupPin(3, True)
    board.pin(3).turnOn()
    ```
    The code below will show an example of an error:
    ```py
    board = piWrapper.Board()
    board.pin(3).turnOn()
    ```
    This will raise:
    ```
    ReferenceError: Pin is not setup
    ```
- **Forgetting to specify input or output in the second parameter for `setupPin`.** This will thrown an error saying you forgot a parameter. Refer to [`setupPin`](#setuppinpinnumber-int-output-bool---none) to see how to properly set up a pin for input or output.<br>
**NOTE**: There has been no testing for changing a pin that has already been setup. I plan to make sure this feature is added and working to allow for more dynamic code and projects.

### Example Code
(NOTE: This was all written while writing this document, meaning it is untested but should work in theory. Ask me if something isn't working when referencing this code.)<br><br>
This code is an example of how to make an LED flash on and off until stopped (use `CTRL+C` to kill any running task, this is know as a `KeyboardInterrupt`). First connect an led to pin 3, and then connect it to a ground pin on the RaspberryPi.
```py
from piWrapper import Board # Imports only Board from piWrapper
# I reccomend doing it this way each time to avoid crowding the global variables

from time import sleep # Only imports the sleep function from the time library

raspPi = Board()         # Creates the main board object, named raspPi
raspPi.setupPin(3, True) # Sets up pin 3 for output
led = raspPi.pin(3)      # Creates a variable named led that has a pointer to the Pin class created by the Board class

try:                     # Will run this code unless an exception (error) is thrown
    while True:          # Loops until the task is killed
        led.turnOn()     # Turn the led on by turning on pin 3
        sleep(0.5)       # Waits for 500ms
        led.turnOff()    # Turn off the led by pulling pin 3 low
        sleep(0.5)       # Waits for 500ms
except KeyboardInturupt: # Catches if the users ends the script
    raspPi.cleanup()     # Cleans up the pins that were used for this program
```
