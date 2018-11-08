package com.tonmoy.smokingema.model;

import java.util.HashMap;
import java.util.Map;

/**
 * Created by hossaim3 on 1/12/2018.
 */

public class Question {
    public String id;
    public String text;
    public Map<String, Answer> answers = new HashMap<String, Answer>();
    public QuestionType type;

    public Question(String id, String text, String typeId, String type, Map<String, Answer> map) {
        this.id = id;
        this.text = text;
        this.answers = map;
        this.type = new QuestionType(typeId, type);
    }

   public class QuestionType {
        public String id;
        public String text;

        public QuestionType() {

        }

        public QuestionType(String id, String text) {
            this.id = id;
            this.text = text;
        }
    }
}
