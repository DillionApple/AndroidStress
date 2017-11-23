import os, sys
import datetime
import time
import signal

def tap_the_device():

    file_name_prefix = "result_"

    file_name = file_name_prefix + str(datetime.datetime.today()) + '.csv'

    f = open(file_name, "w")

    f.write("result:,")
    
    print("[Start Tapping Device]")
    tap_time_list = []
    for i in range(200):
        startTime = time.time()
        os.system("adb shell input tap 10 100")
        endTime = time.time()

        s = "{0},".format(endTime - startTime)
        f.write(s)
        print("[{0}/{1} Tap time: {2}]".format(i, 200, endTime - startTime))
        tap_time_list.append(endTime - startTime)

    f.write("\n")

    sorted_tap_time_list = sorted(tap_time_list)
    sorted_tap_time_list.reverse()
    f.write("sorted:,")
    for each in sorted_tap_time_list:
        f.write("{0},".format(each))

    f.write("\n")

    s = "max {0},".format(max(tap_time_list))
    f.write(s)

    s = "avg {0},".format(sum(tap_time_list)/len(tap_time_list))
    f.write(s)
    
    f.write("\n")
    f.close()
    print('[End Tapping Device]')

def handler(signum, frame):
    print("Ctrl-c")
    exit(0)

if __name__ == "__main__":
    signal.signal(signal.SIGINT, handler)
    signal.signal(signal.SIGTERM, handler)
    signal.signal(signal.SIGHUP, handler)
    tap_the_device()
