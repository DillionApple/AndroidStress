package com.dillionmango.stress;

/**
 * Created by Dillion on 22/11/2017.
 */

public class DiskJNIReadStressThread extends StressThread {

    private int bufferSize;

    public native void readFromDisk(int buffer_size);

    public DiskJNIReadStressThread(int bufferSize) {
        super();
        this.bufferSize = bufferSize;
    }

    @Override
    public void run() {
        super.run();
        while (getShouldRun()) {
            readFromDisk(bufferSize);
        }
    }
}
