package com.tonmoy.smokingema.model;

/**
 * Created by hossaim3 on 1/12/2018.
 */

public class Answer {
    public String id;
    public String text;
    public String nextQuestion;

    public Answer(String id, String text, String nextQuestion) {
        this.id = id;
        this.text = text;
        this.nextQuestion = nextQuestion;
    }
    public Answer()
    {

    }
}
