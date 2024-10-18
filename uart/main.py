# from machine import UART, Pin
import struct

# Configuration UART
# uart = UART(1, baudrate=420000, tx=Pin(21), rx=Pin(20), 
#            bits=8, parity=None, stop=1, timeout=100)

# ### record raw data
# while True:
#     f = open("log.txt", "w")
#     if uart.any():
#         data = uart.readline()
#         f.write(data)
#         print(data)