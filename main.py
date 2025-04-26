# import required libraries
import RPi.GPIO as GPIO
import time
from enum import Enum, auto

class KeypadVal(Enum):
    ZERO = 0
    ONE = 1
    TWO = 2
    THREE = 3
    FOUR = 4
    FIVE = 5
    SIX = 6
    SEVEN = 7
    EIGHT = 8
    NINE = 9

    A = auto()
    B = auto()
    C = auto()
    D = auto()

    STAR = auto()
    HASH = auto()

SERVO_PIN = 2


OUT_PINS = [
    25, 8, 7, 1
]

IN_PINS = [
    12, 16, 20, 21
]


# Initialize the GPIO pins
GPIO.setwarnings(False)
GPIO.setmode(GPIO.BCM)

for i in OUT_PINS:
    GPIO.setup(i, GPIO.OUT)

# Make sure to configure the input pins to use the internal pull-down resistors
for i in IN_PINS:
    GPIO.setup(i, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)

GPIO.setup(SERVO_PIN, GPIO.OUT)
pwm = GPIO.PWM(SERVO_PIN, 50)

pwm.start(0)




# The readLine function implements the procedure discussed in the article
# It sends out a single pulse to one of the rows of the keypad
# and then checks each column for changes
# If it detects a change, the user pressed the button that connects the given line
# to the detected column

def set_angle(angle, pin):
	duty = angle / 18 + 2
	GPIO.output(pin, True)

	pwm.ChangeDutyCycle(duty)

	time.sleep(1)

	GPIO.output(pin, False)

	pwm.ChangeDutyCycle(0)


def read_line(line):
    out = -1
    GPIO.output(line, GPIO.HIGH)

    for i,v in enumerate(IN_PINS):
        if(GPIO.input(v) == 1):
            out = i

    GPIO.output(line, GPIO.LOW)
    return (out != -1, out)

key_matrix = [
    [KeypadVal.ONE, KeypadVal.TWO, KeypadVal.THREE, KeypadVal.A],
    [KeypadVal.FOUR, KeypadVal.FIVE, KeypadVal.SIX, KeypadVal.B],
    [KeypadVal.SEVEN, KeypadVal.EIGHT, KeypadVal.NINE, KeypadVal.C],
    [KeypadVal.STAR, KeypadVal.ZERO, KeypadVal.HASH, KeypadVal.D]
]

last_captured = None
entered = []

def lock_servo():
    set_angle(180, SERVO_PIN)

def unlock_servo():
    set_angle(90, SERVO_PIN)

lock_servo()

try:
    while True:
        for i,v in enumerate(OUT_PINS):
            has_read, val_read = read_line(v)
            if has_read:
                # key captured
                # print(has_read, i, val_read)
                captured = key_matrix[i][val_read]

                if (captured == KeypadVal.A):
                    unlock_servo()
                elif (captured == KeypadVal.B):
                    lock_servo()
                elif (captured != last_captured):
                    entered.append(captured.value)
                
                last_captured = captured
        print(entered)

        time.sleep(0.1)
except KeyboardInterrupt:
    print("\nApplication stopped!")
