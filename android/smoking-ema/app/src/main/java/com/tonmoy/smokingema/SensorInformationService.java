package com.tonmoy.smokingema;

import android.app.Service;
import android.content.Intent;
import android.hardware.Sensor;
import android.hardware.SensorEvent;
import android.hardware.SensorEventListener;
import android.hardware.SensorManager;
import android.os.IBinder;
import android.util.Log;
import android.widget.Toast;

import com.google.firebase.auth.FirebaseAuth;
import com.google.firebase.database.DatabaseReference;
import com.google.firebase.database.FirebaseDatabase;

import java.util.List;

public class SensorInformationService extends Service implements SensorEventListener {

    SensorManager mSensorManager;
    static boolean isRunning = false;
    public SensorInformationService() {
    }

    @Override
    public void onCreate() {
        super.onCreate();
        isRunning = true;
        Toast.makeText(this,"Ambient light collection started.",Toast.LENGTH_LONG).show();
        getSensorData();
    }

    @Override
    public IBinder onBind(Intent intent) {
        // TODO: Return the communication channel to the service.
        return null;
    }



    @Override
    public void onSensorChanged(SensorEvent sensorEvent) {
        if (sensorEvent.sensor.getType() == Sensor.TYPE_STEP_COUNTER) {
            String msg = "Count: " + (int) sensorEvent.values[0];
            uploadSensorInfo("step_count", "" + sensorEvent.values[0]);

        } else if (sensorEvent.sensor.getType() == Sensor.TYPE_LIGHT) {
            uploadSensorInfo("light", "" + sensorEvent.values[0]);

        } else
            Log.d("tonmoy", "Unknown sensor type " + sensorEvent.sensor.getType() + " Name: " + sensorEvent.sensor.getName());

        //  mTextViewLog.setText("Log :" + text);
    }

    @Override
    public void onAccuracyChanged(Sensor sensor, int i) {

    }

    @Override
    public void onDestroy() {
        // TODO Auto-generated method stub
        mSensorManager.unregisterListener(this);
        isRunning = false;
        super.onDestroy();
    }

    private void uploadSensorInfo(String sensor, String data) {
        FirebaseDatabase database = FirebaseDatabase.getInstance();
        String currentUserId = FirebaseAuth.getInstance().getCurrentUser().getUid();
        DatabaseReference refUsersLocation = database.getReference().child("users_data").child(currentUserId).child("sensors").child(sensor);
        refUsersLocation.child(System.currentTimeMillis() + "").setValue(data);

    }

    private void getSensorData() {
        mSensorManager = ((SensorManager) getSystemService(SENSOR_SERVICE));
        List<Sensor> sensors = mSensorManager.getSensorList(Sensor.TYPE_ALL);
        for (Sensor msensor : sensors) {
            Log.d("tonmoy", msensor.toString());
        }

        Sensor mStepCountSensor = mSensorManager.getDefaultSensor(Sensor.TYPE_STEP_COUNTER);
        // Sensor mHeartRateSensor = mSensorManager.getDefaultSensor(Sensor.TYPE_HEART_RATE);
        Sensor mLightSensor = mSensorManager.getDefaultSensor(Sensor.TYPE_LIGHT);

        //  mSensorManager.registerListener(this, mStepCountSensor, SensorManager.SENSOR_DELAY_NORMAL);
        //  mSensorManager.registerListener(this, mHeartRateSensor, SensorManager.SENSOR_DELAY_NORMAL);
        mSensorManager.registerListener(this, mStepCountSensor, SensorManager.SENSOR_DELAY_NORMAL);
        mSensorManager.registerListener(this, mLightSensor, SensorManager.SENSOR_DELAY_NORMAL);
    }
}

