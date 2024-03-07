import RPi.GPIO as GPIO
import time

SDI = 11
RCLK = 12
SRCLK = 13
segCode = [0x40,0x79,0x24,0x30,0x19,0x12,0x02,0x78,0x00,0x10,0x88,0x83,0xC6,0xA1,0x86,0x8E,0xFF]

def print_msg():
    print('Program is running...')
    print('Please press Ctrl+C to end the program...')

def setup():
    GPIO.setmode(GPIO.BOARD) #Number GPIOs by its physical location
    GPIO.setup(SDI, GPIO.OUT)
    GPIO.setup(RCLK, GPIO.OUT)
    GPIO.setup(SRCLK, GPIO.OUT)
    GPIO.output(SDI, GPIO.LOW)
    GPIO.output(RCLK, GPIO.LOW)
    GPIO.output(SRCLK, GPIO.LOW)

def hc595_shift(dat):
    for bit in range(7, -1, -1):  # Iterate over bits from MSB to LSB
        GPIO.output(SDI, (dat >> bit) & 0x01)
        GPIO.output(SRCLK, GPIO.HIGH)
        time.sleep(0.001)
        GPIO.output(SRCLK, GPIO.LOW)
    GPIO.output(RCLK, GPIO.HIGH)
    time.sleep(0.001)
    GPIO.output(RCLK, GPIO.LOW)

def loop():
    while True:
        for i in range(len(segCode)):
            hc595_shift(segCode[i])
            time.sleep(1)

def destroy(): #When program ending, the function is executed.
    GPIO.cleanup()

print_msg()
setup()

try:
    loop()
except KeyboardInterrupt:
    destroy()
