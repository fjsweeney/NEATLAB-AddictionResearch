package com.tonmoy.smokingema.questionnaire;

import android.content.Context;
import android.content.DialogInterface;
import android.content.SharedPreferences;
import android.os.Bundle;
import android.support.v4.app.Fragment;
import android.support.v4.app.FragmentManager;
import android.support.v4.app.FragmentStatePagerAdapter;
import android.support.v4.view.PagerAdapter;
import android.support.v4.view.ViewPager;
import android.support.v7.app.AlertDialog;
import android.support.v7.app.AppCompatActivity;
import android.util.Log;
import android.view.View;
import android.widget.Button;
import android.widget.Toast;

import com.google.firebase.auth.FirebaseAuth;
import com.google.firebase.database.DataSnapshot;
import com.google.firebase.database.DatabaseError;
import com.google.firebase.database.DatabaseReference;
import com.google.firebase.database.FirebaseDatabase;
import com.google.firebase.database.Query;
import com.google.firebase.database.ValueEventListener;
import com.tonmoy.smokingema.R;
import com.tonmoy.smokingema.interfaces.QuestionnaireListener;
import com.tonmoy.smokingema.model.EMAAnswer;
import com.tonmoy.smokingema.model.QuestionType;
import com.tonmoy.smokingema.model.RetrievedQuestion;
import com.tonmoy.smokingema.model.UsersAnswer;

import java.util.HashMap;


public class QuestionnaireActivity extends AppCompatActivity implements View.OnClickListener, QuestionnaireListener {

    /**
     * The number of pages (wizard steps) to show in this demo.
     */
    //private static final int NUM_PAGES = 5;

    /**
     * The pager widget, which handles animation and allows swiping horizontally to access previous
     * and next wizard steps.
     */
    private ViewPager mPager;
    Button buttonSkip, buttonNext;
    public String questionSet = "new_smoking_ema";

    /**
     * The pager adapter, which provides the pages to the view pager widget.
     */
    private PagerAdapter mPagerAdapter;
    HashMap<Integer, RetrievedQuestion> questionMap = new HashMap<Integer, RetrievedQuestion>();
    HashMap<String, EMAAnswer> userEmaAnswerMap = new HashMap<String, EMAAnswer>();

    DatabaseReference refUsersData;
    int emaIndex = 0;
    SharedPreferences prefs;
    int nextQuestion = 1;

    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        setContentView(R.layout.activity_questionnaire);

        Log.d("tonmoy", FirebaseAuth.getInstance().getCurrentUser().getUid() + "");
        prefs = this.getSharedPreferences(
                "com.tonmoy.autismema.questionnaire", Context.MODE_PRIVATE);

        questionSet = getIntent().getStringExtra("question_set");

        // Instantiate a ViewPager and a PagerAdapter.
        mPager = (ViewPager) findViewById(R.id.pager);
        mPagerAdapter = new ScreenSlidePagerAdapter(getSupportFragmentManager());

        // Setup skip and next buttons
        buttonSkip = (Button) findViewById(R.id.buttonSkip);
        buttonNext = (Button) findViewById(R.id.buttonNext);
        buttonSkip.setOnClickListener(this);
        buttonNext.setOnClickListener(this);

        final DatabaseReference ref = FirebaseDatabase.getInstance().getReference().child("question_sets").child(questionSet).child("question");
        ref.addListenerForSingleValueEvent(
            new ValueEventListener() {
                @Override
                public void onDataChange(DataSnapshot dataSnapshot) {
                    //Get map of users in datasnapshot
                    for (DataSnapshot ds : dataSnapshot.getChildren()) {
                        Log.d("tonmoy", ds.getValue().toString());
                        RetrievedQuestion question = ds.getValue(RetrievedQuestion.class);
                        questionMap.put(Integer.parseInt(question.orderId), question);
                    }
                    mPager.setAdapter(mPagerAdapter);
                }

                @Override
                public void onCancelled(DatabaseError databaseError) {
                    //handle databaseError
                }
            });
    }


    @Override
    public void onBackPressed() {
        showExitWarningAlert("Exit?", "No data will be saved. Do you want to Proceed?");
        //super.onBackPressed();
    }

    @Override
    public void onClick(View view) {
        if (view == buttonSkip) {

            // Remove any answers that may have been added to the answer map.
            int orderId = mPager.getCurrentItem();
            String questionId = questionMap.get(orderId).id;
            if (userEmaAnswerMap.containsKey(questionId)) {
                userEmaAnswerMap.remove(questionId);
            }

            if (nextQuestion != -1) {
                mPager.setCurrentItem(nextQuestion);
//                nextQuestion = Integer.parseInt(questionMap.get(nextQuestion).nextQuestion);
            } else {
                uploadAnswers();
                finish();
            }
        }

        if (view == buttonNext) {
            RetrievedQuestion question = questionMap.get(mPager.getCurrentItem());

            if (question.isMandatory.equalsIgnoreCase("False")) {
                if (nextQuestion != -1) {
                    mPager.setCurrentItem(nextQuestion);
//                    nextQuestion = Integer.parseInt(questionMap.get(nextQuestion).nextQuestion);
                } else {
                    uploadAnswers();
                    finish();
                }
            } else {
                showSimpleAlert("Alert", "Please select your answer.");
            }
        }
    }

    private void uploadAnswers() {
        FirebaseDatabase database = FirebaseDatabase.getInstance();
        String currentUserId = FirebaseAuth.getInstance().getCurrentUser().getUid();
        refUsersData = database.getReference().child("users_data").child(currentUserId);

        emaIndex = 0;
        final int savedLastEMAID = prefs.getInt("LastEMAID", 0);
        DatabaseReference refQset = refUsersData.child("ema");
        Query lastQuery = refQset.limitToLast(1);
        lastQuery.keepSynced(true);
        lastQuery.addListenerForSingleValueEvent(new ValueEventListener() {
            @Override
            public void onDataChange(DataSnapshot dataSnapshot) {
                for (DataSnapshot ds : dataSnapshot.getChildren()) {
                    emaIndex = Integer.parseInt(ds.getKey());
                    Log.d("tonmoy", "" + emaIndex);
                }
                emaIndex++;
                emaIndex = Math.max(emaIndex, savedLastEMAID + 1);
                UsersAnswer usersAnswer = new UsersAnswer(System.currentTimeMillis() + "", questionSet, userEmaAnswerMap);
                refUsersData.child("ema").child("" + emaIndex).setValue(usersAnswer);
                prefs.edit().putInt("LastEMAID", emaIndex).commit();
                Log.d("tonmoy", "Final ema index" + emaIndex);
                Toast.makeText(QuestionnaireActivity.this, "EMA submitted successfully.", Toast.LENGTH_LONG).show();
            }

            @Override
            public void onCancelled(DatabaseError databaseError) {
                //Handle possible errors.
            }
        });
    }

    @Override
    public void saveAnswer(EMAAnswer emaAnswer) {
        userEmaAnswerMap.put(emaAnswer.questionId, emaAnswer);
        Log.d("tonmoy", String.format("%s", emaAnswer.toString()));
    }

    @Override
    public void setNextQuestion(int nextQuestion) {
        this.nextQuestion = nextQuestion;
    }

    /**
     * A simple pager adapter that represents 5 ScreenSlidePageFragment objects, in
     * sequence.
     */
    private class ScreenSlidePagerAdapter extends FragmentStatePagerAdapter {
        public ScreenSlidePagerAdapter(FragmentManager fm) {
            super(fm);
        }

        @Override
        public Fragment getItem(int position) {
            // default to using submit fragment.
            Fragment fragment = new SubmitFragment();

            // Get relevant question data
            RetrievedQuestion ques = questionMap.get((position));
            QuestionType type = ques.type;

            // Check if last question has been hit
            if (nextQuestion == -1) {
                type = new QuestionType("-1", "Last one...");
            }

            switch (type.id) {
                case "1":
                    MultipleChoiceSingleAnswerQuestionFragment MCSAQues = new
                            MultipleChoiceSingleAnswerQuestionFragment();
                    MCSAQues.setQuestion(ques);
                    return MCSAQues;
                case "2":
                    RangeQuestionFragment rangeFragment = new RangeQuestionFragment();
                    rangeFragment.setQuestion(ques);
                    return rangeFragment;
                case "3":
                    MultipleChoiceMultipleAnswerQuestionFragment mcmaFragment = new
                            MultipleChoiceMultipleAnswerQuestionFragment();
                    mcmaFragment.setQuestion(ques);
                    return mcmaFragment;
                case "4":
                    DescriptiveQuestionFragment descriptiveQuestionFragment = new
                            DescriptiveQuestionFragment();
                    descriptiveQuestionFragment.setQuestion(ques);
                    return descriptiveQuestionFragment;
                case "5":
                    MultipleChoiceSingleAnswerWithTextQuestionFragment mcsawtFragment = new
                            MultipleChoiceSingleAnswerWithTextQuestionFragment();
                    mcsawtFragment.setQuestion(ques);
                    return mcsawtFragment;
                case "6":
                    MultipleChoiceMultipleAnswerWithTextQuestionFragment mcmawtFragment = new
                            MultipleChoiceMultipleAnswerWithTextQuestionFragment();
                    mcmawtFragment.setQuestion(ques);
                    return mcmawtFragment;
                case "7":
                    NumericQuestionFragment nFragment = new NumericQuestionFragment();
                    nFragment.setQuestion(ques);
                    return nFragment;

                default:
                    break;
            }

            return fragment;
        }

        @Override
        public int getCount() {
            return questionMap.size();
        }

    }

    @Override
    protected void onDestroy() {
        super.onDestroy();
    }

    public void showSimpleAlert(String title, String msg) {
        AlertDialog alertDialog = new AlertDialog.Builder(QuestionnaireActivity.this).create();
        alertDialog.setTitle(title);
        alertDialog.setMessage(msg);
        alertDialog.setButton(AlertDialog.BUTTON_NEUTRAL, "OK",
                new DialogInterface.OnClickListener() {
                    public void onClick(DialogInterface dialog, int which) {
                        dialog.dismiss();
                    }
                });
        alertDialog.show();
    }

    public void showExitWarningAlert(String title, String msg) {
        AlertDialog alertDialog = new AlertDialog.Builder(QuestionnaireActivity.this).create();
        alertDialog.setTitle(title);
        alertDialog.setMessage(msg);
        alertDialog.setButton(AlertDialog.BUTTON_POSITIVE, "OK",
                new DialogInterface.OnClickListener() {
                    public void onClick(DialogInterface dialog, int which) {
                        QuestionnaireActivity.this.finish();
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
