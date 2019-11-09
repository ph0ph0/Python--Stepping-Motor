import RPi.GPIO as GPIO
import time

motorPins = (12, 16, 18, 22) #define pins connected to four phase ABCD of stepper motor

CCWStep = (0x01, 0x02, 0x04, 0x08) #define power supply order for coil rotating anticlockwise

CWStep = (0x08, 0x04, 0x02, 0x01) #define power supply order for coil rotating clockwise

def setup():
    print('Program is starting...')
    GPIO.setmode(GPIO.BOARD)
    for pin in motorPins:
        GPIO.setup(pin, GPIO.OUT)

# For a four phase stepping motor, four steps are a cycle. This function is used to drive the stepping motor clockwise or
# anticlockwise to take four steps
def moveOnePeriod(direction, ms):
    print('Moving one period')
    for j in range(0, 4, 1): #cycle for power supply order
        print('period ', j)
        for i in range(0, 4, 1): #assign to each pin, total of 4
            if (direction == 1): #power supply order anticlockwise
                print('direction was clockwise')
                GPIO.output(motorPins[i], ((CCWStep[j] == 1 << i) and GPIO.HIGH or GPIO.LOW))
            else:
                print('direction was anticlockwise')
                GPIO.output(motorPins[i], ((CWStep[j] == 1 << i) and GPIO.HIGH or GPIO.LOW))
        if (ms < 3): #The delay can not be less than 3 ms, otherwise it will exceed speed limit of motor
            print('ms was less than 3', ms)
            ms = 3
        time.sleep(ms * 0.001)

# Continuous rotation function, the parameter steps specify the rotation cycles, every four steps is a cycle.
def moveSteps(direction, ms, steps):
    print('Moving steps')
    for i in range(steps):
        moveOnePeriod(direction, ms)

# function used to stop rotating
def motorStop():
    print('Stopping motor')
    for i in range(0, 4, 1):
        GPIO.output(motorPins[i], GPIO.LOW)

def loop():
    while True:
        moveSteps(1, 3, 512) #rotating 360 degrees clockwise, total of 2048 steps in a circle (512 cycles)
        time.sleep(0.5)
        moveSteps(0, 3, 512) #rotating 360 degrees anticlockwise
        time.sleep(0.5)

def destroy():
    GPIO.cleanup()

if __name__ == '__main__':
    setup()
    try:
        loop()
    except KeyboardInterrupt:
        destroy()




