package com.tonmoy.smokingema.admin;

import android.content.Context;
import android.content.SharedPreferences;
import android.support.v7.app.AppCompatActivity;
import android.os.Bundle;
import android.text.TextUtils;
import android.util.Log;
import android.view.View;
import android.widget.AdapterView;
import android.widget.Button;
import android.widget.EditText;
import android.widget.Spinner;
import android.widget.Toast;

import com.google.firebase.database.DataSnapshot;
import com.google.firebase.database.DatabaseError;
import com.google.firebase.database.DatabaseReference;
import com.google.firebase.database.FirebaseDatabase;
import com.google.firebase.database.Query;
import com.google.firebase.database.ValueEventListener;
import com.tonmoy.smokingema.R;
import com.tonmoy.smokingema.model.Answer;
import com.tonmoy.smokingema.model.Question;

import java.util.ArrayList;
import java.util.HashMap;
import java.util.Map;

public class AddQuestionActivity extends AppCompatActivity implements View.OnClickListener {
    Button buttonAddQuestion;
    EditText editTextQuestionSet, editTextQuestion, editTextNextQuestion, editTextAnswer1,
            editTextAnswer2, editTextAnswer3, editTextAnswer4, editTextAnswer5, editTextAnswer6,
            editTextAnswer7, editTextAnswer8;
    Spinner spinnerQuestionType;
    int questionNumber = 0;
    DatabaseReference refQSets, refQuestions, refAnswers;
    SharedPreferences prefs;

    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        setContentView(R.layout.activity_add_question);
        prefs = this.getSharedPreferences(
                "com.tonmoy.autismema.admin", Context.MODE_PRIVATE);

        buttonAddQuestion = (Button) findViewById(R.id.buttonAddQuestion);
        buttonAddQuestion.setOnClickListener(this);
        editTextQuestionSet = (EditText) findViewById(R.id.editTextQuestionSet);
        editTextQuestion = (EditText) findViewById(R.id.editTextQuestion);
        editTextNextQuestion = (EditText) findViewById(R.id.editTextNextQuestion);
        editTextAnswer1 = (EditText) findViewById(R.id.editTextAnswer1);
        editTextAnswer2 = (EditText) findViewById(R.id.editTextAnswer2);
        editTextAnswer3 = (EditText) findViewById(R.id.editTextAnswer3);
        editTextAnswer4 = (EditText) findViewById(R.id.editTextAnswer4);
        editTextAnswer5 = (EditText) findViewById(R.id.editTextAnswer5);
        editTextAnswer6 = (EditText) findViewById(R.id.editTextAnswer6);
        editTextAnswer7 = (EditText) findViewById(R.id.editTextAnswer7);
        editTextAnswer8 = (EditText) findViewById(R.id.editTextAnswer8);
        spinnerQuestionType = (Spinner) findViewById(R.id.spinnerQuestionType);
        spinnerQuestionType.setOnItemSelectedListener(new AdapterView.OnItemSelectedListener() {
            @Override
            public void onItemSelected(AdapterView<?> adapterView, View view, int i, long l) {
                if (i == 1 || i == 3) {
                    editTextAnswer1.setVisibility(View.GONE);
                    editTextAnswer2.setVisibility(View.GONE);
                    editTextAnswer3.setVisibility(View.GONE);
                    editTextAnswer4.setVisibility(View.GONE);
                    editTextAnswer5.setVisibility(View.GONE);
                    editTextAnswer6.setVisibility(View.GONE);
                    editTextAnswer7.setVisibility(View.GONE);
                    editTextAnswer8.setVisibility(View.GONE);
                } else {
                    editTextAnswer1.setVisibility(View.VISIBLE);
                    editTextAnswer2.setVisibility(View.VISIBLE);
                    editTextAnswer3.setVisibility(View.VISIBLE);
                    editTextAnswer4.setVisibility(View.VISIBLE);
                    editTextAnswer5.setVisibility(View.VISIBLE);
                    editTextAnswer6.setVisibility(View.VISIBLE);
                    editTextAnswer7.setVisibility(View.VISIBLE);
                    editTextAnswer8.setVisibility(View.VISIBLE);
                }
            }

            @Override
            public void onNothingSelected(AdapterView<?> adapterView) {

            }
        });


    }

    @Override
    public void onClick(View view) {
        if (view == buttonAddQuestion) {

            FirebaseDatabase database = FirebaseDatabase.getInstance();
            refQSets = database.getReference().child("question_sets");
            refQuestions = database.getReference().child("questions");
            refAnswers = database.getReference().child("answers");

            ArrayList<String> answers = new ArrayList<String>();
            if (!TextUtils.isEmpty(editTextAnswer1.getText().toString())) {
                answers.add(editTextAnswer1.getText().toString());
            }
            if (!TextUtils.isEmpty(editTextAnswer2.getText().toString())) {
                answers.add(editTextAnswer2.getText().toString());
            }
            if (!TextUtils.isEmpty(editTextAnswer3.getText().toString())) {
                answers.add(editTextAnswer3.getText().toString());
            }
            if (!TextUtils.isEmpty(editTextAnswer4.getText().toString())) {
                answers.add(editTextAnswer4.getText().toString());
            }
            if (!TextUtils.isEmpty(editTextAnswer5.getText().toString())) {
                answers.add(editTextAnswer5.getText().toString());
            }
            if (!TextUtils.isEmpty(editTextAnswer6.getText().toString())) {
                answers.add(editTextAnswer6.getText().toString());
            }
            if (!TextUtils.isEmpty(editTextAnswer7.getText().toString())) {
                answers.add(editTextAnswer7.getText().toString());
            }
            if (!TextUtils.isEmpty(editTextAnswer8.getText().toString())) {
                answers.add(editTextAnswer8.getText().toString());
            }

            Map<String, Answer> answersHashMap = new HashMap<String, Answer>();
            Map<String, Answer> qSetAnswersHashMap = new HashMap<String, Answer>();
            int i = 1;
            for (String answer : answers) {
                DatabaseReference refAns = refAnswers.push();
                String ansId = refAns.getKey();
                Answer ans = new Answer(ansId, answer, null);
                Answer ansWithNextQues = new Answer(ansId, answer, editTextNextQuestion.getText().toString());
                refAns.setValue(ans);
                answersHashMap.put(i + "", ans);
                qSetAnswersHashMap.put(i + "", ansWithNextQues);
                i++;
            }
            if (i == 1) {
                qSetAnswersHashMap.put(i + "", new Answer("", "", editTextNextQuestion.getText().toString()));
            }

            DatabaseReference refQues = refQuestions.push();
            String questionId = refQues.getKey();
            Question q = new Question(questionId, editTextQuestion.getText().toString(), (spinnerQuestionType.getSelectedItemPosition() + 1) + "", spinnerQuestionType.getSelectedItem().toString(), answersHashMap);
            final Question quesForQSet = new Question(questionId, editTextQuestion.getText().toString(), (spinnerQuestionType.getSelectedItemPosition() + 1) + "", spinnerQuestionType.getSelectedItem().toString(), qSetAnswersHashMap);
            refQues.setValue(q);

            questionNumber = 0;
            //TODO LastQNumber should be based on questionset
            final int savedLastQuestionNumber  = prefs.getInt("LastQNumber", 0);
            DatabaseReference refQset = refQSets.child(editTextQuestionSet.getText().toString());
            Query lastQuery = refQset.child("question").orderByKey().limitToLast(1);
            lastQuery.keepSynced(true);
            lastQuery.addListenerForSingleValueEvent(new ValueEventListener() {
                @Override
                public void onDataChange(DataSnapshot dataSnapshot) {
                    for (DataSnapshot ds : dataSnapshot.getChildren()) {
                        questionNumber = Integer.parseInt(ds.getKey());
                        Log.d("tonmoy", "" + questionNumber);
                    }
                    questionNumber++;
                    questionNumber =Math.max(questionNumber,savedLastQuestionNumber+1);
                    refQSets.child(editTextQuestionSet.getText().toString()).child("question").child("" + questionNumber).setValue(quesForQSet);
                    prefs.edit().putInt("LastQNumber", questionNumber).commit();
                }

                @Override
                public void onCancelled(DatabaseError databaseError) {
                    //Handle possible errors.
                }
            });

            Toast.makeText(this, String.format("Question %d created", savedLastQuestionNumber + 1),
                    Toast
                    .LENGTH_SHORT).show();


//            String questionId =refQues.getKey();
//
//            Question q1 = new Question("1", "why are you stressed?", "1", "multiple choice single answer", answersHashMap);
//            qus.child("1").setValue(q1);
        }
    }
}
