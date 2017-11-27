package com.dillionmango.stress;

import android.os.Environment;
import android.os.SystemClock;

import java.io.File;
import java.io.FileNotFoundException;
import java.io.FileOutputStream;
import java.io.IOException;

/**
 * Created by Dillion on 07/04/2017.
 */
class DiskWriteStressWithLoadThread extends StressThread {

    private static int PERIOD = 500; // 500ms

    private static final File fileToWrite = new File(Environment.getExternalStorageDirectory(), "com.example.dillion.file_to_write");

    private int load;

    public DiskWriteStressWithLoadThread(int load) {
        this.load = load;
    }

    @Override
    public void run() {
        int runTime = PERIOD * load / 100 * 10;
        int bufferSize = 1024 * 1024;
        byte[] buffer = new byte[bufferSize];
        FileOutputStream outputStream = null;



        for (int i = 0; i < bufferSize; ++i) {
            buffer[i] = (byte) i;
        }

        while (getShouldRun()) {

            if (!fileToWrite.exists()) {
                try {
                    fileToWrite.createNewFile();
                } catch (IOException e) {
                    e.printStackTrace();
                    throw new RuntimeException("IOException when create file in " + fileToWrite.getAbsolutePath());
                }
            }

            long startTimeStamp = System.currentTimeMillis();
            long currentTimeStamp = System.currentTimeMillis();

            try {
                outputStream = new FileOutputStream(fileToWrite);
            } catch (FileNotFoundException e) {
                e.printStackTrace();
                throw new RuntimeException("FileNotFoundException when open file in " + fileToWrite.getAbsolutePath());
            }

            while (currentTimeStamp - startTimeStamp < runTime) {
                try {
                    outputStream.write(buffer);
                } catch (IOException e) {
                    e.printStackTrace();
                    throw new RuntimeException("IOException when write to file " + fileToWrite.getAbsolutePath());
                }
                currentTimeStamp = System.currentTimeMillis();
            }
            try {
                sleep(PERIOD - runTime);
            } catch (InterruptedException e) {}

            if (outputStream != null) {
                try {
                    outputStream.close();
                } catch (IOException e) { }
            }


            fileToWrite.delete();

        }


    }

}
