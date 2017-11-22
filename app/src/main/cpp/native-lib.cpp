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
JNIEXPORT void JNICALL
Java_com_dillionmango_stress_MainActivity_startMemoryStress(
        JNIEnv *env,
        jobject /* this */, jint memory_stress) {
    // memory_stress is in MB
    int mem_size = 1024 * 1024 * memory_stress;
    char *mem = (char *)std::malloc(mem_size * sizeof(char));
    if (mem == NULL) {
        return;
    }
    for (int i = 0; i < mem_size; ++i) {
        mem[i] = 10;
    }
    int x = mem[10] * mem[20];
    pthread_mutex_lock(&mutex);
    mem_blocks[mem_blocks_count++] = mem;
    pthread_mutex_unlock(&mutex);
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
        jint buffer_size) {

    int fd = open("/sdcard/R_4096K.img", O_RDONLY);
    int cnt = read(fd, rs, buffer_size);
    close(fd);
}

extern "C"
void
Java_com_dillionmango_stress_DiskJNIWriteStressThread_writeToDisk(
        JNIEnv *env,
        jobject /* this */,
        jint file_number,
        jint buffer_size) {
    char filename[256];
    memset(filename, 0, sizeof(filename));
    sprintf(filename, "%s%d", "/sdcard/com.dillionmango.stress.file_to_write", file_number);

    int fd = open(filename, O_RDWR | O_CREAT, 00777);
    int cnt = write(fd, ws, buffer_size);
    close(fd);
}