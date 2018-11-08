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
import android.widget.EditText;
import android.widget.TextView;

import com.tonmoy.smokingema.R;
import com.tonmoy.smokingema.interfaces.QuestionnaireListener;
import com.tonmoy.smokingema.model.EMAAnswer;
import com.tonmoy.smokingema.model.RetrievedQuestion;

public class NumericQuestionFragment extends Fragment {

    // NOTE: Specifies whether view is currently visible. Used for setting nextQuestion.
    private boolean isViewShown = false;

    private View view;
    private RetrievedQuestion question;
    QuestionnaireListener questionnaireListener;
    EditText editNumericText;

    @Override
    public void onResume() {
        super.onResume();
        editNumericText.addTextChangedListener(new TextWatcher() {
            @Override
            public void beforeTextChanged(CharSequence charSequence, int i, int i1, int i2) {

            }

            @Override
            public void onTextChanged(CharSequence charSequence, int i, int i1, int i2) {

            }

            @Override
            public void afterTextChanged(Editable editable) {
                if (getView() != null) {
                    updateNumericAnswer();
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
        view = inflater.inflate(R.layout.fragment_numeric_question, container, false);
        TextView textViewQuestion = (TextView) view.findViewById(R.id.textviewQuestion);
        textViewQuestion.setText(question.text);
        editNumericText = (EditText) view.findViewById(R.id.editNumericText);

        // Set next question
        if (isViewShown) {
            questionnaireListener.setNextQuestion(Integer.parseInt(question.nextQuestion));
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

    public RetrievedQuestion getQuestion() {
        return question;
    }

    public void setQuestion(RetrievedQuestion question) {
        this.question = question;
    }

    private void updateNumericAnswer() {
        EMAAnswer emaAnswer = new EMAAnswer(question.id, question.text, "numeric",
                editNumericText.getText().toString());

        // NOTE: Hard-coding this for now...
        int response = 0;
        try {
            response = Integer.parseInt(editNumericText.getText().toString());
        } catch (NumberFormatException ex) {
            Log.d("tonmoy", "NumberFormatException in NumericQuestionFragment.");
        }
        int nextQuestion = (response > 0) ? 19 : Integer.parseInt(question.nextQuestion);
        questionnaireListener.saveAnswer(emaAnswer);
        questionnaireListener.setNextQuestion(nextQuestion);
    }
}
