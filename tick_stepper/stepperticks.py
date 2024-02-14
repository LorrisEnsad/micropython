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
        self.actualPosition = 0
        self.targetPosition = 0
        self.isTurning=False
        self.actualSpeed = 800
        self.stateStepPin = False
        self.stateDirPin = False

    def rescaled_value(self, value, in_min, in_max, out_min, out_max):
        scaled_value = (value - in_min) * (out_max - out_min) / (in_max - in_min) + out_min
        return scaled_value

    def get_stateStepPin(self):
        return self.stateStepPin
        
    def get_stateDirPin(self):
        return self.stateDirPin

    def get_target(self):
        return self.targetPosition

    def set_stateStepPin(self, val):
        self.stateStepPin = val
        
    def set_stateDirPin(self, val):
        self.stateDirPin = val
    
    def set_target(self, val):
        self.targetPosition = val

    def is_turning(self):
        return self.isTurning

    def run(self):
        start = ticks_us()
        while self.actualPosition != self.targetPosition
            self.isTurning = True if isTurning == False else False
            now = ticks_us()
            if ticks_diff(now, start) > actualSpeed:
                now = ticks_us()
                start = ticks_us()
                stateStepPin = True if stateStepPin == False else False
                self.stepPin.value(self.stateStepPin) 