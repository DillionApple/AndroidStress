from __future__ import print_function

import os
import time

max_thread_number={1: 64, 5: 64, 10: 16}

f = open("result_11-15-23:32.csv", "w")

def tap_the_device():
    for i in range(50):
        startTime = time.time()
        os.system("adb shell input tap 10 100")
        endTime = time.time()

        s = "{0},".format(endTime - startTime)
        f.write(s)
        print(s)

    f.write("\n")

# CPU Stress
"""
for i in [1]:
    for j in range(1, max_thread_number[i]+1):
        os.system("adb shell am broadcast -a com.dillionmango.stress.set_stress --ei cpu_stress_thread_number {0} --ei cpu_stress_thread_priority {1}".format(j, i))
        time.sleep(15)

        s = "tn{0} tp{1},".format(j, i)
        f.write(s)
        print(s)

        for k in range(15):
            startTime = time.time()
            os.system("adb shell input tap 10 100")
            endTime = time.time()

            s = "{0},".format(endTime - startTime)
            f.write(s)
            print(s)

            time.sleep(1);
        f.write("\n")        
"""

# Memory Stress

MAX_MEMORY = 500 # in MB

STEPS = 10

memory_to_occupy = 0

for i in range(STEPS+1):
    os.system("adb shell am broadcast -a com.dillionmango.stress.set_stress --ei memory_stress {0}".format(memory_to_occupy))
    time.sleep(5)
    
    s = "memory{0},".format(memory_to_occupy)
    f.write(s)
    print(s)

    tap_the_device()

    os.system("adb shell am broadcast -a com.dillionmango.stress.set_stress")
    time.sleep(5)
    
    memory_to_occupy += MAX_MEMORY / STEPS

# Disk Read Stress
# thread 1
# buffer size from 2^0 to 2^12
# sleep time from 0, 10, 100, 1000

buffer_size = 1
for i in range(13):
    sleep_time = 0
    for j in range(4):
        os.system("adb shell am broadcast -a com.dillionmango.stress.set_stress --ei disk_wtn 1 --ei disk_wbs {0} --ei disk_wst {1}".format(buffer_size, sleep_time))
        time.sleep(3)

        s = "disk_wbs{0} disk_wst{1},".format(buffer_size, sleep_time)
        f.write(s)
        print(s)
        
        tap_the_device()
        
        if (sleep_time == 0):
            sleep_time = 10
        else:
            sleep_time *= 10

    buffer_size *= 2

# Disk Read Stress
# thread 1
# buffer size from 2^0 to 2^12
# sleep time from 0, 10, 100, 1000

buffer_size = 1
for i in range(13):
    sleep_time = 0
    for j in range(4):
        os.system("adb shell am broadcast -a com.dillionmango.stress.set_stress --ei disk_rtn 1 --ei disk_rbs {0} --ei disk_rst {1}".format(buffer_size, sleep_time))
        time.sleep(3)

        s = "disk_rbs{0} disk_rst{1},".format(buffer_size, sleep_time)
        f.write(s)
        print(s)
        
        tap_the_device()
        
        if (sleep_time == 0):
            sleep_time = 10
        else:
            sleep_time *= 10

    buffer_size *= 2

f.close()
