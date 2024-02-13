from time import ticks_diff, ticks_us
from machine import Pin

class Stepper:
    def __init__(self, stepPin, stepDir, maxStepSpeed=)

        self.stepPin = Pin(stepPin, Pin.OUT)
        self.dirPin = Pin(dirPin, Pin.OUT)
        self.MAXSTEPSPEED = 400
        self.MINSTEPSPEED = 10000
        self.start = ticks_us()
        self.now = ticks_us()
        self.target = 0
        self.isTurning=False
        self.stateStepPin = False
        self.stateDirPin = False

    def rescaled_value(self, value, in_min, in_max, out_min, out_max):
        scaled_value = (value - in_min) * (out_max - out_min) / (in_max - in_min) + out_min
        return scaled_value

    def get_stateStepPin(self):
        return self.stateStepPin
        
    def get_stateDirPin(self):
        return self.stateDirPin

    def set_stateStepPin(self, val):
        self.stateStepPin = val
        
    def set_stateDirPin(self, val):
        self.stateDirPin = val