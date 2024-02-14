'''
upwmcontroller.py, A MicroPython library for controlling PWM outputs

Copyright (C) 2019, Sean Lanigan

uPWMController is free software: you can redistribute it and/or modify 
it under the terms of the GNU Lesser General Public License as published by 
the Free Software Foundation, either version 3 of the License, or (at your 
option) any later version.

uPWMController is distributed in the hope that it will be useful, but WITHOUT 
ANY WARRANTY; without even the implied warranty of MERCHANTABILITY or FITNESS 
FOR A PARTICULAR PURPOSE.  See the GNU Lesser General Public License for more 
details.

You should have received a copy of the GNU Lesser General Public License along 
with uPWMController.  If not, see <https://www.gnu.org/licenses/>.
'''
import machine
import time
from micropython import const
import uasyncio as asyncio


delay_idle = const(10)
delay_run  = const(1)
step_width = const(3)
left_shift = const(2)

## TODO: If running at high frequency, could do a sequence of 5/5 at one duty, then 4/5 at the next duty, etc
class uPWMController:
    def __init__(self, pwm=None):
        # Allow initialisation without a pin being specified
        self._pwm = None
        self._duty_goal = 0
        self._fade_run = False

        if pwm:
            self.set_pin(pwm)
    
    def set_pin(self, pwm):
        if not isinstance(pwm, machine.PWM):
            raise TypeError("pwm must be a machine.PWM instance")
        # Deconfigure an already initialised pin, if there is one
        if self._pwm:
            try:
                self._pwm.deinit()
            except:
                pass
        # Store the new PWM instance
        self._pwm = pwm
        
    def set_duty_immediate(self, duty):
        if not isinstance(duty, int):
            raise TypeError("duty must be an integer")
        if self._pwm:
            self._pwm.duty(duty)
        else:
            raise PinNotSet("set_duty_immediate() called before a PWM pin has been set")
    
    def set_duty(self, duty, fadetime=200):
        if not isinstance(duty, int):
            raise TypeError("duty must be an integer")
        # Use a left-shift, to allow for longer fade times which need several steps at one PWM duty
        duty = duty << left_shift
        self._duty_goal = duty
        # Calculate the duty steps based on the fade time
        duty_now = (self._pwm.duty() << left_shift)
        num_steps = int(fadetime / step_width)
        step_duty = int((duty - duty_now) / num_steps)
        # Special handling in case step_duty is rounded to zero
        if step_duty == 0:
            if duty_now > duty:
                step_duty = -1
            else:
                step_duty = 1
        self._step_time_next = time.ticks_ms() + step_width
        self._step_duty_next = duty_now
        self._step_duty = step_duty
        self._fade_run = True
    
    async def run(self):
        while True:
            if self._fade_run and self._pwm:
                # Process the fade routine
                if time.ticks_ms() > self._step_time_next:
                    step_duty = self._step_duty
                    duty_next = self._step_duty_next + step_duty
                    duty_goal = self._duty_goal
                    # Check if target is passed yet
                    if (step_duty > 0 and duty_next > duty_goal) or \
                       (step_duty < 0 and duty_next < duty_goal):
                        # If it is passed, set the duty to the goal, and stop
                        duty_next = duty_goal
                        self._fade_run = False
                        ## TODO: Send some kind of signal here that fade is done
                    else:
                        # Otherwise, set duty to the next step
                        self._step_time_next += step_width
                        self._step_duty_next = duty_next
                    # Update the duty to the actual pin
                    # Take off the left-shift at this point
                    duty_next = duty_next >> left_shift
                    self._pwm.duty(duty_next)
                
                # Regardless of if duty was changed, sleep for a short time
                await asyncio.sleep_ms(delay_run)
            
            else:
                # Nothing is happening, can sleep for a bit longer
                await asyncio.sleep_ms(delay_idle)


class PinNotSet(Exception):
    pass
