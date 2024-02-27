from machine import Pin, ADC
from time import sleep

pot = ADC(Pin(3))
# pot.atten(ADC.ATTN_11DB)

while True:
    pot_val = pot.read()
    print(pot_val)
    sleep(0.1)