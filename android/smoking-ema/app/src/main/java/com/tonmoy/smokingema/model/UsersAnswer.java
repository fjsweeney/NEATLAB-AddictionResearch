package com.tonmoy.smokingema.model;

import java.util.HashMap;

/**
 * Created by hossaim3 on 1/23/2018.
 */

public class UsersAnswer {
    public String timeUTC;
    public String questionSet;
    public HashMap<String, EMAAnswer> usersAllEMAAnswers ;

    public UsersAnswer() {

    }

    public UsersAnswer(String timeUTC, String questionSet, HashMap<String, EMAAnswer> usersAllEMAAnswers ) {
        this.timeUTC = timeUTC;
        this.questionSet = questionSet;
        this.usersAllEMAAnswers = usersAllEMAAnswers;
    }
}
