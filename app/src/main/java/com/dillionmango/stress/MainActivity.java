package com.dillionmango.stress;

import android.Manifest;
import android.content.Intent;
import android.content.pm.PackageManager;
import android.os.Bundle;
import android.support.v4.app.ActivityCompat;
import android.support.v7.app.AppCompatActivity;
import android.util.Log;

import java.util.ArrayList;


public class MainActivity extends AppCompatActivity {

    static {
        System.loadLibrary("native-lib");
    }

    public native void startMemoryStress(int memory_stress);
    public native void stopMemoryStress();


    ArrayList<StressThread> stressThreads = null;
    ArrayList<String> stressTypes = null;

    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        setContentView(R.layout.activity_main);

        StressBroadcastReceiver.mainActivity = this;

        stressThreads = new ArrayList<StressThread>();

        Intent intent = getIntent();

        int cpuStressThreadNumber = intent.getIntExtra("cpu_stress_thread_number", 0);
        int cpuStressThreadPrioriry = intent.getIntExtra("cpu_stress_thread_priority", 5);  /* 5 is DEFAULT_PRIORIRY, 1 is the lowest, 10 is the highest(foreground thread) */

        int memoryStress = intent.getIntExtra("memory_stress", 0);

        int diskReadStressThreadNumber = intent.getIntExtra("disk_read_stress_thread_number", 0);
        int diskReadStressBufferSize = intent.getIntExtra("disk_read_stress_buffer_size", 0);   /* is by bytes */
        int diskReadStressSleepTime = intent.getIntExtra("disk_read_stress_sleep_time", 0);    /* is by ms */

        int diskJNIReadStressThreadNumber = intent.getIntExtra("disk_jni_read_stress_thread_number", 0);
        int diskJNIReadStressBufferSize = intent.getIntExtra("disk_jni_read_stress_buffer_size", 0);

        int diskWriteStressThreadNumber = intent.getIntExtra("disk_write_stress_thread_number", 0);
        int diskWriteStressBufferSize = intent.getIntExtra("disk_write_stress_buffer_size", 0); /* is by bytes */
        int diskWriteStressSleepTime = intent.getIntExtra("disk_write_stress_sleep_time", 0);   /* is by ms */

        int diskJNIWriteStressThreadNumber = intent.getIntExtra("disk_jni_write_stress_thread_number", 0);
        int diskJNIWRiteStressBufferSize = intent.getIntExtra("disk_jni_write_stress_buffer_size", 0);

        int networkStress = intent.getIntExtra("network_stress", 0);
        int fileOperationStressFlag = intent.getIntExtra("file_operation_stress", 0);

        if (ActivityCompat.checkSelfPermission(this, Manifest.permission.WRITE_EXTERNAL_STORAGE) == PackageManager.PERMISSION_GRANTED) {
            Log.d("Write To SD Card","Permission is granted");
        } else {
            ActivityCompat.requestPermissions(this, new String[]{Manifest.permission.WRITE_EXTERNAL_STORAGE}, 1);
        }

        if (cpuStressThreadNumber > 0) {
            Log.d(
                    this.getClass().getSimpleName(),
                    String.format("Set cpu stress thread number: %d, prioriry: %d", cpuStressThreadNumber, cpuStressThreadPrioriry)
            );
            for (int i = 0; i < cpuStressThreadNumber; ++i) {
                StressThread thread = new CPUStressThread(cpuStressThreadPrioriry);
                thread.start();
                stressThreads.add(thread);
            }
        }

        if (memoryStress > 0) {
            int unit = 100; // 100M every time
            int numbers = memoryStress / unit;
            for (int i = 0; i < numbers; ++i) {
                startMemoryStress(unit);
            }
            if (memoryStress % unit != 0) {
                startMemoryStress(memoryStress % unit);
            }
        }

        if (diskReadStressThreadNumber > 0 && diskReadStressBufferSize > 0 && diskReadStressSleepTime >= 0) {
            for (int i = 0; i < diskReadStressThreadNumber; i++) {
                StressThread thread = new DiskReadStressThread(diskReadStressBufferSize, diskReadStressSleepTime);
                thread.start();
                stressThreads.add(thread);
            }
        }
        if (diskWriteStressBufferSize > 0 && diskWriteStressSleepTime >= 0) {
            for (int i = 0; i < diskWriteStressThreadNumber; i++) {
                StressThread thread = new DiskWriteStressThread(diskWriteStressBufferSize, diskWriteStressSleepTime, i);
                thread.start();
                stressThreads.add(thread);
            }
        }
        if (networkStress > 0) {
            StressThread thread = new NetworkStressThread(networkStress);
            thread.start();
            stressThreads.add(thread);
        }
        if (diskJNIReadStressThreadNumber > 0 && diskJNIReadStressBufferSize > 0) {
            for (int i = 0; i < diskJNIReadStressThreadNumber; i++) {
                StressThread thread = new DiskJNIReadStressThread(diskJNIReadStressBufferSize);
                thread.start();
                stressThreads.add(thread);
            }
        }
        if (diskJNIWriteStressThreadNumber > 0 && diskJNIWRiteStressBufferSize > 0) {
            for (int i = 0; i < diskJNIWriteStressThreadNumber; i++) {
                StressThread thread = new DiskJNIWriteStressThread(i, diskJNIWRiteStressBufferSize);
                thread.start();
                stressThreads.add(thread);
            }
        }

    }

    @Override
    public  void finish() {
        super.finish();

        if (stressThreads != null) {
            for (Thread thread: stressThreads) {
                thread.interrupt();
            }
        }
        stressThreads = null;

        stopMemoryStress();

        // stop memory stress
        Intent intent = new Intent("com.dillionmango.stress.stop_memory_stress");
        sendBroadcast(intent);
    }


}
