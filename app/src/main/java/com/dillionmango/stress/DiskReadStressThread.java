package com.dillionmango.stress;

import android.os.Environment;
import android.os.SystemClock;
import android.util.Log;

import java.io.File;
import java.io.FileInputStream;
import java.io.FileNotFoundException;
import java.io.IOException;
import java.io.InputStream;

/**
 * Created by Dillion on 07/04/2017.
 */
class DiskReadStressThread extends StressThread {

    private static final File fileToRead = new File(Environment.getExternalStorageDirectory(), "com.dillionmango.stress.file_to_read");

    private int bufferSizeInBytes, sleepTimeInMs;

    public DiskReadStressThread(int bufferSizeInBytes, int sleepTimeInMs) {
        super();
        this.bufferSizeInBytes = bufferSizeInBytes;
        this.sleepTimeInMs = sleepTimeInMs;
    }

    private InputStream getRefreshedInputStream() {
        InputStream ret;
        try {
            ret = new FileInputStream(fileToRead);
        } catch (FileNotFoundException e) {
            e.printStackTrace();
            throw new RuntimeException("FileNotFoundException when opening file in " + fileToRead.getAbsolutePath());
        }
        return ret;
    }

    @Override
    public void run() {
        byte[] buffer = new byte[bufferSizeInBytes];

        InputStream inputStream = null;

        while (getShouldRun()) {
            int len;
            inputStream = getRefreshedInputStream();
            try {
                //long currentTimeStamp = System.currentTimeMillis();
                len = inputStream.read(buffer);
                //long readTime =  System.currentTimeMillis() - currentTimeStamp;
                //Log.d("Write time: ", Long.toString(readTime));
            } catch (IOException e) {
                e.printStackTrace();
                throw new RuntimeException("IOException when reading file in " + fileToRead.getAbsolutePath());
            }

            if (len == -1) {
                try {
                    inputStream.close();
                } catch (IOException e) {}
                inputStream = getRefreshedInputStream();
            }

            if (sleepTimeInMs > 0) {
                try {
                    sleep(sleepTimeInMs);
                } catch (InterruptedException e) {
                }
            }
            if (inputStream != null) {
                try {
                    inputStream.close();
                } catch (IOException e) { }
            }
        }
    }
}
