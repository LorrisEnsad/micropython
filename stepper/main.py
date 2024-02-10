from stepper import Stepper
import time

s1 = Stepper(step_pin=8, dir_pin=20, steps_per_rev=200,speed_sps=50)

s1.speed(20)

print(s1.get_pos_deg())
s1.target_deg(360)
print(s1.get_pos_deg())
time.sleep(2)
s1.target_deg(-360)
print(s1.get_pos_deg())