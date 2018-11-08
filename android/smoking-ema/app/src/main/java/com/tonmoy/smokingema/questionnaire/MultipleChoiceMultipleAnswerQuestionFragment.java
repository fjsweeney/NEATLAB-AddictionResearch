package com.tonmoy.smokingema.questionnaire;

import android.content.Context;
import android.os.Bundle;
import android.support.v4.app.Fragment;
import android.util.Log;
import android.view.LayoutInflater;
import android.view.View;
import android.view.ViewGroup;
import android.widget.CheckBox;
import android.widget.LinearLayout;
import android.widget.TextView;

import com.tonmoy.smokingema.R;
import com.tonmoy.smokingema.interfaces.QuestionnaireListener;
import com.tonmoy.smokingema.model.Answer;
import com.tonmoy.smokingema.model.EMAAnswer;
import com.tonmoy.smokingema.model.RetrievedQuestion;

import java.util.ArrayList;

public class MultipleChoiceMultipleAnswerQuestionFragment extends Fragment {

    // NOTE: Specifies whether view is currently visible. Used for setting nextQuestion.
    private boolean isViewShown = false;

    private View view;
    private LinearLayout checkboxLayout;
    private ArrayList<String> runningAnswer;
    private RetrievedQuestion question;
    QuestionnaireListener questionnaireListener;

    public RetrievedQuestion getQuestion() {
        return question;
    }

    public void setQuestion(RetrievedQuestion question) {
        this.question = question;
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

        view = inflater.inflate(R.layout.fragment_multiple_choice_multiple_answer, container, false);
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

                    // Retrieve answer text
                    Answer ans = question.answers.get(id - 1000);
                    String answerText = ans.text;


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
