# MIT License (MIT)
# Copyright (c) 2021 Mike Teachman
# https://opensource.org/licenses/MIT

# example for MicroPython rotary encoder
# - uasyncio implementation
# - 2 independent rotary encoders
# - register callbacks with the rotary objects
# - shows the use of an Observer pattern in Python

import sys
if sys.platform == 'esp8266' or sys.platform == 'esp32':
    from rotary_irq_esp import RotaryIRQ
elif sys.platform == 'pyboard':
    from rotary_irq_pyb import RotaryIRQ
elif sys.platform == 'rp2':
    from rotary_irq_rp2 import RotaryIRQ
else:
    print('Warning:  The Rotary module has not been tested on this platform')

import uasyncio as asyncio
import time
import machine

btn = machine.Pin(2, mode=machine.Pin.IN, pull=machine.Pin.PULL_UP)

def btnPress(pin):
    print('Button pressed')


# example of a class that uses one rotary encoder
class Application1():
    def __init__(self, r1):
        self.r1 = r1
        self.myevent = asyncio.Event()
        asyncio.create_task(self.action())
        r1.add_listener(self.callback)

    def callback(self):
        self.myevent.set()

    async def action(self):
        while True:
            await self.myevent.wait()
            print('App 1:  rotary 1 = {}'. format(self.r1.value()))
            # do something with the encoder result ...
            self.myevent.clear()

async def main():
    rotary_encoder_1 = RotaryIRQ(pin_num_clk=10,
                                 pin_num_dt=9,
                                 min_val=0,
                                 max_val=15,
                                 reverse=False,
                                 range_mode=RotaryIRQ.RANGE_WRAP)
    app1 = Application1(rotary_encoder_1)

    # keep the event loop active
    while True:
        await asyncio.sleep_ms(10)
        btn.irq(handler=btnPress, trigger=machine.Pin.IRQ_FALLING)

try:
    asyncio.run(main())
except (KeyboardInterrupt, Exception) as e:
    print('Exception {} {}\n'.format(type(e).__name__, e))
finally:
    ret = asyncio.new_event_loop()  # Clear retained uasyncio state
