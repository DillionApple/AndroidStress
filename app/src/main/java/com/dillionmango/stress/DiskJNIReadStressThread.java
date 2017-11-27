package com.dillionmango.stress;

/**
 * Created by Dillion on 22/11/2017.
 */

public class DiskJNIReadStressThread extends StressThread {

    private int bufferSize, fileNumber;

    public native void readFromDisk(int file_number, int buffer_size);

    public DiskJNIReadStressThread(int fileNumber, int bufferSize) {
        super();
        this.fileNumber = fileNumber;
        this.bufferSize = bufferSize;
    }

    @Override
    public void run() {
        super.run();
        while (getShouldRun()) {
            readFromDisk(fileNumber, bufferSize);
        }
    }
}
