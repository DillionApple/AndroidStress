import sys,os

command = "adb shell am broadcast -a com.dillionmango.stress.set_stress"

CPU_STRESS_THREAD_NUMBER = 'cpu_stress_thread_number'
CPU_STRESS_THREAD_PRIORITY = 'cpu_stress_thread_priority'

MEMORY_STRESS = 'memory_stress'

DISK_READ_STRESS_THREAD_NUMBER = 'disk_read_stress_thread_number'
DISK_READ_STRESS_BUFFER_SIZE = 'disk_read_stress_buffer_size'
DISK_READ_STRESS_SLEEP_TIME = 'disk_read_stress_sleep_time'

DISK_JNI_READ_STRESS_THREAD_NUMBER = 'disk_jni_read_stress_thread_number'
DISK_JNI_READ_STRESS_BUFFER_SIZE = 'disk_jni_read_stress_buffer_size'

DISK_WRITE_STRESS_THREAD_NUMBER = 'disk_write_stress_thread_number'
DISK_WRITE_STRESS_BUFFER_SIZE = 'disk_write_stress_buffer_size'
DISK_WRITE_STRESS_SLEEP_TIME = 'disk_write_stress_sleep_time'

DISK_WRITE_STRESS_WITH_LOAD_LOAD = 'disk_write_stress_with_load_load'

DISK_JNI_WRITE_STRESS_THREAD_NUMBER = 'disk_jni_write_stress_thread_number'
DISK_JNI_WRITE_STRESS_BUFFER_SIZE = 'disk_jni_write_stress_buffer_size'

NETWORK_STRESS_THREAD_NUMBER = 'network_stress_thread_number'


full_key_map = {
    'cpu_tn': CPU_STRESS_THREAD_NUMBER,
    'cpu_tp': CPU_STRESS_THREAD_PRIORITY,
    'mem': MEMORY_STRESS,
    'disk_rtn': DISK_READ_STRESS_THREAD_NUMBER,
    'disk_rbs': DISK_READ_STRESS_BUFFER_SIZE,
    'disk_rst': DISK_READ_STRESS_SLEEP_TIME,
    'disk_jni_rtn': DISK_JNI_READ_STRESS_THREAD_NUMBER,
    'disk_jni_rbs': DISK_JNI_READ_STRESS_BUFFER_SIZE,
    'disk_wtn': DISK_WRITE_STRESS_THREAD_NUMBER,
    'disk_wbs': DISK_WRITE_STRESS_BUFFER_SIZE,
    'disk_wst': DISK_WRITE_STRESS_SLEEP_TIME,
    'disk_wwll': DISK_WRITE_STRESS_WITH_LOAD_LOAD,
    'disk_jni_wtn': DISK_JNI_WRITE_STRESS_THREAD_NUMBER,
    'disk_jni_wbs': DISK_JNI_WRITE_STRESS_BUFFER_SIZE,
    'net_tn': NETWORK_STRESS_THREAD_NUMBER,
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
