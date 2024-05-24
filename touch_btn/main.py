import machine
import time

light = machine.ADC(Pin(A0))
light.atten(ADC.ATTN_11DB) #full range 3.3V

while True:
    lightval = light.read()
    print(lightval)
    time.sleep(0.5)