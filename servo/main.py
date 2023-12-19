import time
from servo import Servo

servo = Servo(pin_id=0)

servo.write(0)
time.sleep(1)
servo.write(45)
time.sleep(1)
servo.write(90)
time.sleep(1)
servo.write(180)
time.sleep(1)
servo.write(0)