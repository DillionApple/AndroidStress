import os
import time


while True:
    startTime = time.time()
    os.system("adb shell input tap 10 100")
    endTime = time.time()
    print(endTime - startTime)
    time.sleep(1);