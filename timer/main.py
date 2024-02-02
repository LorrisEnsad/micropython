import machine

led = machine.Pin(21, machine.Pin.OUT)

def ToggleLed(timer):
    led.toggle()

timer = machine.Timer()
timer.init(period=1000, mode=machine.Timer.PERIODIC, callback=ToggleLed)

# timer.deinit()
# timer.start()
# timer.stop()