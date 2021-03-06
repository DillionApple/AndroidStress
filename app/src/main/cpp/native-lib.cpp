//
// Created by WangDillion on 14/11/2017.
//

#include <jni.h>
#include <string>
#include <cstdlib>
#include <stdio.h>
#include <sys/types.h>
#include <sys/stat.h>
#include <sys/fcntl.h>
#include <unistd.h>

static pthread_mutex_t mutex;
static char * mem_blocks[128];
static int mem_blocks_count = 0;

static const int MAX_LEN = 4194304;
static char rs[MAX_LEN+1];
static char ws[MAX_LEN+1];
static bool wsInited = false;

extern "C"
JNIEXPORT int JNICALL
Java_com_dillionmango_stress_MainActivity_startMemoryStress(
        JNIEnv *env,
        jobject /* this */, jint memory_stress) {
    // memory_stress is in MB
    int mem_size = 1024 * 1024 * memory_stress;
    char *mem = (char *)std::malloc(mem_size * sizeof(char));
    if (mem == NULL) {
        return -1;
    }
    for (int i = 0; i < mem_size; ++i) {
        mem[i] = 10;
    }
    int x = mem[10] * mem[20];
    pthread_mutex_lock(&mutex);
    mem_blocks[mem_blocks_count++] = mem;
    pthread_mutex_unlock(&mutex);
    return 0;
}

extern "C"
void
Java_com_dillionmango_stress_MainActivity_stopMemoryStress(
        JNIEnv *env,
        jobject  /* this */ ) {
    for (int i = 0; i < mem_blocks_count; ++i) {
        free(mem_blocks[i]);
    }
    pthread_mutex_lock(&mutex);
    mem_blocks_count = 0;
    pthread_mutex_unlock(&mutex);
}

extern "C"
void
Java_com_dillionmango_stress_DiskJNIReadStressThread_readFromDisk(
        JNIEnv *env,
        jobject /* this */,
        jint file_number,
        jint buffer_size) {
    static int files[] = {-1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1}; // 32
    if (files[file_number] == -1) {
        char filename[256];
        memset(filename, 0, sizeof(filename));
        sprintf(filename, "%s%d", "/sdcard/com.dillionmango.stress.file_to_read", file_number);
        files[file_number] = open(filename, O_RDONLY);
    }
    int fd = files[file_number];
    int cnt = read(fd, rs, buffer_size);
    lseek(fd, 0, SEEK_SET);
}

extern "C"
void
Java_com_dillionmango_stress_DiskJNIWriteStressThread_writeToDisk(
        JNIEnv *env,
        jobject /* this */,
        jint file_number,
        jint buffer_size) {
    static int files[] = {-1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1}; // 32
    if (files[file_number] == -1) {
        char filename[256];
        memset(filename, 0, sizeof(filename));
        sprintf(filename, "%s%d", "/sdcard/com.dillionmango.stress.file_to_write", file_number);
        files[file_number] = open(filename, O_RDWR | O_CREAT, 00777);
    }
    int fd = files[file_number];
    int cnt = write(fd, ws, buffer_size);
    lseek(fd, 0, SEEK_SET);
}