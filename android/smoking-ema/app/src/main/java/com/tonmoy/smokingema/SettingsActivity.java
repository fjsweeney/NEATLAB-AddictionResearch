package com.tonmoy.smokingema;

import android.app.AlarmManager;
import android.app.PendingIntent;
import android.content.Context;
import android.content.Intent;
import android.content.SharedPreferences;
import android.content.pm.PackageManager;
import android.support.v4.app.ActivityCompat;
import android.support.v7.app.AppCompatActivity;
import android.os.Bundle;
import android.view.View;
import android.widget.Button;

import com.google.gson.Gson;
import com.google.gson.GsonBuilder;
import com.tonmoy.smokingema.location.LocationActivity;
import com.tonmoy.smokingema.model.SettingsModel;

public class SettingsActivity extends AppCompatActivity implements View.OnClickListener {
    Button buttonLocation, buttonStartSensorInfo, buttonStopSensorInfo, buttonStartNoiseInfo, buttonStopNoiseInfo, buttonRestart;
    private static final int REQUEST_RECORD_AUDIO_PERMISSION = 200;
    private boolean permissionToRecordAccepted = false;
    private String[] permissions = {android.Manifest.permission.RECORD_AUDIO};
    SettingsModel settings;
    private AlarmManager alarmMgr;
    private PendingIntent alarmIntent;
    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        setContentView(R.layout.activity_settings);


        buttonLocation = (Button) findViewById(R.id.buttonUsersLocation);
        buttonStartSensorInfo = (Button) findViewById(R.id.buttonStartLightCollection);
        buttonStopSensorInfo = (Button) findViewById(R.id.buttonStopLightCollection);
        buttonStartNoiseInfo = (Button) findViewById(R.id.buttonStartNoiseCollection);
        buttonStopNoiseInfo = (Button) findViewById(R.id.buttonStopNoiseCollection);
        buttonRestart = (Button) findViewById(R.id.buttonRestart);

        buttonLocation.setOnClickListener(this);
        buttonStartSensorInfo.setOnClickListener(this);
        buttonStopSensorInfo.setOnClickListener(this);
        buttonStartNoiseInfo.setOnClickListener(this);
        buttonStopNoiseInfo.setOnClickListener(this);
        buttonRestart.setOnClickListener(this);

        buttonStopSensorInfo.setEnabled(false);
        buttonStopNoiseInfo.setEnabled(false);
        settings = new SettingsModel();
        loadSettingsValues();
    }

    @Override
    public void onRequestPermissionsResult(int requestCode, String[] permissions, int[] grantResults) {
        super.onRequestPermissionsResult(requestCode, permissions, grantResults);
        switch (requestCode) {
            case REQUEST_RECORD_AUDIO_PERMISSION:
                permissionToRecordAccepted = grantResults[0] == PackageManager.PERMISSION_GRANTED;
                startService(new Intent(SettingsActivity.this, NoiseInformationService.class));
                break;
        }

    }

    @Override
    public void onClick(View view) {

        if (view == buttonLocation) {
            startActivity(new Intent(SettingsActivity.this, LocationActivity.class));
        }
        if (view == buttonStartSensorInfo) {
            settings.collectSensors = true;
            saveSettings();
            updateButtonsState(buttonStopSensorInfo, buttonStartSensorInfo);
            startService(new Intent(SettingsActivity.this, SensorInformationService.class));

        }
        if (view == buttonStopSensorInfo) {
            settings.collectSensors = false;
            saveSettings();
            updateButtonsState(buttonStartSensorInfo, buttonStopSensorInfo);
            stopService(new Intent(SettingsActivity.this, SensorInformationService.class));
        }
        if (view == buttonStartNoiseInfo) {
            settings.collectNoise = true;
            saveSettings();
            updateButtonsState(buttonStopNoiseInfo, buttonStartNoiseInfo);
            ActivityCompat.requestPermissions(this, permissions, REQUEST_RECORD_AUDIO_PERMISSION);

        }
        if (view == buttonStopNoiseInfo) {
            settings.collectNoise = false;
            saveSettings();
            updateButtonsState(buttonStartNoiseInfo, buttonStopNoiseInfo);
            stopService(new Intent(SettingsActivity.this, NoiseInformationService.class));
        }
        if (view == buttonRestart) {
            startAssistance();
            if (settings.collectNoise) {
                ActivityCompat.requestPermissions(this, permissions, REQUEST_RECORD_AUDIO_PERMISSION);
            }
            if (settings.collectSensors) {
                startService(new Intent(SettingsActivity.this, SensorInformationService.class));
            }

        }
    }

    private void startAssistance() {

//        alarmMgr = (AlarmManager)getSystemService(Context.ALARM_SERVICE);
//        Intent intent = new Intent(this, AlarmReceiver.class);
//        alarmIntent = PendingIntent.getBroadcast(this, 0, intent, 0);
//
//// Set the alarm to start at 8:30 a.m.
//        Calendar calendar = Calendar.getInstance();
//        calendar.setTimeInMillis(System.currentTimeMillis());
//        calendar.set(Calendar.HOUR_OF_DAY, 8);
//        calendar.set(Calendar.MINUTE, 30);
//
//// setRepeating() lets you specify a precise custom interval--in this case,
//// 20 minutes.
//        alarmMgr.setRepeating(AlarmManager.RTC_WAKEUP, calendar.getTimeInMillis(),
//                1000 * 60 * 20, alarmIntent);
    }

    private void updateButtonsState(Button bt1, Button bt2) {
        bt2.setEnabled(false);
        bt1.setEnabled(true);
    }

    private void loadSettingsValues() {
        SharedPreferences prefs = this.getSharedPreferences(
                "com.tonmoy.autismema.settings", Context.MODE_PRIVATE);
        String data = prefs.getString("settings", "");
        if (!data.isEmpty()) {
            GsonBuilder builder = new GsonBuilder();
            Gson gson = builder.create();
            settings = gson.fromJson(data, SettingsModel.class);
        }
        if (settings.collectNoise && NoiseInformationService.isRunning) {
            updateButtonsState(buttonStopNoiseInfo, buttonStartNoiseInfo);
        } else {
            updateButtonsState(buttonStartNoiseInfo, buttonStopNoiseInfo);
        }
        if (settings.collectSensors && SensorInformationService.isRunning) {
            updateButtonsState(buttonStopSensorInfo, buttonStartSensorInfo);
        } else {
            updateButtonsState(buttonStartSensorInfo, buttonStopSensorInfo);
        }
    }

    private void saveSettings() {
        SharedPreferences prefs = this.getSharedPreferences(
                "com.tonmoy.autismema.settings", Context.MODE_PRIVATE);
        GsonBuilder builder = new GsonBuilder();
        Gson gson = builder.create();
        prefs.edit().putString("settings", gson.toJson(settings)).commit();
    }
}
