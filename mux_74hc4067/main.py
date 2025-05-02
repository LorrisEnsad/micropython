from machine import Pin, ADC
from time import sleep

pin_s = [
    Pin(14, Pin.OUT),
    Pin(15, Pin.OUT),
    Pin(16, Pin.OUT),
    Pin(17, Pin.OUT) 
]
adc = ADC(Pin(28))

def select_channel(ch):
    for i in range(4):
        pin_s[i].value((ch >> i) & 1)

def read_ldr(ch):
    select_channel(ch)
    sleep(0.001)
    raw = adc.read_u16()
    voltage = raw * 3.3 / 65535
    return raw, voltage

while True:
    for ch in range(16):
        raw, volt = read_ldr(ch)
        print("LDR {:2d} → raw: {:5d}, V: {:.2f} V".format(ch, raw, volt))
    print("-"*10)
    sleep(1)
