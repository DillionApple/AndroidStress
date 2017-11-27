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

* cpu_tn
* cpu_tp

### Memory
    
* mem

### Disk Write
    
* disk_wtn
* disk_wbs
* disk_wst
* disk_w2tn
* disk_w2bs
* disk_w2st
* disk_jni_wtn
* disk_jni_wbs

### Disk Read

* disk_rtn
* disk_rbs
* disk_rst
* disk_r2tn
* disk_r2bs
* disk_r2st
* disk_jni_rtn
* disk_jni_rbs

### Network

* net_tn