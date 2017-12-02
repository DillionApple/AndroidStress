import os
import subprocess
import multiprocessing
import datetime
import time
import re
import traceback

def run_cmd(cmd):
    print(cmd)
    proc = subprocess.Popen(cmd, stdout=subprocess.PIPE, shell=True)
    (out, err) = proc.communicate()
    return out

def get_procs(package_name):
    # return {pid: proc_name}
    ret = []
    draft_string = run_cmd("adb shell ps")
    procs_list = draft_string.split("\r\n")[:-1]
    procs_dict = {}
    example_pkg_proc_str = ""
    for proc_info_str in procs_list:
        proc_info_list = proc_info_str.split()
        pid = proc_info_list[1]
        proc_name = proc_info_list[-1]
        procs_dict[pid] = proc_name
        if example_pkg_proc_str == "" and proc_name.find(package_name) >= 0:
            example_pkg_proc_str = proc_info_str
            
    # get uid u0_a***
    pattern = re.compile(".*u0_a(\d+).*")
    match = re.match(pattern, example_pkg_proc_str)
    uid = 10000 + int(match.group(1))
    uid_folder = "/acct/uid_{0}/".format(uid)

    draft_string = run_cmd("adb shell ls {0} | grep pid".format(uid_folder))
    pids_list = []
    for pid_string in draft_string.split():
        pid_string.strip()
        if pid_string[0:4] == "pid_":
            pids_list.append(pid_string[4:])
    ret = {}
    for pid in pids_list:
        ret[pid] = procs_dict[pid]
    
    return ret

def record_pkg_threads(procs_dict, pr_f, number_of_times):

    draft_string = run_cmd("adb shell ps -t -p")
    all_threads_list = draft_string.split("\r\n")[:-1]

    pkg_threads_list = procs_dict.keys()
    i = 0
    while (i < len(pkg_threads_list)):
        pid = pkg_threads_list[i]
        for each in all_threads_list:
            ppid = each.split()[2]
            if ppid == pid:
                pkg_threads_list.append(each.split()[1])
        i += 1

    draft_string = run_cmd("adb shell top -t -n 1")
    top_list = draft_string.split("\r\n")[:-1]

    all_threads_dict = {} # pid: [percent, thread_name]

    for each in top_list:
        try:
            each_list = each.split()
            all_threads_dict[each_list[1]] = [int(each_list[3][:-1]), each_list[-2]]
        except:
            print("Pass: {}".format(each))

    pkg_thread_priority_dict = {} # {priority: [count, percentage, nr_threads_using_cpu, ["thread_name percentage",...]]}
    pkg_threads_set = set(pkg_threads_list)
    pkg_threads_using_cpu = [] # threads using cpu "<thread name> <cpu_percentage>"
    
    for each in all_threads_list:
        try:
            pid = each.split()[1] # prevent index out of range exception
        except:
            continue
        if pid in pkg_threads_set:
            cpu_percent = 0
            try:
                cpu_percent = all_threads_dict[pid][0]
            except Exception as e:
                print(e.message)
                cpu_percent = 0
                
            priority = each.split()[5]
            if priority in pkg_thread_priority_dict:
                pkg_thread_priority_dict[priority][0] += 1
                pkg_thread_priority_dict[priority][1] += cpu_percent
            else:
                pkg_thread_priority_dict[priority] = [1, cpu_percent, 0, []]
                
            if cpu_percent > 0:
                pkg_thread_priority_dict[priority][2] += 1
                pkg_thread_priority_dict[priority][3].append("{0} {1}".format(all_threads_dict[pid][1], cpu_percent))
                
    # format is "number,time,priority,count,cpu percentage,count of threads using cpu"
    for priority in sorted(pkg_thread_priority_dict):
        pr_f.write("{number},{time},{priority},{count},{cpu_percent},{nr_threads_using_cpu},".format(
            number = number_of_times,
            time = time.time(),
            priority = priority,
            count = pkg_thread_priority_dict[priority][0],
            cpu_percent = pkg_thread_priority_dict[priority][1],
            nr_threads_using_cpu = pkg_thread_priority_dict[priority][2],
        ))
        for each in pkg_thread_priority_dict[priority][3]:
            pr_f.write("{0},".format(each))
        pr_f.write("\n")

def record_memory():

    global other_f

    draft_string = run_cmd("adb shell cat /proc/meminfo")
    l = draft_string.split()
    total_memory = int(l[l.index("MemTotal:") + 1])
    free_memory = int(l[l.index("MemFree:") + 1])
    occupied_memory = total_memory - free_memory
    occupied_memory_percentage = (1.0 * occupied_memory) / (1.0 * total_memory)
    total_swap = int(l[l.index("SwapTotal:") + 1])
    free_swap = int(l[l.index("SwapFree:") + 1])
    occupied_swap = total_swap - free_swap
    # occupied_swap_percentage = (1.0 * occupied_swap) / (1.0 * total_swap)

    other_f.write("{0},{1},".format(occupied_memory, occupied_memory_percentage))

def record_pkg_diskio(procs_dict, diskio_f):

    run_cmd("adb root")
    total_rchar = 0
    total_wchar = 0
    total_read_bytes = 0
    total_write_bytes = 0
    proc_io_output_list = []
    for pid in procs_dict:
        draft_string = run_cmd("adb shell cat /proc/{0}/io".format(pid))
        l = draft_string.split()
        rchar = int(l[l.index("rchar:") + 1])
        wchar = int(l[l.index("wchar:") + 1])
        read_bytes = int(l[l.index("read_bytes:") + 1])
        write_bytes = int(l[l.index("write_bytes:") + 1])

        proc_io_output_list.append(rchar)
        proc_io_output_list.append(read_bytes)
        proc_io_output_list.append(wchar)
        proc_io_output_list.append(write_bytes)
        
        total_rchar += rchar
        total_wchar += wchar
        total_read_bytes += read_bytes
        total_write_bytes += write_bytes

    #format is "time,total_rchar,total_read_bytes,total_wchar,total_write_bytes,..."
    diskio_f.write("{time},{total_rchar},{total_read_bytes},{total_wchar},{total_write_bytes},".format(
        time=time.time(),
        total_rchar=total_rchar,
        total_read_bytes=total_read_bytes,
        total_wchar=total_wchar,
        total_write_bytes=total_write_bytes,
    ))
    
    for each in proc_io_output_list:
        diskio_f.write("{0},".format(each))
    diskio_f.write("\n")
    

def install_app(app_name):
    run_cmd("adb install {0}".format(app_name))

def uninstall_app(package_name):
    run_cmd("adb uninstall {0}".format(package_name))

def get_packages_set():
    draft_string = run_cmd("adb shell pm list packages")
    l = [x[8:] for x in draft_string.split()]
    return set(l)

def open_app(package_name):
    run_cmd("adb shell monkey -p {0} 1".format(package_name))

def press_home_button():
    run_cmd("adb shell input keyevent 3")
    run_cmd("adb shell input keyevent 3")

def record_threads_process_func(filename, procs_dict):
    # procs_dict {pid: proc_name}

    f = open(filename, "w")

    # format f's header
    f.write("number,time,priority,count,cpu percentage,count of threads using cpu\n")

    N = 3

    for i in range(N):
        record_pkg_threads(procs_dict, f, i)

    f.close()
        

def record_diskio_process_func(filename, procs_dict):
    # procs_dict {pid: proc_name}
    print(procs_dict)

    f = open(filename, "w")

    # format f's header
    f.write("time,total_rchar,total_read_bytes,total_wchar,total_write_bytes,")
    for pid in procs_dict:
        proc_name = procs_dict[pid]
        f.write("{proc_name}_rchar,{proc_name}_read_bytes,{proc_name}_wchar,{proc_name}_write_bytes,".format(proc_name=proc_name))
    f.write("\n")
    while (True):
        record_pkg_diskio(procs_dict, f)
        
    f.close()

if __name__ == '__main__':

    global pr_f
    global io_f

    dt = datetime.datetime.now()

    log_file = open("log", "w")

    for filename in os.listdir("."):
        if filename[-4:] == ".apk":
            try:
                apk_name = filename[:-4]
                # new folder and create file for the app
                os.system("mkdir -p {0}".format(apk_name))
                file_name_prefix = "{0}/record_".format(apk_name)
                file_name_prefix = file_name_prefix + dt.strftime("%Y-%m-%d-%H-%M-%S")

                pr_file_name = file_name_prefix + ".pr.csv"
                io_file_name = file_name_prefix + ".io.csv"
                # get pkg name
                origin_packages_set = get_packages_set()
                install_app(filename)
                new_packages_set = get_packages_set()
                package_name = list(new_packages_set - origin_packages_set)[0]
                print("New package is: {0}".format(package_name))
                
                # open the app
                open_app(package_name)
                raw_input("After you finish opening the app, press ENTER")
                time.sleep(0)
                press_home_button()

                procs_dict = get_procs(package_name)
                
                # run record threads thread
                record_threads_proc = multiprocessing.Process(target=record_threads_process_func, args=(pr_file_name, procs_dict))
                record_diskio_proc = multiprocessing.Process(target=record_diskio_process_func, args=(io_file_name, procs_dict))
                record_threads_proc.start()
                record_diskio_proc.start()
                record_threads_proc.join()
                record_diskio_proc.terminate()
                time.sleep(3)
                
                uninstall_app(package_name)

                log_file.write("Success with app {0}".format(apk_name))

            except Exception as e:
                traceback.print_exc()
                log_file.write("Error when run app {0}: {1}".format(apk_name, e.message))
                          
                try:
                    record_threads_proc.terminate()
                except:
                    pass
                          
                try:
                    record_diskio_proc.terminate()
                except:
                    pass
                
                try:
                    uninstall_app(package_name)
                except:
                    pass

    log_file.close()

# loop through the apps
## install app
## open app
## wait for use's response
## start process1 to record phone's diskio
## start process2 to record app's thread infos
## when process2 ends, terminate process1
## uninstall the app
