import os
import subprocess
import datetime
from time import sleep

def run_cmd(cmd):
    print(cmd)
    proc = subprocess.Popen([cmd], stdout=subprocess.PIPE, shell=True)
    (out, err) = proc.communicate()
    return out

def get_pids(package_name):
    ret = []
    draft_string = run_cmd("adb shell ps")
    l = draft_string.split("\r\n")
    for each in l:
        if each.find(package_name) != -1:
            pid = each.split()[1]
            ret.append(pid)
    return ret

def record_threads(package_name):

    global pr_f

    tree = get_pids(package_name)

    draft_string = run_cmd("adb shell ps -t -p")
    l = draft_string.split("\r\n")[1:-1]
    
    i = 0
    while (i < len(tree)):
        pid = tree[i]
        for each in l:
            ppid = each.split()[2]
            if ppid == pid:
                tree.append(each.split()[1])
        i += 1

    priority_count_dict = {}
    threads_set = set(tree)
    for each in l:
        pid = each.split()[1]
        if pid in threads_set:
            priority = each.split()[5]
            if priority in priority_count_dict:
                priority_count_dict[priority] += 1
            else:
                priority_count_dict[priority] = 1

    for index in sorted(priority_count_dict):
        pr_f.write("{0},{1}\n".format(index, priority_count_dict[index]))
    pr_f.write("---,---\n")
    

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

def record_disk_io(package_name):

    global other_f

    run_cmd("adb root")
    pids = get_pids(package_name)
    total_rchar = 0
    total_wchar = 0
    total_read_bytes = 0
    total_write_bytes = 0
    for pid in pids:        
        draft_string = run_cmd("adb shell cat /proc/{0}/io".format(pid))
        l = draft_string.split()
        rchar = int(l[l.index("rchar:") + 1])
        wchar = int(l[l.index("wchar:") + 1])
        read_bytes = int(l[l.index("read_bytes:") + 1])
        write_bytes = int(l[l.index("write_bytes:") + 1])
        total_rchar += rchar
        total_wchar += wchar
        total_read_bytes += read_bytes
        total_write_bytes += write_bytes

    print(total_rchar, total_wchar, total_read_bytes, total_write_bytes)

    other_f.write("{0},{1},".format(total_rchar, total_read_bytes))
    other_f.write("{0},{1}\n".format(total_wchar, total_write_bytes))

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


if __name__ == '__main__':

    global pr_f
    global other_f

    dt = datetime.datetime.now()

    for each in os.listdir("."):
        if each[-4:] == ".apk":
            try:
                os.system("mkdir -p {0}".format(each[:-4]))
                file_name_prefix = "{0}/record_".format(each[:-4])

                file_name_prefix = file_name_prefix + dt.strftime("%Y-%m-%d-%H-%M-%S")

                pr_file_name = file_name_prefix + ".pr.csv"
                other_file_name = file_name_prefix + ".other.csv"

                pr_f = open(pr_file_name, "w")
                other_f = open(other_file_name, "w")

                pr_f.write("priority,count\n")
                other_f.write("time,occupied_memory,occupied_percentage,rchar,rbytes,wchar,wbytes\n")

                origin_packages_set = get_packages_set()
                install_app(each)
                new_packages_set = get_packages_set()
                new_package = list(new_packages_set - origin_packages_set)[0]
                print(new_package)
                open_app(new_package)
                sleep(20)
                press_home_button()
                for i in range(600):
                    pr_f.write("{0},".format(datetime.datetime.now().strftime("%Y-%m-%d-%H-%M-%S")))
                    other_f.write("{0},".format(datetime.datetime.now().strftime("%Y-%m-%d-%H-%M-%S")))
                    record_threads(new_package)
                    record_memory()
                    record_disk_io(new_package)
                    
                pr_f.close()
                other_f.close()
                uninstall_app(new_package)

            except Exception as e:
                print(e)
                pr_f.close()
                other_f.close()
                uninstall_app(new_package)


# install app
# open app
# wait for use's response
# start the recorder app
# loop to fetch thread infos
# copy the diskio info back to computer
# end the app
# uninstall the app
