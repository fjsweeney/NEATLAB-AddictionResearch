package com.tonmoy.smokingema.model;

/**
 * Created by hossaim3 on 1/23/2018.
 */

public class EMAAnswer {
    public String questionId;
    public String question;
    public String answerId;
    public String answer;

    public EMAAnswer(String questionId, String question, String answerId, String answer) {
        this.questionId = questionId;
        this.question = question;
        this.answer = answer;
        this.answerId = answerId;
    }

    @Override
    public String toString() {
        return "EMAAnswer{" +
                "questionId='" + questionId + '\'' +
                ", question='" + question + '\'' +
                ", answerId='" + answerId + '\'' +
                ", answer='" + answer + '\'' +
                '}';
    }
}
