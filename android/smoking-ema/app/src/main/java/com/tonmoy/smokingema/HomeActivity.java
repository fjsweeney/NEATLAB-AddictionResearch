package com.tonmoy.smokingema;

import android.content.Context;
import android.content.DialogInterface;
import android.content.Intent;
import android.content.SharedPreferences;
import android.os.Bundle;
import android.support.v7.app.AlertDialog;
import android.support.v7.app.AppCompatActivity;
import android.view.View;
import android.widget.Button;
import android.widget.SeekBar;
import android.widget.TextView;
import android.widget.Toast;

import com.google.firebase.auth.FirebaseAuth;
import com.google.firebase.database.DatabaseReference;
import com.google.firebase.database.FirebaseDatabase;
import com.google.gson.Gson;
import com.google.gson.GsonBuilder;
import com.google.gson.reflect.TypeToken;
import com.tonmoy.smokingema.admin.AdminLoginActivity;
import com.tonmoy.smokingema.model.EMAScheduleModel;
import com.tonmoy.smokingema.model.SelfReportType;
import com.tonmoy.smokingema.model.SmokingEpisodeModel;
import com.tonmoy.smokingema.model.SmokingUrgeModel;
import com.tonmoy.smokingema.model.StressModel;
import com.tonmoy.smokingema.questionnaire.QuestionnaireActivity;

import java.text.SimpleDateFormat;
import java.util.ArrayList;
import java.util.Calendar;

public class HomeActivity extends AppCompatActivity implements View.OnClickListener {
    Button buttonQuestionnaire, buttonAdmin, buttonSettings, buttonSelfReportStress,
            buttonSelfReportSmokingLapse, buttonSelfReportSmokingUrge;
    TextView textViewUser;
    String questionSet = "new_smoking_ema";
    SeekBar stressSeekBar, smokingUrgeSeekBar;

    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        setContentView(R.layout.activity_home);

        // Assign layout elements to objects.
        buttonAdmin = (Button) findViewById(R.id.buttonAdmin);
        buttonQuestionnaire = (Button) findViewById(R.id.buttonQuestionnaire);
        buttonSettings = (Button) findViewById(R.id.buttonSettings);
        buttonSelfReportStress = (Button) findViewById(R.id.buttonSelfReportStress);
        buttonSelfReportSmokingLapse = (Button) findViewById(R.id.buttonSelfReportSmoke);
        buttonSelfReportSmokingUrge = (Button) findViewById(R.id.buttonSelfReportSmokingUrge);
        textViewUser = (TextView) findViewById(R.id.textviewUser);
        stressSeekBar = (SeekBar) findViewById(R.id.likertSeekBar);
        smokingUrgeSeekBar = (SeekBar) findViewById(R.id.smokingUrgeSeekBar);

        // Setup onClick listeners
        buttonSettings.setOnClickListener(this);
        buttonQuestionnaire.setOnClickListener(this);
        buttonAdmin.setOnClickListener(this);
        buttonSelfReportStress.setOnClickListener(this);
        buttonSelfReportSmokingLapse.setOnClickListener(this);
        buttonSelfReportSmokingUrge.setOnClickListener(this);

        if(FirebaseAuth.getInstance().getCurrentUser()!=null)
        {
            String name = FirebaseAuth.getInstance().getCurrentUser().getDisplayName();
            textViewUser.setText(name);
        }
    }

    @Override
    protected void onResume() {
        super.onResume();
        selectQuestionSet();
    }

    private void selectQuestionSet() {
        SharedPreferences prefs = this.getSharedPreferences(
                "com.tonmoy.autismema", Context.MODE_PRIVATE);
        String data = prefs.getString("EMASchedule", "");
        if (!data.isEmpty()) {
            ArrayList<EMAScheduleModel> list = new ArrayList<EMAScheduleModel>();
            GsonBuilder builder = new GsonBuilder();
            Gson gson = builder.create();
            list = gson.fromJson(data, new TypeToken<ArrayList<EMAScheduleModel>>() {
            }.getType());
            String arr[] = list.get(0).endTime.split(":");
            Calendar endTime1 = Calendar.getInstance();
            endTime1.set(Calendar.HOUR_OF_DAY, Integer.parseInt(arr[0]));
            endTime1.set(Calendar.MINUTE, Integer.parseInt(arr[1]));
            arr = list.get(1).endTime.split(":");
            Calendar endTime2 = Calendar.getInstance();
            endTime2.set(Calendar.HOUR_OF_DAY, Integer.parseInt(arr[0]));
            endTime2.set(Calendar.MINUTE, Integer.parseInt(arr[1]));
            arr = list.get(2).endTime.split(":");
            Calendar endTime3 = Calendar.getInstance();
            endTime3.set(Calendar.HOUR_OF_DAY, Integer.parseInt(arr[0]));
            endTime3.set(Calendar.MINUTE, Integer.parseInt(arr[1]));

            long curTime = System.currentTimeMillis();
            if (endTime1.getTimeInMillis() > curTime) {
                questionSet = list.get(0).questionSet;
            } else if (endTime2.getTimeInMillis() > curTime) {
                questionSet = list.get(1).questionSet;
            } else if (endTime3.getTimeInMillis() > curTime) {
                questionSet = list.get(2).questionSet;
            } else {
                //do nothing at this moment. default is general question set
            }
            // Toast.makeText(HomeActivity.this,questionSet,Toast.LENGTH_LONG).show();

        }
    }

    @Override
    public void onClick(View view) {
        if (view == buttonAdmin) {
            startActivity(new Intent(HomeActivity.this, AdminLoginActivity.class));

        }
        if (view == buttonQuestionnaire) {
            Intent intent = new Intent(HomeActivity.this, QuestionnaireActivity.class);
            intent.putExtra("question_set", questionSet);
            startActivity(intent);
        }
        if (view == buttonSettings) {
            startActivity(new Intent(HomeActivity.this, SettingsActivity.class));
        }
        if (view == buttonSelfReportStress) {
            showSelfReportUploadAlert("Submit Stress Status", "Are you sure?",
                    SelfReportType.STRESS);
        }
        if (view == buttonSelfReportSmokingLapse) {
            showSelfReportUploadAlert("Submit Smoking Episode", "Are you sure?",
                    SelfReportType.SMOKING);
        }
        if (view == buttonSelfReportSmokingUrge) {
            showSelfReportUploadAlert("Submit Smoking Urge Status", "Are you sure?",
                    SelfReportType.URGE);
        }
    }

    private void uploadStressValue(int value) {
        StressModel model = new StressModel();
        SimpleDateFormat formatter = new SimpleDateFormat("MM/dd/yyyy HH:mm");
        Calendar calendar = Calendar.getInstance();
        model.time = formatter.format(calendar.getTime());
        model.timeUTC = calendar.getTimeInMillis();
        model.stressValue = value;
        FirebaseDatabase database = FirebaseDatabase.getInstance();
        String currentUserId = FirebaseAuth.getInstance().getCurrentUser().getUid();
        DatabaseReference refUsersLocation = database.getReference().child("users_data").child(currentUserId).child("self_reported_stress");
        refUsersLocation.child(calendar.getTime().toString()).setValue(model);
        Toast.makeText(HomeActivity.this, "Stress value submitted successfully.",
                Toast.LENGTH_LONG).show();
    }

    private void uploadUrgeValue(int value) {
        SmokingUrgeModel model = new SmokingUrgeModel();
        SimpleDateFormat formatter = new SimpleDateFormat("MM/dd/yyyy HH:mm");
        Calendar calendar = Calendar.getInstance();
        model.time = formatter.format(calendar.getTime());
        model.timeUTC = calendar.getTimeInMillis();
        model.urgeValue = value;
        FirebaseDatabase database = FirebaseDatabase.getInstance();
        String currentUserId = FirebaseAuth.getInstance().getCurrentUser().getUid();
        DatabaseReference refUsersLocation = database.getReference().child("users_data").child
                (currentUserId).child("self_reported_urge");
        refUsersLocation.child(calendar.getTime().toString()).setValue(model);
        Toast.makeText(HomeActivity.this, "Urge value submitted successfully.",
                Toast.LENGTH_LONG).show();
    }

    private void uploadSmokingEpisode() {
        SmokingEpisodeModel model = new SmokingEpisodeModel();
        SimpleDateFormat formatter = new SimpleDateFormat("MM/dd/yyyy HH:mm");
        Calendar calendar = Calendar.getInstance();
        model.time = formatter.format(calendar.getTime());
        model.timeUTC = calendar.getTimeInMillis();
        FirebaseDatabase database = FirebaseDatabase.getInstance();
        String currentUserId = FirebaseAuth.getInstance().getCurrentUser().getUid();
        DatabaseReference refUsersLocation = database.getReference().child("users_data").child
                (currentUserId).child("self_reported_smoking_episode");
        refUsersLocation.child(calendar.getTime().toString()).setValue(model);
        Toast.makeText(HomeActivity.this, "Smoking episode submitted successfully.",
                Toast.LENGTH_LONG).show();
    }

    public void showSelfReportUploadAlert(String title, String msg, final SelfReportType uploadType) {
        AlertDialog alertDialog = new AlertDialog.Builder(HomeActivity.this).create();
        alertDialog.setTitle(title);
        alertDialog.setMessage(msg);
        alertDialog.setButton(AlertDialog.BUTTON_POSITIVE, "OK",
                new DialogInterface.OnClickListener() {
                    public void onClick(DialogInterface dialog, int which) {
                        switch(uploadType) {
                            case STRESS:
                                uploadStressValue(stressSeekBar.getProgress());
                                break;
                            case SMOKING:
                                uploadSmokingEpisode();
                                showEMARequestAlert();
                                break;
                            case URGE:
                                uploadUrgeValue(smokingUrgeSeekBar.getProgress());
                        }
                    }
                });
        alertDialog.setButton(AlertDialog.BUTTON_NEGATIVE, "Cancel",
                new DialogInterface.OnClickListener() {
                    public void onClick(DialogInterface dialog, int which) {
                        dialog.dismiss();
                    }
                });
        alertDialog.show();
    }

    public void showEMARequestAlert() {
        AlertDialog alertDialog = new AlertDialog.Builder(HomeActivity.this).create();
        alertDialog.setTitle("EMA?");
        alertDialog.setMessage("Would you like to fill out an EMA for this smoking episode?");
        alertDialog.setButton(AlertDialog.BUTTON_POSITIVE, "OK", new DialogInterface.OnClickListener() {
            @Override
            public void onClick(DialogInterface dialogInterface, int i) {
                Intent intent = new Intent(HomeActivity.this, QuestionnaireActivity.class);
                intent.putExtra("question_set", questionSet);
                startActivity(intent);
            }
        });
        alertDialog.setButton(AlertDialog.BUTTON_NEGATIVE, "Cancel",
                new DialogInterface.OnClickListener() {
                    public void onClick(DialogInterface dialog, int which) {
                        dialog.dismiss();
                    }
                });
        alertDialog.show();
    }
}
