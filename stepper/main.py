from stepper import Stepper
import machine
import time

s1 = Stepper(8,20,steps_per_rev=400,speed_sps=900, timer_id=0)
pos = 0

# s1.target(1500)
# print(s1.get_pos())
# time.sleep(2.0)
# print(s1.get_pos())
# s1.target(0)
# print(s1.get_pos())
# time.sleep(2.0)
# print(s1.get_pos())
# s1.free_run(-1)

s1.target(1500)
time.sleep(2.0)
s1.target(0)