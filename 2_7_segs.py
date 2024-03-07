import RPi.GPIO as GPIO
import time

# Pin Definitions for Shift Register 1
SDI_A = 11
RCLK_A = 12
SRCLK_A = 13

# Pin Definitions for Shift Register 2
SDI_B = 15
RCLK_B = 16
SRCLK_B = 18

# Define segment codes for numbers 0-9 (common anode)
segCode = [0x3F, 0x06, 0x5B, 0x4F, 0x66, 0x6D, 0x7D, 0x07, 0x7F, 0x6F]

# Define segment codes for alphabets A-Z (common anode)
alphaSegCode = [
    0x77, 0x7C, 0x39, 0x5E, 0x79, 0x71, 0x3D, 0x74, 0x06, 0x0E,
    0x1C, 0x38, 0x55, 0x54, 0x5C, 0x73, 0x67, 0x50, 0x6D, 0x78,
    0x3E, 0x1C, 0x55, 0x6E, 0x5B  # Adjusted to include necessary codes for A-Z
]

def print_msg():
    print('Program is running...')
    print('Please press Ctrl+C to end the program...')

def setup():
    GPIO.setmode(GPIO.BOARD)  # Number GPIOs by physical location
    GPIO.setup(SDI_A, GPIO.OUT)
    GPIO.setup(RCLK_A, GPIO.OUT)
    GPIO.setup(SRCLK_A, GPIO.OUT)
    GPIO.setup(SDI_B, GPIO.OUT)
    GPIO.setup(RCLK_B, GPIO.OUT)
    GPIO.setup(SRCLK_B, GPIO.OUT)
    GPIO.output(SDI_A, GPIO.LOW)
    GPIO.output(RCLK_A, GPIO.LOW)
    GPIO.output(SRCLK_A, GPIO.LOW)
    GPIO.output(SDI_B, GPIO.LOW)
    GPIO.output(RCLK_B, GPIO.LOW)
    GPIO.output(SRCLK_B, GPIO.LOW)

def hc595_shift(dat, reg):
    if reg == 'A':
        SDI, RCLK, SRCLK = SDI_A, RCLK_A, SRCLK_A
    elif reg == 'B':
        SDI, RCLK, SRCLK = SDI_B, RCLK_B, SRCLK_B

    for bit in range(7, -1, -1):  # Iterate over bits from MSB to LSB
        GPIO.output(SDI, not ((dat >> bit) & 0x01))  # Invert logic for common anode
        GPIO.output(SRCLK, GPIO.HIGH)
        time.sleep(0.001)
        GPIO.output(SRCLK, GPIO.LOW)
    GPIO.output(RCLK, GPIO.HIGH)
    time.sleep(0.001)
    GPIO.output(RCLK, GPIO.LOW)

def display_number(num):
    tens_digit = num // 10
    ones_digit = num % 10
    hc595_shift(segCode[tens_digit], 'A')  # Display tens digit on first display
    hc595_shift(segCode[ones_digit], 'B')  # Display ones digit on second display

def display_alphabet(alpha):
    alpha_index = ord(alpha.upper()) - ord('A')  # Convert alphabet to index (0-25)
    if 0 <= alpha_index < len(alphaSegCode):
        hc595_shift(alphaSegCode[alpha_index], 'A')  # Display alphabet on first display
        hc595_shift(0x00, 'B')  # Turn off second display
    else:
        hc595_shift(0x00, 'A')  # Turn off first display
        hc595_shift(0x00, 'B')  # Turn off second display

def loop():
    print_msg()
    while True:
        for i in range(26):  # Display numbers 0-25
            display_number(i)
            time.sleep(1)
        for alpha in range(ord('A'), ord('Z')+1):  # Display alphabets A-Z
            display_alphabet(chr(alpha))
            time.sleep(1)

def destroy():
    GPIO.cleanup()

setup()

try:
    loop()
except KeyboardInterrupt:
    destroy()