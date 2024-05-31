import machine
from machine import ADC
import time

MAX = 20
buffer = []

light = ADC(machine.Pin(1))
light.atten(ADC.ATTN_11DB) #full range 3.3V

for i in range(MAX):
    buffer.append(light.read())
    time.sleep(0.05)
print("done")