led = machine.PWM(machine.Pin(7), freq=1000)
tr = machine.PWM(machine.Pin(5), freq=1000)
val = 3
minimum = 1
maximum = 40
amount = 3

delaymin = 2
delaymax = 10

while True:
    percent = int((val*65536) /100)
    print(percent)
    led.duty_u16(percent)
    tr.duty_u16(percent)
    val+=amount
    if val>=maximum or val<=minimum:
        amount*=-1
    time.sleep_ms(random.randint(delaymin,delaymax))