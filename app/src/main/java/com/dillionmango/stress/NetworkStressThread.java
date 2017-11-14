package com.dillionmango.stress;

import android.os.SystemClock;

import java.io.IOException;
import java.io.InputStream;
import java.net.HttpURLConnection;
import java.net.MalformedURLException;
import java.net.URL;

/**
 * Created by Dillion on 07/04/2017.
 */
class NetworkStressThread extends StressThread {

    public NetworkStressThread(int load) {
        super();
    }

    @Override
    public void run() {
        int runTime = 500 * 10 / 100;

        String downloadURLString = "http://weixin.qq.com/cgi-bin/download302?check=false&uin=&stype=&promote=&fr=&lang=zh_CN&ADTAG=&url=android16";
        URL downloadURL;
        try {
            downloadURL = new URL(downloadURLString);
        } catch (MalformedURLException e) {
            e.printStackTrace();
            throw new RuntimeException("MalformedURLException when create URL object of " + downloadURLString);
        }

        InputStream inputStream = null;
        byte[] buffer = new byte[100 * 1024];

        while (getShouldRun()) {

            long startTimeStamp = SystemClock.currentThreadTimeMillis();
            long currentTimeStamp = SystemClock.currentThreadTimeMillis();
            HttpURLConnection connection;

            try {
                connection = (HttpURLConnection) downloadURL.openConnection();
                connection.setConnectTimeout(10 * 1000);
                connection.connect();
                if (connection.getResponseCode() == 200) {
                    inputStream = connection.getInputStream();

                    while (currentTimeStamp - startTimeStamp < runTime) {
                        int len = inputStream.read(buffer);
                        if (len == -1) {
                            break;
                        }
                        currentTimeStamp = SystemClock.currentThreadTimeMillis();
                    }
                }
            } catch (IOException e) {
                e.printStackTrace();
                throw new RuntimeException("IOException when reading data from url " + downloadURLString);
            }

            try {
                sleep(500 - runTime);
            } catch (InterruptedException e) {}

            if (inputStream!= null) {
                try {
                    inputStream.close();
                } catch (IOException e) {}
            }

        }
    }

}
