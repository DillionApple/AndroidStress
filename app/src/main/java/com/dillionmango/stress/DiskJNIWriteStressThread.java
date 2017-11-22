package com.dillionmango.stress;

/**
 * Created by Dillion on 22/11/2017.
 */

public class DiskJNIWriteStressThread extends StressThread {

    private int fileNumber, bufferSize;

    public native void writeToDisk(int file_number, int buffer_size);

    public DiskJNIWriteStressThread(int fileNumber, int bufferSize) {
        this.fileNumber = fileNumber;
        this.bufferSize = bufferSize;
    }

    @Override
    public void run() {
        super.run();
        while (getShouldRun()) {
            writeToDisk(fileNumber, bufferSize);
        }
    }
}
