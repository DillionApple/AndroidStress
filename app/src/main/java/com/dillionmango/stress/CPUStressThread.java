package com.dillionmango.stress;

import android.os.SystemClock;

import java.util.Random;

/**
 * Created by Dillion on 07/04/2017.
 */
public class CPUStressThread extends StressThread {

    private int threadPriority;

    public CPUStressThread(int prioriry) {
        /**
         * CPU load is the number of threads will run to generate cpu stress
         * priority must be MIN_PRIORITY(1), DEFAULT_PRIORITY(5) or MAX_PRIORITY(10)
         */
        super();
        this.threadPriority = prioriry;
    }

    @Override
    public void run() {
        long currentTimeStamp = SystemClock.currentThreadTimeMillis();
        Random random = new Random();
        random.setSeed(currentTimeStamp);
        setPriority(threadPriority);
        while(getShouldRun()) {
            double x = random.nextDouble();
            double y;
            y = x * x;
            y = y / x;
        }
    }
}
