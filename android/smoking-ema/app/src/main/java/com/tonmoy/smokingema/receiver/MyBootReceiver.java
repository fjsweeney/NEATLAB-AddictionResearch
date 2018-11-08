package com.tonmoy.smokingema.receiver;

import android.content.BroadcastReceiver;
import android.content.Context;
import android.content.Intent;

import com.tonmoy.smokingema.BootStartActivity;
import com.tonmoy.smokingema.model.SettingsModel;

/**
 * Created by hossaim3 on 1/30/2018.
 */

public class MyBootReceiver extends BroadcastReceiver {
    SettingsModel settings;
    private static final int REQUEST_RECORD_AUDIO_PERMISSION = 200;
    private String[] permissions = {android.Manifest.permission.RECORD_AUDIO};
    @Override
    public void onReceive(Context context, Intent intent) {
        if (intent.getAction().equals("android.intent.action.BOOT_COMPLETED")) {
            // TODO Set the alarm here.
            Intent i= new Intent(context, BootStartActivity.class);
            context.startActivity(i);
        }
    }

}