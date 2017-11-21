package com.dillionmango.stress;

import android.os.Environment;
import android.util.Log;

import java.io.BufferedOutputStream;
import java.io.File;
import java.io.FileDescriptor;
import java.io.FileNotFoundException;
import java.io.FileOutputStream;
import java.io.IOException;

/**
 * Created by Dillion on 06/11/2017.
 */

/* This thread is different from DiskWriteStressThread.
    You can specify write buffer size and sleep time for the thread,
    Then with every buffer written to the disk, the thread will sleep some time.
 */
public class DiskWriteStressThread extends StressThread {

    private static final File fileToWrite = new File(Environment.getExternalStorageDirectory(), "com.dillionmango.stress.file_to_write");

    private int bufferSizeInBytes, sleepTimeInMs;

    public DiskWriteStressThread(int bufferSizeInBytes, int sleepTimeInMs) {
        super();
        this.bufferSizeInBytes = bufferSizeInBytes;
        this.sleepTimeInMs = sleepTimeInMs;
    }

    @Override
    public void run() {

        byte[] buffer = new byte[bufferSizeInBytes];
        FileOutputStream outputStream = null;
        FileDescriptor fd = null;


        for (int i = 0; i < bufferSizeInBytes; ++i) {
            buffer[i] = (byte) i;
        }

        if (!fileToWrite.exists()) {
            try {
                fileToWrite.createNewFile();
            } catch (IOException e) {
                e.printStackTrace();
                throw new RuntimeException("IOException when create file in " + fileToWrite.getAbsolutePath());
            }
        }

        try {
            outputStream = new FileOutputStream(fileToWrite);
            fd = outputStream.getFD();
        } catch (IOException e) {
            e.printStackTrace();
            throw new RuntimeException("IOException when create outputStream");
        }



        while (getShouldRun()) {
            try {
                long currentTimeStamp = System.currentTimeMillis();
                outputStream.write(buffer);
                fd.sync();
                long writeTime = System.currentTimeMillis() - currentTimeStamp;
                Log.d("Write time: ", Long.toString(writeTime));
            } catch (IOException e) {
                e.printStackTrace();
                throw new RuntimeException("IOException when write to file " + fileToWrite.getAbsolutePath());
            }
            if (sleepTimeInMs > 0) {
                try {
                    sleep(sleepTimeInMs);
                } catch (InterruptedException e) {}
            }
        }
        try {
            outputStream.close();
        } catch (IOException e) {}
    }


}