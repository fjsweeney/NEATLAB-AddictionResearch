package com.tonmoy.smokingema;

import android.content.Context;
import android.content.Intent;
import android.content.SharedPreferences;
import android.content.pm.PackageManager;
import android.support.v4.app.ActivityCompat;
import android.support.v7.app.AppCompatActivity;
import android.os.Bundle;

import com.google.gson.Gson;
import com.google.gson.GsonBuilder;
import com.tonmoy.smokingema.model.SettingsModel;

public class BootStartActivity extends AppCompatActivity {
    SettingsModel settings;
    private static final int REQUEST_RECORD_AUDIO_PERMISSION = 200;
    private String[] permissions = {android.Manifest.permission.RECORD_AUDIO};
    private boolean permissionToRecordAccepted = false;

    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        setContentView(R.layout.activity_boot_start);
        startServices();
    }

    @Override
    public void onRequestPermissionsResult(int requestCode, String[] permissions, int[] grantResults) {
        super.onRequestPermissionsResult(requestCode, permissions, grantResults);
        switch (requestCode) {
            case REQUEST_RECORD_AUDIO_PERMISSION:
                permissionToRecordAccepted = grantResults[0] == PackageManager.PERMISSION_GRANTED;
                startService(new Intent(BootStartActivity.this, NoiseInformationService.class));
                BootStartActivity.this.finish();
                break;
        }

    }

    private void startServices() {
        SharedPreferences prefs = getSharedPreferences(
                "com.tonmoy.autismema.settings", Context.MODE_PRIVATE);
        String data = prefs.getString("settings", "");
        if (!data.isEmpty()) {
            GsonBuilder builder = new GsonBuilder();
            Gson gson = builder.create();
            settings = gson.fromJson(data, SettingsModel.class);
        }
        if (settings.collectNoise) {
            ActivityCompat.requestPermissions(this, permissions, REQUEST_RECORD_AUDIO_PERMISSION);
        }
        if (settings.collectSensors) {
            startService(new Intent(BootStartActivity.this, SensorInformationService.class));

        }
    }
}
