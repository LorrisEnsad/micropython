import machine, time

btn = machine.Pin(2, mode=machine.Pin.IN, pull=machine.Pin.PULL_UP)

def t(pin):
    print('hey')

while True:
    btn.irq(handler=t, trigger=machine.Pin.IRQ_FALLING)