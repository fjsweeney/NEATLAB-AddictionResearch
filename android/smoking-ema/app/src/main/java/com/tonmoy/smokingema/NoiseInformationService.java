package com.tonmoy.smokingema;

import android.app.Service;
import android.content.Intent;
import android.content.pm.PackageManager;
import android.media.MediaRecorder;
import android.os.Handler;
import android.os.IBinder;
import android.support.annotation.NonNull;
import android.support.v4.app.ActivityCompat;
import android.util.Log;
import android.widget.Toast;

import com.google.firebase.auth.FirebaseAuth;
import com.google.firebase.database.DatabaseReference;
import com.google.firebase.database.FirebaseDatabase;

import java.io.IOException;

public class NoiseInformationService extends Service implements ActivityCompat.OnRequestPermissionsResultCallback {
    private static final int REQUEST_RECORD_AUDIO_PERMISSION = 200;
    private static int TIME_FREQUENCY = 3000;
    Handler handler;
    Runnable runable;
    private static String mFileName = null;
    private boolean permissionToRecordAccepted = false;
    private String[] permissions = {android.Manifest.permission.RECORD_AUDIO};
    private MediaRecorder mRecorder = null;
    int index = 0;
    static boolean isRunning = false;

    public NoiseInformationService() {
    }

    @Override
    public void onCreate() {
        super.onCreate();
        mFileName = getExternalCacheDir().getAbsolutePath();
        mFileName += "/audiorecord.3gp";
        //startRecording();
        isRunning = true;
        startNoiseDetect();
        Toast.makeText(this,"Noise collection started.",Toast.LENGTH_LONG).show();
    }

    @Override
    public IBinder onBind(Intent intent) {
        // TODO: Return the communication channel to the service.
        return null;
    }

    @Override
    public void onRequestPermissionsResult(int requestCode, @NonNull String[] permissions, @NonNull int[] grantResults) {
        switch (requestCode) {
            case REQUEST_RECORD_AUDIO_PERMISSION:
                permissionToRecordAccepted = grantResults[0] == PackageManager.PERMISSION_GRANTED;
                break;
        }
        if (!permissionToRecordAccepted) stopSelf();
    }


    @Override
    public void onDestroy() {
        // TODO Auto-generated method stub
        stopRecording();
        if (handler != null) {
            handler.removeCallbacks(runable);
        }
        isRunning = false;
        super.onDestroy();
    }

    private void uploadNoiceInfo(String sensor, String data) {
        FirebaseDatabase database = FirebaseDatabase.getInstance();
        String currentUserId = FirebaseAuth.getInstance().getCurrentUser().getUid();
        DatabaseReference refUsersLocation = database.getReference().child("users_data").child(currentUserId).child("sensors").child(sensor);
        refUsersLocation.child(System.currentTimeMillis() + "").setValue(data);
    }


    private void startRecording() {
        mRecorder = new MediaRecorder();
        mRecorder.setAudioSource(MediaRecorder.AudioSource.MIC);
        mRecorder.setOutputFormat(MediaRecorder.OutputFormat.THREE_GPP);
        mRecorder.setOutputFile(mFileName);
        mRecorder.setAudioEncoder(MediaRecorder.AudioEncoder.AMR_NB);

        try {
            mRecorder.prepare();
        } catch (IOException e) {
            Log.d("tonmoy", "prepare() failed");
        }
        mRecorder.start();
    }

    private void stopRecording() {
        if(mRecorder!=null) {
            mRecorder.stop();
            mRecorder.release();
            mRecorder = null;
        }
    }

    public double getAmplitude() {
        if (mRecorder != null)
            return mRecorder.getMaxAmplitude();
        else
            return 0;

    }

    private void startNoiseDetect() {
        handler = new Handler();
        runable = new Runnable() {
            @Override
            public void run() {
                try {
                    Log.d("tonmoy", "index :" + index);
                    if (index == 0) {
                        startRecording();
                    } else if (index >= 100) {
                        stopRecording();
                        index = -1;
                    } else {
                        double amp = getAmplitude();
                        uploadNoiceInfo("noise", amp + "");
                    }
                    index++;

                } catch (Exception e) {
                    // TODO: handle exception
                } finally {
                    handler.postDelayed(
                            this,
                            TIME_FREQUENCY);
                }
            }

        };

        handler.postDelayed(
                runable,
                TIME_FREQUENCY);
    }
}

