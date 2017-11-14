from __future__ import print_function

import os
import time

max_thread_number={1: 64, 5: 64, 10: 16}

f = open("result.csv", "w")

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
        
