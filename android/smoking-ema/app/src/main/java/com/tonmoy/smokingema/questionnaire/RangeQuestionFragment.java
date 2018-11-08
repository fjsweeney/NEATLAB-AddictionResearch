package com.tonmoy.smokingema.questionnaire;

import android.content.Context;
import android.os.Bundle;
import android.support.v4.app.Fragment;
import android.view.LayoutInflater;
import android.view.View;
import android.view.ViewGroup;
import android.widget.SeekBar;
import android.widget.TextView;

import com.tonmoy.smokingema.R;
import com.tonmoy.smokingema.interfaces.QuestionnaireListener;
import com.tonmoy.smokingema.model.EMAAnswer;
import com.tonmoy.smokingema.model.RetrievedQuestion;

public class RangeQuestionFragment extends Fragment {

    // NOTE: Specifies whether view is currently visible. Used for setting nextQuestion.
    private boolean isViewShown = false;

    private View view;
    private RetrievedQuestion question;
    QuestionnaireListener questionnaireListener;
    SeekBar seekBar;

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
        // Inflate the layout for this fragment
        view = inflater.inflate(R.layout.fragment_range_question, container, false);
        TextView textViewQuestion = (TextView) view.findViewById(R.id.textviewQuestion);
        textViewQuestion.setText(question.text);

        // Set next question
        if (isViewShown) {
            questionnaireListener.setNextQuestion(Integer.parseInt(question.nextQuestion));
        }

        seekBar = (SeekBar)view.findViewById(R.id.likertSeekBar);
        seekBar.setOnSeekBarChangeListener(new SeekBar.OnSeekBarChangeListener() {
            @Override
            public void onProgressChanged(SeekBar seekBar, int progress, boolean initiatedByUser) {
                if(initiatedByUser)
                {
                    EMAAnswer emaAnswer = new EMAAnswer(question.id, question.text, "range1", progress+"");
                    int nextQuestion = Integer.parseInt(question.nextQuestion);
                    questionnaireListener.saveAnswer(emaAnswer);
                    questionnaireListener.setNextQuestion(nextQuestion);
                }

            }

            @Override
            public void onStartTrackingTouch(SeekBar seekBar) {

            }

            @Override
            public void onStopTrackingTouch(SeekBar seekBar) {

            }
        });

        // Save the default response so the user isn't forced to touch the seek bar.
        EMAAnswer emaAnswer = new EMAAnswer(question.id, question.text, "range1", "2");
        questionnaireListener.saveAnswer(emaAnswer);

        return view;
    }

    @Override
    public void onAttach(Context context) {
        super.onAttach(context);
        // This makes sure that the container activity has implemented
        // the callback interface. If not, it throws an exception
        ((QuestionnaireActivity) context).buttonNext.setEnabled(true);
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
}
