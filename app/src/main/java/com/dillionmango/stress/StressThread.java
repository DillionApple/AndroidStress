package com.dillionmango.stress;

/**
 * Created by Dillion on 07/04/2017.
 */
abstract class StressThread extends Thread {

    private volatile boolean shouldRun;

    public StressThread() {
        this.shouldRun = true;
    }

    public boolean getShouldRun() {
        return shouldRun;
    }

    @Override
    public void interrupt() {
        super.interrupt();
        this.shouldRun = false;
    }
}
