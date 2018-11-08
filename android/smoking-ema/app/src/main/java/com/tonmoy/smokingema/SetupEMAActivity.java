package com.tonmoy.smokingema;

import android.app.TimePickerDialog;
import android.content.Context;
import android.content.SharedPreferences;
import android.support.v7.app.AppCompatActivity;
import android.os.Bundle;
import android.view.View;
import android.widget.Button;
import android.widget.EditText;
import android.widget.RadioButton;
import android.widget.RadioGroup;
import android.widget.TimePicker;
import android.widget.Toast;

import com.google.gson.Gson;
import com.google.gson.GsonBuilder;
import com.google.gson.reflect.TypeToken;
import com.tonmoy.smokingema.model.EMAScheduleModel;

import java.util.ArrayList;
import java.util.Calendar;

public class SetupEMAActivity extends AppCompatActivity implements View.OnClickListener {
    EditText ema1StartTime, ema1EndTime, ema1NotificationTime, ema2StartTime, ema2EndTime, ema2NotificationTime, ema3StartTime, ema3EndTime, ema3NotificationTime;
    Button buttonSave;

    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        setContentView(R.layout.activity_setup_ema);
        buttonSave = (Button) findViewById(R.id.buttonSave);
        ema1StartTime = (EditText) findViewById(R.id.ema1StartTime);
        ema1EndTime = (EditText) findViewById(R.id.ema1EndTime);
        ema1NotificationTime = (EditText) findViewById(R.id.ema1NotificationTime);
        ema2StartTime = (EditText) findViewById(R.id.ema2StartTime);
        ema2EndTime = (EditText) findViewById(R.id.ema2EndTime);
        ema2NotificationTime = (EditText) findViewById(R.id.ema2NotificationTime);
        ema3StartTime = (EditText) findViewById(R.id.ema3StartTime);
        ema3EndTime = (EditText) findViewById(R.id.ema3EndTime);
        ema3NotificationTime = (EditText) findViewById(R.id.ema3NotificationTime);
        buttonSave.setOnClickListener(this);
        ema1StartTime.setOnClickListener(this);
        ema1EndTime.setOnClickListener(this);
        ema1NotificationTime.setOnClickListener(this);
        ema2StartTime.setOnClickListener(this);
        ema2EndTime.setOnClickListener(this);
        ema2NotificationTime.setOnClickListener(this);
        ema3StartTime.setOnClickListener(this);
        ema3EndTime.setOnClickListener(this);
        ema3NotificationTime.setOnClickListener(this);
        loadSavedValues();
    }

    private void loadSavedValues() {
        SharedPreferences prefs = this.getSharedPreferences(
                "com.tonmoy.autismema", Context.MODE_PRIVATE);
        String data = prefs.getString("EMASchedule", "");
        if (!data.isEmpty()) {
            ArrayList<EMAScheduleModel> list = new ArrayList<EMAScheduleModel>();
            GsonBuilder builder = new GsonBuilder();
            Gson gson = builder.create();
            list = gson.fromJson(data, new TypeToken<ArrayList<EMAScheduleModel>>() {
            }.getType());
            ema1StartTime.setText(list.get(0).startTime);
            ema1EndTime.setText(list.get(0).endTime);
            ema1NotificationTime.setText(list.get(0).notificationTime);
            ema2StartTime.setText(list.get(1).startTime);
            ema2EndTime.setText(list.get(1).endTime);
            ema2NotificationTime.setText(list.get(1).notificationTime);
            ema3StartTime.setText(list.get(2).startTime);
            ema3EndTime.setText(list.get(2).endTime);
            ema3NotificationTime.setText(list.get(2).notificationTime);

        }

    }

    private void emaTimePicker(final EditText et, int hour, int minute) {
        TimePickerDialog mTimePicker;
        mTimePicker = new TimePickerDialog(SetupEMAActivity.this, new TimePickerDialog.OnTimeSetListener() {
            @Override
            public void onTimeSet(TimePicker timePicker, int selectedHour, int selectedMinute) {
                et.setText(selectedHour + ":" + selectedMinute);
            }
        }, hour, minute, true);//Yes 24 hour time
        mTimePicker.setTitle("Select Time");
        mTimePicker.show();
    }

    @Override
    public void onClick(View view) {
        Calendar mcurrentTime = Calendar.getInstance();
        int hour = mcurrentTime.get(Calendar.HOUR_OF_DAY);
        int minute = mcurrentTime.get(Calendar.MINUTE);
        switch (view.getId()) {
            case R.id.buttonSave:
                saveEMASchedule();
                break;
            case R.id.ema1StartTime:

            case R.id.ema1EndTime:

            case R.id.ema1NotificationTime:

            case R.id.ema2StartTime:

            case R.id.ema2EndTime:

            case R.id.ema2NotificationTime:

            case R.id.ema3StartTime:

            case R.id.ema3EndTime:

            case R.id.ema3NotificationTime:
                emaTimePicker((EditText) view, hour, minute);
                break;
            default:
                break;
        }
    }

    private void saveEMASchedule() {
        ArrayList<EMAScheduleModel> list = new ArrayList<EMAScheduleModel>();
        list.add(buildEMAModel(ema1StartTime.getText().toString(), ema1EndTime.getText().toString
                (), ema1NotificationTime.getText().toString(), "new_smoking_ema"));
        list.add(buildEMAModel(ema2StartTime.getText().toString(), ema2EndTime.getText().toString
                (), ema2NotificationTime.getText().toString(), "new_smoking_ema"));
        list.add(buildEMAModel(ema3StartTime.getText().toString(), ema3EndTime.getText().toString
                (), ema3NotificationTime.getText().toString(), "new_smoking_ema"));
        GsonBuilder builder = new GsonBuilder();
        Gson gson = builder.create();
        System.out.println(gson.toJson(list));
        SharedPreferences prefs = this.getSharedPreferences(
                "com.tonmoy.autismema", Context.MODE_PRIVATE);
        prefs.edit().putString("EMASchedule", gson.toJson(list)).commit();
        Toast.makeText(this, "EMA Schedule has been saved.", Toast.LENGTH_SHORT).show();
        finish();
    }

    private EMAScheduleModel buildEMAModel(String startTime, String endTime, String notificationTime, String questionSet) {
        EMAScheduleModel model = new EMAScheduleModel();
        model.startTime = startTime;
        model.endTime = endTime;
        model.notificationTime = notificationTime;
        model.questionSet = questionSet;
        return model;
    }
}


/*
[{"endTime":"11:59","notificationTime":"9:00","questionSet":"general","startTime":"8:0"},{"endTime":"16:59","notificationTime":"1:30","questionSet":"general","startTime":"12:00"},{"endTime":"23:59","notificationTime":"18:00","questionSet":"general2","startTime":"17:00"}]
 */