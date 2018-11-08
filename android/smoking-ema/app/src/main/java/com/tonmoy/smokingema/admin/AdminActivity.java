package com.tonmoy.smokingema.admin;

import android.app.AlarmManager;
import android.app.Notification;
import android.app.PendingIntent;
import android.content.ComponentName;
import android.content.Context;
import android.content.Intent;
import android.content.SharedPreferences;
import android.content.pm.PackageManager;
import android.graphics.drawable.BitmapDrawable;
import android.media.MediaRecorder;
import android.media.RingtoneManager;
import android.support.v4.app.ActivityCompat;
import android.support.v7.app.AppCompatActivity;
import android.os.Bundle;
import android.util.Log;
import android.view.View;
import android.widget.Button;
import android.widget.Toast;

import com.google.gson.Gson;
import com.google.gson.GsonBuilder;
import com.google.gson.reflect.TypeToken;
import com.tonmoy.smokingema.NoiseInformationService;
import com.tonmoy.smokingema.R;
import com.tonmoy.smokingema.SensorInformationService;
import com.tonmoy.smokingema.SetupEMAActivity;
import com.tonmoy.smokingema.model.EMAScheduleModel;
import com.tonmoy.smokingema.model.SettingsModel;
import com.tonmoy.smokingema.questionnaire.QuestionnaireActivity;
import com.tonmoy.smokingema.receiver.NotificationPublisher;
import com.tonmoy.smokingema.receiver.MyBootReceiver;

import java.util.ArrayList;
import java.util.Calendar;
import java.util.Date;

public class AdminActivity extends AppCompatActivity implements View.OnClickListener {

    Button buttonAddQuestion, buttonUsersLocationMap, buttonEMAScheduler, buttonEMAScheduleCancel, buttonSetupEMASchedule, buttonStartSensorInfo, buttonStopSensorInfo, buttonStartNoiseInfo, buttonStopNoiseInfo;
    AlarmManager mAlarmManager;
    SettingsModel settings;

    private static final int REQUEST_RECORD_AUDIO_PERMISSION = 200;
    private static String mFileName = null;
    private boolean permissionToRecordAccepted = false;
    private String[] permissions = {android.Manifest.permission.RECORD_AUDIO};
    private MediaRecorder mRecorder = null;

    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        setContentView(R.layout.activity_admin);

        buttonAddQuestion = (Button) findViewById(R.id.buttonAddQuestion);
        buttonUsersLocationMap = (Button) findViewById(R.id.buttonUsersLocation);
        buttonEMAScheduler = (Button) findViewById(R.id.buttonEMAScheduler);
        buttonEMAScheduleCancel = (Button) findViewById(R.id.buttonEMAScheduleCancel);
        buttonSetupEMASchedule = (Button) findViewById(R.id.buttonSetupEMASchedule);
        buttonStartSensorInfo = (Button) findViewById(R.id.buttonStartLightCollection);
        buttonStopSensorInfo = (Button) findViewById(R.id.buttonStopLightCollection);
        buttonStartNoiseInfo = (Button) findViewById(R.id.buttonStartNoiseCollection);
        buttonStopNoiseInfo = (Button) findViewById(R.id.buttonStopNoiseCollection);

        buttonAddQuestion.setOnClickListener(this);
        buttonUsersLocationMap.setOnClickListener(this);
        buttonEMAScheduler.setOnClickListener(this);
        buttonEMAScheduleCancel.setOnClickListener(this);
        buttonSetupEMASchedule.setOnClickListener(this);
        buttonStartSensorInfo.setOnClickListener(this);
        buttonStopSensorInfo.setOnClickListener(this);
        buttonStartNoiseInfo.setOnClickListener(this);
        buttonStopNoiseInfo.setOnClickListener(this);

        settings = new SettingsModel();
        loadSettingsValues();
    }

    @Override
    public void onRequestPermissionsResult(int requestCode, String[] permissions, int[] grantResults) {
        super.onRequestPermissionsResult(requestCode, permissions, grantResults);
        switch (requestCode) {
            case REQUEST_RECORD_AUDIO_PERMISSION:
                permissionToRecordAccepted = grantResults[0] == PackageManager.PERMISSION_GRANTED;
                startService(new Intent(AdminActivity.this, NoiseInformationService.class));
                break;
        }

    }

    @Override
    public void onClick(View view) {
        if (view == buttonAddQuestion) {
            startActivity(new Intent(AdminActivity.this, AddQuestionActivity.class));
        }
        if (view == buttonUsersLocationMap) {
            startActivity(new Intent(AdminActivity.this, MapsActivity.class));
        }
        if (view == buttonEMAScheduler) {
            updateButtonsState(buttonEMAScheduleCancel, buttonEMAScheduler);
            startAlarm();
        }
        if (view == buttonEMAScheduleCancel) {
            updateButtonsState(buttonEMAScheduler, buttonEMAScheduleCancel);
            cancelAlarm();
        }
        if (view == buttonSetupEMASchedule) {
            startActivity(new Intent(AdminActivity.this, SetupEMAActivity.class));
        }
        if (view == buttonStartSensorInfo) {
            settings.collectSensors = true;
            saveSettings();
            updateButtonsState(buttonStopSensorInfo, buttonStartSensorInfo);
            startService(new Intent(AdminActivity.this, SensorInformationService.class));
        }
        if (view == buttonStopSensorInfo) {
            settings.collectSensors = false;
            saveSettings();
            updateButtonsState(buttonStartSensorInfo, buttonStopSensorInfo);
            stopService(new Intent(AdminActivity.this, SensorInformationService.class));
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
            stopService(new Intent(AdminActivity.this, NoiseInformationService.class));
        }
    }

    private void cancelAlarm() {
        SharedPreferences prefs = this.getSharedPreferences(
                "com.tonmoy.autismema", Context.MODE_PRIVATE);
        String data = prefs.getString("EMASchedule", "");
        if (!data.isEmpty()) {
            ArrayList<EMAScheduleModel> list = new ArrayList<EMAScheduleModel>();
            GsonBuilder builder = new GsonBuilder();
            Gson gson = builder.create();
            list = gson.fromJson(data, new TypeToken<ArrayList<EMAScheduleModel>>() {
            }.getType());
            for (int i = 0; i < list.size(); i++) {
                mAlarmManager = (AlarmManager) getSystemService(ALARM_SERVICE);
                Intent notificationIntent = new Intent(this, NotificationPublisher.class);
                PendingIntent pendingIntent = PendingIntent.getBroadcast(this, i, notificationIntent, 0);
                mAlarmManager.cancel(pendingIntent);
            }
        }
    }

    public void startAlarm() {
        int notificationId = 1012;

        SharedPreferences prefs = this.getSharedPreferences(
                "com.tonmoy.autismema", Context.MODE_PRIVATE);
        String data = prefs.getString("EMASchedule", "");
        if (!data.isEmpty()) {
            ArrayList<EMAScheduleModel> list = new ArrayList<EMAScheduleModel>();
            GsonBuilder gsonbuilder = new GsonBuilder();
            Gson gson = gsonbuilder.create();
            list = gson.fromJson(data, new TypeToken<ArrayList<EMAScheduleModel>>() {
            }.getType());
            for (int i = 0; i < list.size(); i++) {
                EMAScheduleModel model = list.get(i);
                Notification.Builder builder = new Notification.Builder(this)
                        .setContentTitle("EMA ")
                        .setContentText("EMA Time!")
                        .setAutoCancel(true)
                        .setSmallIcon(R.drawable.ic_ema)
                        .setLargeIcon(((BitmapDrawable) getResources().getDrawable(R.drawable.ic_ema)).getBitmap())
                        .setSound(RingtoneManager.getDefaultUri(RingtoneManager.TYPE_NOTIFICATION));

                Intent intent = new Intent(this, QuestionnaireActivity.class);
                intent.putExtra("question_set", model.questionSet);
                PendingIntent activity = PendingIntent.getActivity(this, notificationId, intent, PendingIntent.FLAG_CANCEL_CURRENT);
                builder.setContentIntent(activity);

                Notification notification = builder.build();

                Intent notificationIntent = new Intent(this, NotificationPublisher.class);
                notificationIntent.putExtra(NotificationPublisher.NOTIFICATION_ID, notificationId);
                notificationIntent.putExtra(NotificationPublisher.NOTIFICATION, notification);
                notificationIntent.putExtra("question_set", model.questionSet);
                Log.d("tonmoy", notificationIntent.toUri(0));
                PendingIntent pendingIntent = PendingIntent.getBroadcast(this, i, notificationIntent, 0);

                mAlarmManager = (AlarmManager) getSystemService(ALARM_SERVICE);
                String arr[] = model.notificationTime.split(":");
                Calendar calendar = Calendar.getInstance();
                calendar.setTimeInMillis(System.currentTimeMillis());
                calendar.set(Calendar.HOUR_OF_DAY, Integer.parseInt(arr[0]));
                calendar.set(Calendar.MINUTE, Integer.parseInt(arr[1]));
                if (calendar.getTimeInMillis() < System.currentTimeMillis()) {
                    //make it tomorrow then
                    Log.d("tonmoy", "Set for tomorrow");
                    calendar.add(Calendar.DATE, 1);
                }
                Date date = calendar.getTime();

                mAlarmManager.setRepeating(AlarmManager.RTC_WAKEUP, calendar.getTimeInMillis(),
                        1000 * 60 * 60 * 24, pendingIntent);

                Toast.makeText(this, "EMA schedule has started.", Toast.LENGTH_SHORT).show();
            }

            // Enable {@code BootReceiver} to automatically restart when the
            // device is rebooted.
            //// TODO: you may need to reference the context by ApplicationActivity.class
            ComponentName receiver = new ComponentName(this, MyBootReceiver.class);
            PackageManager pm = getPackageManager();
            pm.setComponentEnabledSetting(receiver, PackageManager.COMPONENT_ENABLED_STATE_ENABLED,
                    PackageManager.DONT_KILL_APP);
        }

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
        if (settings.collectNoise) {
            updateButtonsState(buttonStopNoiseInfo, buttonStartNoiseInfo);
        } else {
            updateButtonsState(buttonStartNoiseInfo, buttonStopNoiseInfo);
        }
        if (settings.collectSensors) {
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
