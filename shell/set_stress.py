import sys,os

command = "adb shell am broadcast -a com.dillionmango.stress.set_stress"

CPU_STRESS_THREAD_NUMBER = 'cpu_stress_thread_number'
CPU_STRESS_THREAD_PRIORITY = 'cpu_stress_thread_priority'

MEMORY_STRESS = 'memory_stress'

DISK_READ_STRESS_THREAD_NUMBER = 'disk_read_stress_thread_number'
DISK_READ_STRESS_BUFFER_SIZE = 'disk_read_stress_buffer_size'
DISK_READ_STRESS_SLEEP_TIME = 'disk_read_stress_sleep_time'

DISK_WRITE_STRESS_THREAD_NUMBER = 'disk_write_stress_thread_number'
DISK_WRITE_STRESS_BUFFER_SIZE = 'disk_write_stress_buffer_size'
DISK_WRITE_STRESS_SLEEP_TIME = 'disk_write_stress_sleep_time'


full_key_map = {
    'cpu_tn': CPU_STRESS_THREAD_NUMBER,
    CPU_STRESS_THREAD_NUMBER: CPU_STRESS_THREAD_NUMBER,
    'cpu_tp': CPU_STRESS_THREAD_PRIORITY,
    CPU_STRESS_THREAD_PRIORITY: CPU_STRESS_THREAD_PRIORITY,
    'mem': MEMORY_STRESS,
    MEMORY_STRESS: MEMORY_STRESS,
    'disk_rtn': DISK_READ_STRESS_THREAD_NUMBER,
    DISK_READ_STRESS_THREAD_NUMBER: DISK_READ_STRESS_THREAD_NUMBER,
    'disk_rbs': DISK_READ_STRESS_BUFFER_SIZE,
    DISK_READ_STRESS_BUFFER_SIZE: DISK_READ_STRESS_BUFFER_SIZE,
    'disk_rst': DISK_READ_STRESS_SLEEP_TIME,
    DISK_READ_STRESS_SLEEP_TIME: DISK_READ_STRESS_SLEEP_TIME,
    'disk_wtn': DISK_WRITE_STRESS_THREAD_NUMBER,
    DISK_WRITE_STRESS_THREAD_NUMBER: DISK_WRITE_STRESS_THREAD_NUMBER,
    'disk_wbs': DISK_WRITE_STRESS_BUFFER_SIZE,
    DISK_WRITE_STRESS_BUFFER_SIZE: DISK_WRITE_STRESS_BUFFER_SIZE,
    'disk_wst': DISK_WRITE_STRESS_SLEEP_TIME,
    DISK_WRITE_STRESS_SLEEP_TIME: DISK_WRITE_STRESS_SLEEP_TIME,
}

for index in range(1, len(sys.argv), 2):
    key = full_key_map.get(sys.argv[index], None)
    if key == None:
        print("Unknown key: {key}".format(key=sys.argv[index]))
        continue
    value = sys.argv[index+1]
    command = "{origin} --ei {key} {value}".format(
        origin=command, key=key, value=value)
    

print(command)
os.system(command)



