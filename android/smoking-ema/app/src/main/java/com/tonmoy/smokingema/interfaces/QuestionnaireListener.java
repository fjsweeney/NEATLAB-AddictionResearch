package com.tonmoy.smokingema.interfaces;

import com.tonmoy.smokingema.model.EMAAnswer;
import com.tonmoy.smokingema.model.Question;

/**
 * Created by hossaim3 on 1/17/2018.
 */

public interface QuestionnaireListener {
    void saveAnswer(EMAAnswer emaAnswer);
    void setNextQuestion(int nextQuestion);
}
