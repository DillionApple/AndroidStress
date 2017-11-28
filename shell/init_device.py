import os

push_files = [
    'R_16B.img',
    'R_256B.img',
    'R_1K.img',
    'R_4K.img',
    'R_16K.img',
    'R_64K.img',
    'R_256K.img',
    'com.dillionmango.stress.file_to_read0',
    'com.dillionmango.stress.file_to_read1',
    'com.dillionmango.stress.file_to_read2',
    'com.dillionmango.stress.file_to_read3',
    'com.dillionmango.stress.file_to_read4',
    'com.dillionmango.stress.file_to_read5',
    'com.dillionmango.stress.file_to_read6',
    'com.dillionmango.stress.file_to_read7',
    'com.dillionmango.stress.file_to_read8',
    'com.dillionmango.stress.file_to_read9',
    'com.dillionmango.stress.file_to_read10',
    'com.dillionmango.stress.file_to_read11',
    'com.dillionmango.stress.file_to_read12',
    'com.dillionmango.stress.file_to_read13',
    'com.dillionmango.stress.file_to_read14',
    'com.dillionmango.stress.file_to_read15',
]

for each in push_files:
    cmd = "adb push {0} /sdcard/".format(each)
    os.system(cmd)
