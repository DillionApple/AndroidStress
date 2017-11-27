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

    public NetworkStressThread() {
        super();
    }

    public InputStream getRefreshedInputStream(URL downloadURL) {
        HttpURLConnection connection;
        try {
            connection = (HttpURLConnection) downloadURL.openConnection();
            connection.setConnectTimeout(10 * 1000);
            connection.connect();
            if (connection.getResponseCode() != 200) {
                throw new IOException("Connection return code is not 200");
            } else {
                return connection.getInputStream();
            }
        } catch(IOException e) {
            throw new RuntimeException("IOException when connecting to remote server");
        }
    }

    @Override
    public void run() {

        String downloadURLString = "http://weixin.qq.com/cgi-bin/download302?check=false&uin=&stype=&promote=&fr=&lang=zh_CN&ADTAG=&url=android16";
        URL downloadURL;
        try {
            downloadURL = new URL(downloadURLString);
        } catch (MalformedURLException e) {
            e.printStackTrace();
            throw new RuntimeException("MalformedURLException when create URL object of " + downloadURLString);
        }

        InputStream inputStream = getRefreshedInputStream(downloadURL);
        byte[] buffer = new byte[10 * 1024 * 1024];

        while (getShouldRun()) {
            try {
                if (inputStream.read(buffer) == -1) {
                    inputStream.close();
                    inputStream = getRefreshedInputStream(downloadURL);
                }
            } catch (IOException e) {
                e.printStackTrace();
                throw new RuntimeException("IOException when reading data from url " + downloadURLString);
            }
        }

        if (inputStream!= null) {
            try {
                inputStream.close();
            } catch (IOException e) {}
        }


    }

}
