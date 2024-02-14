'''
main.py - An example MicroPython project, using the uPWMController library. 

This example code is dedicated to the public domain. To the extent possible 
under law, Sean Lanigan has waived all copyright and related or neighbouring 
rights to "main.py". This work is published from: Australia. 

https://creativecommons.org/publicdomain/zero/1.0/
'''
import uasyncio as asyncio
import machine

from upwmcontroller import uPWMController, PinNotSet


async def run_once(led1, led2):
    led1.set_duty_immediate(0)
    led2.set_duty_immediate(0)
    print("Setting duty to 0")
    await asyncio.sleep_ms(50)

    print("Setting duty to 1023, with a fade time of 500 ms")
    led1.set_duty(1023, fadetime=500)
    led2.set_duty(1023, fadetime=500)
    await asyncio.sleep(2)

    print("Setting duty to 0, with a fade time of 500 ms")
    led1.set_duty(0, fadetime=500)
    led2.set_duty(0, fadetime=500)

    await asyncio.sleep(2)

    print("Setting duty to 1023, with a fade time of 5000 ms")
    led1.set_duty(1023, fadetime=5000)
    led2.set_duty(1023, fadetime=5000)
    await asyncio.sleep(10)

    print("Setting duty to 0, with a fade time of 5000 ms")
    led1.set_duty(0, fadetime=5000)
    led2.set_duty(0, fadetime=5000)

    await asyncio.sleep(10)
    print("Fade done")


def main():
    # Instantiate the controller instances
    led1 = uPWMController(machine.PWM(machine.Pin(17), duty=0))
    led2 = uPWMController(machine.PWM(machine.Pin(18), duty=0))

    # Get a reference to the event loop
    loop = asyncio.get_event_loop()
    # Create instances of the background coroutine
    led1_coro = asyncio.coroutine(led1.run())
    led2_coro = asyncio.coroutine(led2.run())
    # Schedule the coroutines to run ASAP
    loop.create_task(led1_coro)
    loop.create_task(led2_coro)
    # Run the event loop, waiting for the 'run_once' function to finish
    loop.run_until_complete(run_once(led1, led2))

    # Cancel the coroutine and clean up the loop
    asyncio.cancel(led1_coro)
    asyncio.cancel(led2_coro)
    loop.close()


if __name__ == '__main__':
    main()
