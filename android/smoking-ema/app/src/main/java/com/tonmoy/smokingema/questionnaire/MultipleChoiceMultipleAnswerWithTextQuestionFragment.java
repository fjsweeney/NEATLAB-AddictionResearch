package com.tonmoy.smokingema.questionnaire;

import android.content.Context;
import android.os.Bundle;
import android.support.v4.app.Fragment;
import android.text.Editable;
import android.text.TextWatcher;
import android.util.Log;
import android.view.LayoutInflater;
import android.view.View;
import android.view.ViewGroup;
import android.widget.CheckBox;
import android.widget.EditText;
import android.widget.LinearLayout;
import android.widget.TextView;

import com.tonmoy.smokingema.R;
import com.tonmoy.smokingema.interfaces.QuestionnaireListener;
import com.tonmoy.smokingema.model.Answer;
import com.tonmoy.smokingema.model.EMAAnswer;
import com.tonmoy.smokingema.model.RetrievedQuestion;

import java.util.ArrayList;

public class MultipleChoiceMultipleAnswerWithTextQuestionFragment extends Fragment {

    // NOTE: Specifies whether view is currently visible. Used for setting nextQuestion.
    private boolean isViewShown = false;

    private View view;
    private RetrievedQuestion question;
    private LinearLayout checkboxLayout;
    private EditText editTextOther;
    private ArrayList<String> runningAnswer;
    QuestionnaireListener questionnaireListener;

    public RetrievedQuestion getQuestion() {
        return question;
    }

    public void setQuestion(RetrievedQuestion question) {
        this.question = question;
    }

    @Override
    public void onResume() {
        super.onResume();
        editTextOther.addTextChangedListener(new TextWatcher() {
            @Override
            public void beforeTextChanged(CharSequence charSequence, int i, int i1, int i2) {

            }

            @Override
            public void onTextChanged(CharSequence charSequence, int i, int i1, int i2) {

            }

            @Override
            public void afterTextChanged(Editable editable) {
                // NOTE: Some edit texts are being triggered when not in view. This is a temporary fix.
                if (getView() != null) {
                    updateOtherAnswer();
                }
            }
        });
    }

    @Override
    public void setUserVisibleHint(boolean isVisibleToUser) {
        super.setUserVisibleHint(isVisibleToUser);
        if (getView() != null) {
            isViewShown = true;
            questionnaireListener.setNextQuestion(Integer.parseInt(question.nextQuestion));
        } else {
            isViewShown = false;
        }
    }

    @Override
    public View onCreateView(LayoutInflater inflater, ViewGroup container,
                             Bundle savedInstanceState) {
        // Initialize temporary data structures
        runningAnswer = new ArrayList<>();

        // Set up views
        view = inflater.inflate(R.layout.fragment_multiple_choice_multiple_answer_with_text,
                container, false);
        TextView textViewQuestion = (TextView) view.findViewById(R.id.textviewQuestion);
        textViewQuestion.setText(question.text);
        editTextOther = (EditText) view.findViewById(R.id.editTextOther);

        TextView textviewQuestionMandatory = (TextView) view.findViewById(R.id.textviewQuestionMandatory);
        if (question.isMandatory.equalsIgnoreCase("True")) {
            textviewQuestionMandatory.setVisibility(View.VISIBLE);
        }

        // Set next question
        if (isViewShown) {
            questionnaireListener.setNextQuestion(Integer.parseInt(question.nextQuestion));
        }

        // Setup checkboxes
        checkboxLayout = (LinearLayout) view.findViewById(R.id.checkboxLayout);
        for (int i = 1; i < question.answers.size(); i++) {
            Answer ans = question.answers.get(i);
            CheckBox checkbox = new CheckBox(getActivity());
            checkbox.setId(i + 1000);
            checkbox.setText(ans.text);
            checkbox.setOnClickListener(new View.OnClickListener() {
                @Override
                public void onClick(View view) {
                    int id = view.getId();

                    // Check it this is the user supplied field (i.e. "Other")
                    Answer ans = question.answers.get(id - 1000);
                    String answerText = (ans.text.equalsIgnoreCase("other"))
                            ? ans.text + " - " + editTextOther.getText().toString() : ans.text;

                    // Add or remove answers
                    CheckBox checkbox = (CheckBox) checkboxLayout.findViewById(id);
                    if (checkbox.isChecked()) {
                        runningAnswer.add(answerText);
                    } else {
                        runningAnswer.remove(answerText);
                    }

                    String answer_csv = (runningAnswer.isEmpty()) ? "" : toCsv(runningAnswer);
                    EMAAnswer emaAnswer = new EMAAnswer(question.id, question.text, "-1", answer_csv);
                    int nextQuestion = Integer.parseInt(ans.nextQuestion);
                    questionnaireListener.setNextQuestion(nextQuestion);
                    questionnaireListener.saveAnswer(emaAnswer);

                    Log.d("tonmoy", "Answer : " + answerText);
                }
            });
            checkboxLayout.addView(checkbox);
        }
        return view;
    }

    @Override
    public void onAttach(Context context) {
        super.onAttach(context);
        // This makes sure that the container activity has implemented
        // the callback interface. If not, it throws an exception
        try {
            questionnaireListener = (QuestionnaireListener) context;
        } catch (ClassCastException e) {
            throw new ClassCastException(context.toString()
                    + " must implement OnHeadlineSelectedListener");
        }
    }

    private void updateOtherAnswer() {
        // Remove any "Other" answer that may may previously existed.
        for (String answer : runningAnswer) {
            if (answer.toLowerCase().contains("other")) {
                runningAnswer.remove(answer);
                break;
            }
        }

        // NOTE: tw - Should always be the last element of the Answer list. I'm assuming the
        // question set is probably organized to have the "other" option be the last choice.
        int lastIdx = 1000 + question.answers.size() - 1;

        CheckBox checkbox = (CheckBox) checkboxLayout.findViewById(lastIdx);

        // Force checkbox on if user begins typing in content
        if (!checkbox.isChecked()) {
            checkbox.setChecked(true);
        }

        // Save text to runningAnswer list
        Answer ans = question.answers.get(lastIdx - 1000);
        String answerText = ans.text + " - " + editTextOther.getText().toString();
        runningAnswer.add(answerText);

        // Save answer
        EMAAnswer emaAnswer = new EMAAnswer(question.id, question.text, "-1",
                toCsv(runningAnswer));
        int nextQuestion = Integer.parseInt(ans.nextQuestion);

        questionnaireListener.setNextQuestion(nextQuestion);
        questionnaireListener.saveAnswer(emaAnswer);
    }

    private String toCsv(ArrayList<String> runningAnswer) {
        StringBuilder sb = new StringBuilder();
        for (String answer : runningAnswer.subList(0, runningAnswer.size()-1)) {
            sb.append(answer);
            sb.append(",");
        }
        sb.append(runningAnswer.get(runningAnswer.size() - 1));

        return sb.toString();
    }
}
