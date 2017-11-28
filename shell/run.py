from __future__ import print_function

import os
import sys
import time
import datetime
import multiprocessing
import signal
import subprocess


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
def run_disk_write_stress(filename, load):
    print("[Run Disk Write Stress bs{0}, ld{1}]".format(filename, load))
    while (True):
        start_time = time.time() # in seconds
        run_cmd("adb push {0} /storage/sdcard0/".format(filename))
        end_time = time.time() # in seconds
        period = end_time - start_time # in seconds
        sleep_time = (100 - load) * period / load
        if sleep_time > 0:
            time.sleep(sleep_time)

def run_disk_write_stress2(buffer_size, sleep_time, thread_number = 1):
    print("[Run Disk Write Stress 2 bs{0}, st{1}".format(buffer_size, sleep_time))
    cmd = "adb shell am broadcast -a com.dillionmango.stress.set_stress --ei disk_write_stress_thread_number {0} --ei disk_write_stress_buffer_size {1} --ei disk_write_stress_sleep_time {2}".format(thread_number, buffer_size, sleep_time)
    run_cmd(cmd)

def run_disk_jni_write_stress(buffer_size, thread_number = 1):
    print("[Run Disk Write JNI Stress tn{0} bs{1}]".format(thread_number, buffer_size))
    cmd = "adb shell am broadcast -a com.dillionmango.stress.set_stress --ei disk_jni_write_stress_thread_number {0} --ei disk_jni_write_stress_buffer_size {1}".format(thread_number, buffer_size)
    run_cmd(cmd)

# bolck_size if one of 4 16 64 256 1024 4096
# load is from >0 to <=100
def run_disk_read_stress(filename, load):
    print("[Run Disk Read Stress bs{0}, ld{1}]".format(filename, load))
    while (True):
        start_time = time.time() # in seconds
        run_cmd("adb pull /storage/sdcard0/{0} ~/".format(filename))
        end_time = time.time() # in seconds
        period = end_time - start_time # in seconds
        sleep_time = (100 - load) * period / load
        if sleep_time > 0:
            time.sleep(sleep_time)

def run_disk_read_stress2(buffer_size, sleep_time, thread_number = 1):
    print("[Run Disk Read Stress 2 bs{0}, st{1}".format(buffer_size, sleep_time))
    cmd = "adb shell am broadcast -a com.dillionmango.stress.set_stress --ei disk_read_stress_thread_number {0} --ei disk_read_stress_buffer_size {1} --ei disk_read_stress_sleep_time {2}".format(thread_number, buffer_size, sleep_time)
    run_cmd(cmd)

def run_disk_jni_read_stress(buffer_size, thread_number = 1):
    print("[Run Disk Read JNI Stress tn{0}, bs{1}]".format(thread_number, buffer_size))
    cmd = "adb shell am broadcast -a com.dillionmango.stress.set_stress --ei disk_jni_read_stress_thread_number {0} --ei disk_jni_read_stress_buffer_size {1}".format(thread_number, buffer_size)
    run_cmd(cmd)

def run_network_stress(thread_number):
    print("[Run Network Stress tn{0}]".format(thread_number))
    cmd = "adb shell am broadcast -a com.dillionmango.stress.set_stress --ei network_stress_thread_number {0}".format(thread_number)
    run_cmd(cmd)

def clear_stress():
    
    global stress_processes
    
    print("[Clear Stress]")
    cmd = "adb shell am broadcast -a com.dillionmango.stress.set_stress"
    run_cmd(cmd)
    time.sleep(1)
    cmd = "adb shell am start -n com.dillionmango.stress/.MainActivity"
    run_cmd(cmd)

    for process in stress_processes:
        process.terminate()

def tap_the_device(record_memory = False):
    TAP_TIMES = 50
    print("[Start Tapping Device]")
    tap_time_list = []
    f.write("\n")
    f.write("result:,")
    pre_occupied_memory = 1024000000
    for i in range(TAP_TIMES):
        if (record_memory):
            proc = subprocess.Popen(["adb shell cat /proc/meminfo"], stdout=subprocess.PIPE, shell=True)
            (out, err) = proc.communicate()
            l = out.split()

            total_memory = int(l[l.index("MemTotal:") + 1]) # in KB
            free_memory = int(l[l.index("MemFree:") + 1])
            total_swap = int(l[l.index("SwapTotal:") + 1])
            free_swap = int(l[l.index("SwapFree:") + 1])
            occupied_memory = total_memory - free_memory
            occupied_swap = total_swap - free_swap
            occupied_memory_percentage = (1.0 * occupied_memory) / (1.0 * total_memory)
            occupied_swap_percentage = (1.0 * occupied_swap) / (1.0 * total_swap)

            if (pre_occupied_memory - occupied_memory > 409600): # 400M
                f.write("---------- restart app ----------\n")

            pre_occupied_memory = occupied_memory
            
            s = "{0},{1},{2},{3},".format(occupied_memory, occupied_memory_percentage, occupied_swap, occupied_swap_percentage)
            f.write(s)
            f.flush()
            print("[Memory: {0}]".format(s))

        startTime = time.time()
        os.system("adb shell input tap 10 100")
        endTime = time.time()

        s = "{0},".format(endTime - startTime)
        f.write(s)
        if (record_memory):
            f.write("\n")
        f.flush()
        print("[Tap time: {0} {1}/{2}]".format(s, i+1, TAP_TIMES))
        tap_time_list.append(endTime - startTime)

    f.write("\n")
    s = "max {0},".format(max(tap_time_list))
    f.write(s)
    s = "avg {0},".format(sum(tap_time_list)/len(tap_time_list))
    f.write(s)

    f.write("\n")
    sorted_tap_time_list = sorted(tap_time_list)
    f.write("sorted:,")
    for each in sorted_tap_time_list:
        f.write("{0},".format(each))
    f.write("\n")
    sorted_tap_time_list.reverse()
    f.write("reverse:,")
    for each in sorted_tap_time_list:
        f.write("{0},".format(each))

    f.write("\n")
    print('[End Tapping Device]')

    f.flush()


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
    
    priorities = [5]
    start_thread_number={1: 1, 5: 1, 10: 2}
    max_thread_number={1: 12, 5: 4, 10: 8}
    thread_number_steps={1: 1, 5: 1, 10: 1}
    
    for i in priorities:
        thread_number = start_thread_number[i]
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

def cpu_stress_routine_repeat():

    for i in range(5):
        cpu_stress_routine()
        f.write("\n\n\n")

def memory_stress_routine():

    # HUAWEI 2500
    # LIANXINAG 1500
    MAX_MEMORY = 600 # in MB, change this
    STEPS = 2
    memory_to_occupy = MAX_MEMORY / STEPS

    for i in range(STEPS):
        run_memory_stress(memory_to_occupy)
    
        s = "memory{0},".format(memory_to_occupy)
        f.write(s)
        print(s)

        tap_the_device(record_memory=True)

        clear_stress()
        time.sleep(5)

        memory_to_occupy += MAX_MEMORY / STEPS
    
    f.write("\n")
    
# Disk Write Stress
# file block size is 4 16 64 256 1024 4096 K
# load is from >0 to <=100

def disk_write_stress_routine():

    global stress_processes

    WRITE_FILES = ["W_16B.img", "W_256B.img", "W_1K.img", "W_4K.img", "W_16K.img", "W_64K.img", "W_256K.img"]
        
    for filename in WRITE_FILES:
        load = 100
        process = multiprocessing.Process(target=run_disk_write_stress, args=(filename, load))
        process.start()
        stress_processes.append(process)
        time.sleep(0.1)
        s = "disk_wbs{0} disk_wld{1},".format(filename, load)
        f.write(s)
        print(s)
            
        tap_the_device()

        load += 10

        clear_stress()
        time.sleep(0.1)

    f.write("\n")

# Disk Write Stress
# file block size is 4 16 64 256 1024 4096 K
# load is from >0 to <=100

def disk_read_stress_routine():

    global stress_processes

    READ_FILES = ["R_16B.img", "R_256B.img", "R_1K.img", "R_4K.img", "R_16K.img", "R_64K.img", "R_256K.img"]

    for filename in READ_FILES:
        load = 100
        process = multiprocessing.Process(target=run_disk_read_stress, args=(filename, load))
        process.start()
        stress_processes.append(process)
        time.sleep(0.1)
        s = "disk_rbs{0} disk_rld{1},".format(filename, load)
        f.write(s)
        print(s)

        tap_the_device()

        clear_stress()
        time.sleep(0.1)

    f.write("\n")

def disk_read_stress_routine2():

    BUFFER_SIZES = [16,64,256,1024,4096,16384,65536]

    for buffer_size in BUFFER_SIZES:
        run_disk_read_stress2(buffer_size, 0)
        s = "disk_r2bs{0} disk_r2st{1}".format(buffer_size, 0)
        f.write(s)
        print(s)

        tap_the_device()

        clear_stress()
        time.sleep(1)
    f.write("\n")

def disk_write_stress_routine2():

    BUFFER_SIZES = [16,64,256,1024,4096,16384,65536, 4194304]

    for buffer_size in BUFFER_SIZES:
        run_disk_write_stress2(buffer_size, 0)
        s = "disk_w2bs{0} disk_w2st{1}".format(buffer_size, 0)
        f.write(s)
        print(s)

        tap_the_device()

        clear_stress()
        time.sleep(1)
    f.write("\n")

def disk_read_stress_multithread_routine():

    BUFFER_SIZES = [256,4096,65536,4194304]
    THREAD_NUMBERS = [4, 8, 16]

    for buffer_size in BUFFER_SIZES:
        for thread_number in THREAD_NUMBERS:
            run_disk_read_stress2(buffer_size, 0, thread_number)
            s = "disk_r_multi_bs{0} st{1} tn{2},".format(buffer_size, 0, thread_number)
            f.write(s)
            print(s)

            tap_the_device()

            clear_stress()
            time.sleep(5)
        f.write("\n")
        
def disk_write_stress_multithread_routine():

    BUFFER_SIZES = [256,4096,65536,4194304]
    THREAD_NUMBERS = [4, 8, 16]

    for buffer_size in BUFFER_SIZES:
        for thread_number in THREAD_NUMBERS:
            run_disk_write_stress2(buffer_size, 0, thread_number)
            s = "disk_w_multi_bs{0} st{1} tn{2},".format(buffer_size, 0, thread_number)
            f.write(s)
            print(s)

            tap_the_device()

            clear_stress()
            time.sleep(5)
        f.write("\n")

def disk_jni_read_stress_multithread_routine():

    BUFFER_SIZES = [16, 64, 256, 1024, 4096, 16384, 65536, 4194304]
    THREAD_NUMBERS = [1, 2, 3, 4]

    for buffer_size in BUFFER_SIZES:
        for thread_number in THREAD_NUMBERS:
            run_disk_jni_read_stress(buffer_size, thread_number)
            s = "disk_jni_r_bs{0} disk_jni_r_tn{1},".format(buffer_size, thread_number)
            f.write(s)
            print(s)
            
            tap_the_device()

            clear_stress()
            time.sleep(3)
        f.write("\n")

def disk_jni_write_stress_multithread_routine():
    
    BUFFER_SIZES = [16, 64, 256, 1024, 4096, 16384, 65536, 4194304]
    THREAD_NUMBERS = [1, 2, 3, 4]

    for buffer_size in BUFFER_SIZES:
        for thread_number in THREAD_NUMBERS:
            run_disk_jni_write_stress(buffer_size, thread_number)
            s = "disk_jni_w_bs{0} disk_jni_w_tn{1},".format(buffer_size, thread_number)
            f.write(s)
            print(s)
            
            tap_the_device()

            clear_stress()
            time.sleep(3)
        f.write("\n")

def network_stress_routine():

    MIN_THREAD_NUMBER = 1
    MAX_THREAD_NUMBER = 16
    STEP_LENGTH = 4

    for thread_number in range(MIN_THREAD_NUMBER, MAX_THREAD_NUMBER + 1):
        run_network_stress(thread_number)
        s = "net_tn{0},".format(thread_number)
        f.write(s)
        print(s)

        tap_the_device()

        clear_stress()
        time.sleep(1)
    f.write("\n")

func_dict = {
    'run_stress_test': test_stress,
    'cpu': cpu_stress_routine,
    'cpu_repeat': cpu_stress_routine_repeat,
    'memory': memory_stress_routine,
    'disk_write': disk_write_stress_routine,
    'disk_write2': disk_write_stress_routine2,
    'disk_write_mt': disk_write_stress_multithread_routine,
    'disk_jni_write': disk_jni_write_stress_multithread_routine,
    'disk_read': disk_read_stress_routine,
    'disk_read2': disk_read_stress_routine2,
    'disk_read_mt': disk_read_stress_multithread_routine,
    'disk_jni_read': disk_jni_read_stress_multithread_routine,
    'network': network_stress_routine,
}

def terminate_program(a, b):
    clear_stress()
    exit(0)

if __name__ == "__main__":

    signal.signal(signal.SIGINT, terminate_program)
    signal.signal(signal.SIGTERM, terminate_program)

    test_flag = False

    file_name_prefix = "result_"

    dt = datetime.datetime.now()
    file_name = file_name_prefix + dt.strftime("%Y-%m-%d-%H-%M-%S") + '.csv'
    

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
        clear_stress()
        each()

    f.close()
