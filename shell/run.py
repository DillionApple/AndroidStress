from __future__ import print_function

import os
import sys
import time
import datetime

def run_cpu_stress(tn, tp):
    print("[Run CPU Stress]")
    cmd = "adb shell am broadcast -a com.dillionmango.stress.set_stress --ei cpu_stress_thread_number {0} --ei cpu_stress_thread_priority {1}".format(tn, tp)
    print(cmd)
    os.system(cmd)

def run_memory_stress(mb):
    print("[Run Memory Stress]")
    cmd = "adb shell am broadcast -a com.dillionmango.stress.set_stress --ei memory_stress {0}".format(mb)
    print(cmd)
    os.system(cmd)

def run_disk_write_stress(tn, bs, st):
    print("[Run Disk Write Stress]")
    cmd = "adb shell am broadcast -a com.dillionmango.stress.set_stress --ei disk_write_stress_thread_number {0} --ei disk_write_stress_buffer_size {1} --ei disk_write_stress_sleep_time {2}".format(tn, bs, st)
    print(cmd)
    os.system(cmd)

def run_disk_read_stress(tn, bs, st):
    print("[Run Disk Read Stress]")
    cmd = "adb shell am broadcast -a com.dillionmango.stress.set_stress --ei disk_read_stress_thread_number {0} --ei disk_read_stress_buffer_size {1} --ei disk_read_stress_sleep_time {2}".format(tn, bs, st)
    print(cmd)
    os.system(cmd)

def run_empty_stress():
    print("[Run Empty Stress]")
    cmd = "adb shell am broadcast -a com.dillionmango.stress.set_stress"
    print(cmd)
    os.system(cmd)

def tap_the_device():
    print("[Start Tapping Device]")
    tap_time_list = []
    for i in range(1000):
        startTime = time.time()
        os.system("adb shell input tap 10 100")
        endTime = time.time()

        s = "{0},".format(endTime - startTime)
        f.write(s)
        print(s)
        tap_time_list.append(endTime - startTime)

    s = "max {0},".format(max(tap_time_list))
    f.write(s)
    print(s)

    s = "avg {0},".format(sum(tap_time_list)/len(tap_time_list))
    f.write(s)
    print(s)

    sorted_tap_time_list = sorted(tap_time_list)
    f.write("sorted:,")
    for each in sorted_tap_time_list:
        f.write("{0},".format(each))
    
    f.write("\n")

def top_the_device():
    print("[Start Topping Device]")
    cmd = "adb shell top -n 5 | grep stress"
    print(cmd)
    os.system(cmd)

def test_stress():
    # CPU
    run_cpu_stress(4, 10)
    top_the_device()

    # Memory
    run_memory_stress(100)
    top_the_device()

    # Disk Write
    run_disk_write_stress(1, 4096, 0)
    top_the_device()

    # Disk Read
    run_disk_read_stress(1, 4096, 0)
    top_the_device()

def cpu_stress_routine(test=False):

    if not test:
        priorities = [1, 5, 10]    
        max_thread_number={1: 64, 5: 64, 10: 16}
    else:
        priorities = [10]
        max_thread_number={10: 1}
    
    for i in priorities:
        for j in range(1, max_thread_number[i]+1):
            run_cpu_stress(j, i)
            time.sleep(15)

            s = "tn{0} tp{1},".format(j, i)
            f.write(s)
            print(s)

            if (not test):
                tap_the_device()
            else:
                top_the_device()

            run_empty_stress()
            time.sleep(5)
            
        f.write("\n")

def memory_stress_routine(test):

    if (not test):
        MAX_MEMORY = 500 # in MB
        STEPS = 10
        memory_to_occupy = 0
    else:
        MAX_MEMORY = 500
        STEPS = 0
        memory_to_occupy = 100

    for i in range(STEPS+1):
        run_memory_stress(memory_to_occupy)
        time.sleep(10)
    
        s = "memory{0},".format(memory_to_occupy)
        f.write(s)
        print(s)

        if (not test):
            tap_the_device()
            memory_to_occupy += MAX_MEMORY / STEPS
        else:
            top_the_device()

        run_empty_stress()
        time.sleep(5)
    
    f.write("\n")
    
# Disk Write Stress
# thread 1
# buffer size from 2^0 to 2^14
# sleep time from 0, 10, 100, 1000

def disk_write_stress_routine(test):
    
    if (not test):
        BS_STEPS = 15 # buffer size from 2^0 to 2^14
        ST_STEPS = 4  # sleep time from 0, 10, 100, 1000
        buffer_size = 1
    else:
        BS_STEPS = 1
        ST_STEPS = 1
        buffer_size = 4096
        
    for i in range(BS_STEPS):
        sleep_time = 0
        for j in range(ST_STEPS):
            run_disk_write_stress(1, buffer_size, sleep_time)
            time.sleep(3)

            s = "disk_wbs{0} disk_wst{1},".format(buffer_size, sleep_time)
            f.write(s)
            print(s)

            if (not test):
                tap_the_device()
            else:
                top_the_device()
                
            if (sleep_time == 0):
                sleep_time = 10
            else:
                sleep_time *= 10

            run_empty_stress()
            time.sleep(5)

        buffer_size *= 2
        f.write("\n")

# Disk Read Stress
# thread 1
# buffer size from 2^0 to 2^14
# sleep time from 0, 10, 100, 1000

def disk_read_stress_routine(test):

    if (not test):
        BS_STEPS = 15 # buffer size from 2^0 to 2^14
        ST_STEPS = 4  # sleep time from 0, 10, 100, 1000
        buffer_size = 1
    else:
        BS_STEPS = 1
        ST_STEPS = 1
        buffer_size = 4096
    
    for i in range(BS_STEPS):
        sleep_time = 0
        for j in range(ST_STEPS):
            run_disk_read_stress(1, buffer_size, sleep_time)
            time.sleep(3)

            s = "disk_rbs{0} disk_rst{1},".format(buffer_size, sleep_time)
            f.write(s)
            print(s)

            if (not test):
                tap_the_device()
            else:
                top_the_device()
                
            if (sleep_time == 0):
                sleep_time = 10
            else:
                sleep_time *= 10

            run_empty_stress()
            time.sleep(5)

        buffer_size *= 2
        f.write("\n")

func_dict = {
    'run_stress_test': test_stress,
    'cpu': cpu_stress_routine,
    'memory': memory_stress_routine,
    'disk_write': disk_write_stress_routine,
    'disk_read': disk_read_stress_routine    
}

if __name__ == "__main__":

    test_flag = False

    file_name_prefix = "result_"

    file_name = file_name_prefix + str(datetime.datetime.today()) + '.csv'
    

    functions = []

    for each in sys.argv[1:]:
        if each == '--test':
            test_flag = True
        function = func_dict.get(each)
        if function != None:
            functions.append(function)

    if test_flag == True:
        file_name = file_name + '.test'
        
    f = open(file_name, "w")

    for each in functions:
        each(test_flag)

    f.close()
