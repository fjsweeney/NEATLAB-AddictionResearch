package com.tonmoy.smokingema.questionnaire;


import android.content.Context;
import android.os.Bundle;
import android.support.v4.app.Fragment;
import android.util.Log;
import android.view.LayoutInflater;
import android.view.View;
import android.view.ViewGroup;
import android.widget.RadioButton;
import android.widget.RadioGroup;
import android.widget.TextView;

import com.tonmoy.smokingema.R;
import com.tonmoy.smokingema.interfaces.QuestionnaireListener;
import com.tonmoy.smokingema.model.Answer;
import com.tonmoy.smokingema.model.EMAAnswer;
import com.tonmoy.smokingema.model.RetrievedQuestion;


public class MultipleChoiceSingleAnswerQuestionFragment extends Fragment implements RadioGroup.OnCheckedChangeListener {

    // NOTE: Specifies whether view is currently visible. Used for setting nextQuestion.
    private boolean isViewShown = false;

    private View view;
    private RadioGroup options;
    private String answer;
    QuestionnaireListener questionnaireListener;
    private RetrievedQuestion question;
    RadioGroup rgp;

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
        view = inflater.inflate(R.layout.fragment_multiple_choice_single_answer, container, false);
        TextView textViewQuestion = (TextView) view.findViewById(R.id.textviewQuestion);
        textViewQuestion.setText(question.text);

        TextView textviewQuestionMandatory = (TextView) view.findViewById(R.id.textviewQuestionMandatory);
        if (question.isMandatory.equalsIgnoreCase("True")) {
            textviewQuestionMandatory.setVisibility(View.VISIBLE);
        }

        // Set next question
        if (isViewShown) {
            questionnaireListener.setNextQuestion(Integer.parseInt(question.nextQuestion));
        }

        // Setup radio group
        rgp = (RadioGroup) view.findViewById(R.id.radioGroupAnswers);
        for (int i = 1; i < question.answers.size(); i++) {
            Answer ans = question.answers.get(i);
            RadioButton rbn = new RadioButton(getActivity());
            rbn.setId(i + 1000);
            rbn.setText(ans.text);
            rgp.addView(rbn);
        }
        rgp.setOnCheckedChangeListener(this);
        return view;
    }

    private void getChoice(int id) {
        RadioButton selected = (RadioButton) view.findViewById(id);
        answer = (String) selected.getText();
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

    @Override
    public void onCheckedChanged(RadioGroup radioGroup, int id) {
        RadioButton checkedRadioButton = (RadioButton) radioGroup.findViewById(id);
        boolean isChecked = checkedRadioButton.isChecked();
        Log.d("tonmoy", "ID : " + id);
        ((QuestionnaireActivity) getActivity()).buttonNext.setEnabled(true);
        if (isChecked) {
            Answer ans = question.answers.get(id - 1000);
            int nextQuestion = Integer.parseInt(ans.nextQuestion);
            EMAAnswer emaAnswer = new EMAAnswer(question.id, question.text, ans.id, ans.text);
            questionnaireListener.setNextQuestion(nextQuestion);
            questionnaireListener.saveAnswer(emaAnswer);
        }
    }
}
