# Android Stress App

This is an android app that can generate cpu, memory, disk IO stress

## How to use

1. build and install the app into your phone

2. run `python shell/set_stress.py` with options to set stress

3. everytime you set a new stress, the old stress will be canceled

## Examples

1. run `python shell/set_stress.py cpu_tn 10 cpu_tp 10` to start 10 threads, each has priority 10, the max priority a thread can have

2. run `python shell/set_stress.py disk_rtn 10 disk_rbs 1024 disk_rst 1` to start 10 threads, write to the phone's external storage. Each time the thread runs, it writes 1024 bytes to the disk and then sleeps for 1 ms. Then it runs for another time, and loops forever

## Stress Types

### CPU

* cpu_tn (or cpu_stress_thread_number)
* cpu_tp (or cpu_stress_thread_priority)

### Memory
    
* mem (or memory_stress)

### Disk Write
    
* disk_wtn (or disk_write_stress_thread_number)
* disk_wbs (or disk_write_stress_buffer_size)
* disk_wst (or disk_write_stress_sleep_time)

### Disk Read

* disk_rtn (or disk_read_stress_thread_number)
* disk_rbs (or disk_read_stress_buffer_size)
* disk_rst (or disk_read_stress_sleep_time)

