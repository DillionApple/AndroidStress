from __future__ import print_function

import os
import sys
import time
import datetime
import multiprocessing
import signal


stress_processes = []

def run_cmd(cmd):
    print("[Run CMD: {0}]".format(cmd))
    os.system(cmd)

def run_cpu_stress(tn, tp):
    print("[Run CPU Stress]")
    cmd = "adb shell am broadcast -a com.dillionmango.stress.set_stress --ei cpu_stress_thread_number {0} --ei cpu_stress_thread_priority {1}".format(tn, tp)
    run_cmd(cmd)

def run_memory_stress(mb):
    print("[Run Memory Stress]")
    cmd = "adb shell am broadcast -a com.dillionmango.stress.set_stress --ei memory_stress {0}".format(mb)
    run_cmd(cmd)

# bolck_size if one of 4 16 64 256 1024 4096
# load is from >0 to <=100
def run_disk_write_stress(block_size, load):
    print("[Run Disk Write Stress bs{0}, ld{1}]".format(block_size, load))
    img_file_name = "W_{0}K.img".format(block_size)
    while (True):
        start_time = time.time() # in seconds
        run_cmd("adb push {0} /storage/sdcard0/".format(img_file_name))
        end_time = time.time() # in seconds
        period = end_time - start_time # in seconds
        sleep_time = (100 - load) * period / load
        if sleep_time > 0:
            time.sleep(sleep_time)

# bolck_size if one of 4 16 64 256 1024 4096
# load is from >0 to <=100
def run_disk_read_stress(block_size, load):
    print("[Run Disk Read Stress bs{0}, ld{1}]".format(block_size, load))
    img_file_name = "R_{0}K.img".format(block_size)
    while (True):
        start_time = time.time() # in seconds
        run_cmd("adb pull /storage/sdcard0/{0} ~/".format(img_file_name))
        end_time = time.time() # in seconds
        period = end_time - start_time # in seconds
        sleep_time = (100 - load) * period / load
        if sleep_time > 0:
            time.sleep(sleep_time)

def clear_stress():
    
    global stress_processes
    
    print("[Clear Stress]")    
    cmd = "adb shell am broadcast -a com.dillionmango.stress.set_stress"
    run_cmd(cmd)

    for process in stress_processes:
        process.terminate()

def tap_the_device():
    print("[Start Tapping Device]")
    tap_time_list = []
    for i in range(200):
        startTime = time.time()
        os.system("adb shell input tap 10 100")
        endTime = time.time()

        s = "{0},".format(endTime - startTime)
        f.write(s)
        print("[Tap time: {0}]".format(s))
        tap_time_list.append(endTime - startTime)

    s = "max {0},".format(max(tap_time_list))
    f.write(s)

    s = "avg {0},".format(sum(tap_time_list)/len(tap_time_list))
    f.write(s)

    sorted_tap_time_list = sorted(tap_time_list)
    f.write("sorted:,")
    for each in sorted_tap_time_list:
        f.write("{0},".format(each))
    
    f.write("\n")
    print('[End Tapping Device]')

def top_the_device():
    print("[Start Topping Device]")
    cmd = "adb shell top -n 5 -m 10"
    run_cmd(cmd)

def test_stress():
    # CPU
    run_cpu_stress(4, 10)
    top_the_device()

    # Memory
    run_memory_stress(100)
    top_the_device()

    # Disk Write
    run_disk_write_stress(4096, 100)
    top_the_device()

    # Disk Read
    run_disk_read_stress(4096, 100)
    top_the_device()

def cpu_stress_routine():
    
    priorities = [1, 5, 10]
    max_thread_number={1: 64, 5: 64, 10: 16}
    thread_number_steps={1: 8, 5: 4, 10: 2}
    
    for i in priorities:
        thread_number = thread_number_steps[i]
        while (thread_number <= max_thread_number[i]):
            run_cpu_stress(thread_number, i)
            time.sleep(10)

            s = "tn{0} tp{1},".format(thread_number, i)
            f.write(s)
            print(s)

            tap_the_device()

            clear_stress()
            time.sleep(5)

            thread_number += thread_number_steps[i]
            
        f.write("\n")

def memory_stress_routine():

    MAX_MEMORY = 500 # in MB, change this
    STEPS = 5
    memory_to_occupy = MAX_MEMORY / STEPS

    for i in range(STEPS):
        run_memory_stress(memory_to_occupy)
        time.sleep(10)
    
        s = "memory{0},".format(memory_to_occupy)
        f.write(s)
        print(s)

        tap_the_device()

        clear_stress()
        time.sleep(5)

        memory_to_occupy += MAX_MEMORY / STEPS
    
    f.write("\n")
    
# Disk Write Stress
# file block size is 4 16 64 256 1024 4096 K
# load is from >0 to <=100

def disk_write_stress_routine():

    global stress_processes
    
    BK_STEPS = 1
    LD_STEPS = 10
    file_block_size = 256 # in K
        
    for i in range(BK_STEPS):
        load = 10
        for j in range(LD_STEPS):
            process = multiprocessing.Process(target=run_disk_write_stress, args=(file_block_size, load))
            process.start()
            stress_processes.append(process)
            time.sleep(0.1)
            s = "disk_wbs{0} disk_wld{1},".format(file_block_size, load)
            f.write(s)
            print(s)
            
            tap_the_device()

            load += 10

            clear_stress()
            time.sleep(0.1)

        file_block_size *= 4
        f.write("\n")

# Disk Write Stress
# file block size is 4 16 64 256 1024 4096 K
# load is from >0 to <=100

def disk_read_stress_routine():

    global stress_should_run
    
    BK_STEPS = 1
    LD_STEPS = 10
    file_block_size = 256 # in K
        
    for i in range(BK_STEPS):
        load = 10
        for j in range(LD_STEPS):
            process = multiprocessing.Process(target=run_disk_read_stress, args=(file_block_size, load))
            process.start()
            stress_processes.append(process)
            time.sleep(0.1)
            s = "disk_rbs{0} disk_rld{1},".format(file_block_size, load)
            f.write(s)
            print(s)

            tap_the_device()
                
            load += 10

            clear_stress()
            time.sleep(0.1)

        file_block_size *= 4
        f.write("\n")

func_dict = {
    'run_stress_test': test_stress,
    'cpu': cpu_stress_routine,
    'memory': memory_stress_routine,
    'disk_write': disk_write_stress_routine,
    'disk_read': disk_read_stress_routine
}

def terminate_program(a, b):
    clear_stress()
    exit(0)

if __name__ == "__main__":

    signal.signal(signal.SIGINT, terminate_program)
    signal.signal(signal.SIGTERM, terminate_program)

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
        each()

    f.close()
