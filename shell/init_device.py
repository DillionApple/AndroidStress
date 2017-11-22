import os

push_files = [
    'R_16B.img',
    'R_256B.img',
    'R_1K.img',
    'R_4K.img',
    'R_16K.img',
    'R_64K.img',
    'R_256K.img',
    'com.dillionmango.stress.file_to_read'
]

for each in push_files:
    cmd = "adb push {0} /sdcard/".format(each)
    os.system(cmd)