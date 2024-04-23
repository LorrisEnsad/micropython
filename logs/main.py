import machine, time, random

btn = machine.Pin(0, mode=machine.Pin.IN, pull=machine.Pin.PULL_UP)

def count_ms():
    global new_time
    t = time.ticks_ms()
    new_time = time.ticks_diff(t, start)
    return new_time

start = time.ticks_ms()
new_time = 0
btnPrevState = 0

f = open("log.txt", "w")
s = "boot , "
count_ms()
s+=str(random.randint(0, 100))
s+="\n"
f.write(s)
f.close()

def writeFile(string):
    f = open("log.txt", "a")
    f.write(string)
    f.close()

while True:
    if btn.value()==0 and btnPrevState!=btn.value() :
        btnPrevState = btn.value()
        s = "action , "
        count_ms()
        s+=str(new_time)
        s+="\n"
        writeFile(s)
        print(s)
    btnPrevState = btn.value()