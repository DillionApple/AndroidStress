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
        int diskReadStressSleepTime = intent.getIntExtra("disk_read_stress_buffer_size", 0);    /* is by ms */

        int diskWriteStressThreadNumber = intent.getIntExtra("disk_write_stress_thread_number", 0);
        int diskWriteStressBufferSize = intent.getIntExtra("disk_write_stress_buffer_size", 0); /* is by bytes */
        int diskWriteStressSleepTime = intent.getIntExtra("disk_write_stress_sleep_time", 0);   /* is by ms */

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
                StressThread thread = new DiskWriteStressThread(diskWriteStressBufferSize, diskWriteStressSleepTime);
                thread.start();
                stressThreads.add(thread);
            }
        }
        if (networkStress > 0) {
            StressThread thread = new NetworkStressThread(networkStress);
            thread.start();
            stressThreads.add(thread);
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

        // stop memory stress
        Intent intent = new Intent("com.dillionmango.stress.stop_memory_stress");
        sendBroadcast(intent);
    }


}
