package com.tonmoy.smokingema.model;

import java.util.ArrayList;

/**
 * Created by hossaim3 on 1/12/2018.
 */

public class RetrievedQuestion {
    public String id;
    public String nextQuestion;
    public String orderId;
    public String text;
    public String isMandatory ="False";
    public ArrayList<Answer> answers = new ArrayList<Answer>();
    public QuestionType type;

    public RetrievedQuestion() {
    }

    public RetrievedQuestion(String id, String text, String typeId, String type, ArrayList<Answer> map) {
        this.id = id;
        this.text = text;
        this.answers = map;
        this.type = new QuestionType(typeId, type);
    }
}
