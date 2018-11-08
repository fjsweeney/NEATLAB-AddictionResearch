package com.tonmoy.smokingema;

import android.app.Activity;
import android.content.Intent;
import android.os.Bundle;
import android.util.Log;
import android.view.View;
import android.widget.Button;
import android.widget.Toast;

import com.tonmoy.smokingema.questionnaire.QuestionnaireActivity;

public class EMAAlertDialogActivity extends Activity implements View.OnClickListener {
    Button buttonCancel, buttonEMA;
    String questionSet = "new_smoking_ema";

    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        //requestWindowFeature(Window.FEATURE_NO_TITLE); //hide activity title
        setContentView(R.layout.activity_emaalert_dialog);
        this.setFinishOnTouchOutside(false);
        questionSet = getIntent().getStringExtra("question_set");
        buttonCancel = (Button) findViewById(R.id.buttonCancel);
        buttonEMA = (Button) findViewById(R.id.buttonEMA);
        buttonCancel.setOnClickListener(this);
        buttonEMA.setOnClickListener(this);
        Log.d("tonmoy", "EMAAlertDialogActivity: "+questionSet);
    }

    @Override
    public void onClick(View view) {
        if (view == buttonCancel) {
            this.finish();
        } else if (view == buttonEMA) {
            Toast.makeText(this, questionSet, Toast.LENGTH_LONG).show();
            Intent intent = new Intent(this, QuestionnaireActivity.class);
            intent.putExtra("question_set", questionSet);
            startActivity(intent);

            this.finish();

        }
    }
}
