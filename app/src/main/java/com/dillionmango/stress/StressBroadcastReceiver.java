package com.dillionmango.stress;

import android.content.BroadcastReceiver;
import android.content.Context;
import android.content.Intent;
import android.os.Bundle;

/**
 * Created by Dillion on 04/04/2017.
 */

public class StressBroadcastReceiver extends BroadcastReceiver {

    static MainActivity mainActivity;

    @Override
    public void onReceive(Context context, Intent intent) {

        String action = intent.getAction();
        if (action.equals("com.dillionmango.stress.set_stress")) {

            if (mainActivity != null) {
                mainActivity.finish();
                mainActivity = null;
            }

            Intent startMainActivityIntent = new Intent();
            startMainActivityIntent.setFlags(Intent.FLAG_ACTIVITY_NEW_TASK);
            startMainActivityIntent.setClass(context, MainActivity.class);
            Bundle extras = intent.getExtras();
            if (extras != null) {
                startMainActivityIntent.putExtras(extras);
            }

            context.startActivity(startMainActivityIntent);
        }

    }

}
