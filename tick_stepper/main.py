import time
import machine

stepPin = machine.Pin(8, machine.Pin.OUT)
dirPin = machine.Pin(20, machine.Pin.OUT)

MINVAL = 350
MAXVAL = 10000

start = time.ticks_us()
inter = 500
inter_p = 50.00
statePin = False

def scale_value(value, in_min, in_max, out_min, out_max):
  scaled_value = (value - in_min) * (out_max - out_min) / (in_max - in_min) + out_min
  return scaled_value

rescaled = int(scale_value(inter_p, 0, 100, MAXVAL, MINVAL))

def run():
    global statePin
    global start
    while True:
        now = time.ticks_us()
        if time.ticks_diff(now, start) > inter:
            print((time.ticks_diff(now, start))-inter)
            start = time.ticks_us()
            now = time.ticks_us()
            statePin = True if statePin == False else False
            stepPin.value(statePin)

if __name__ == "__main__":
    run()