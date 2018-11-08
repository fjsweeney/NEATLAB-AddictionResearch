package com.tonmoy.smokingema.questionnaire;


import android.content.Context;
import android.os.Bundle;
import android.support.v4.app.Fragment;
import android.text.Editable;
import android.text.TextWatcher;
import android.view.LayoutInflater;
import android.view.View;
import android.view.ViewGroup;
import android.widget.EditText;
import android.widget.TextView;

import com.tonmoy.smokingema.R;
import com.tonmoy.smokingema.interfaces.QuestionnaireListener;
import com.tonmoy.smokingema.model.EMAAnswer;
import com.tonmoy.smokingema.model.RetrievedQuestion;

public class DescriptiveQuestionFragment extends Fragment {

    // NOTE: Specifies whether view is currently visible. Used for setting nextQuestion.
    private boolean isViewShown = false;

    private View view;
    private RetrievedQuestion question;
    QuestionnaireListener questionnaireListener;
    EditText editTextDescription;

    @Override
    public void onResume() {
        super.onResume();
        editTextDescription.addTextChangedListener(new TextWatcher() {
            @Override
            public void beforeTextChanged(CharSequence charSequence, int i, int i1, int i2) {

            }

            @Override
            public void onTextChanged(CharSequence charSequence, int i, int i1, int i2) {

            }

            @Override
            public void afterTextChanged(Editable editable) {
                if (getView() != null) {
                    updateTextAnswer();
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
        view = inflater.inflate(R.layout.fragment_descriptive_question, container, false);
        TextView textViewQuestion = (TextView) view.findViewById(R.id.textviewQuestion);
        textViewQuestion.setText(question.text);
        editTextDescription = (EditText) view.findViewById(R.id.editTextDescription);

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

    private void updateTextAnswer() {
        // Do not save answer on empty response.
        if (editTextDescription.getText().toString().isEmpty()) {
            return;
        }

        EMAAnswer emaAnswer = new EMAAnswer(question.id, question.text, "descriptive",
                editTextDescription.getText().toString());
        int nextQuestion = Integer.parseInt(question.nextQuestion);

        questionnaireListener.setNextQuestion(nextQuestion);
        questionnaireListener.saveAnswer(emaAnswer);
    }
}
