package com.tonmoy.smokingema.questionnaire;

import android.app.Application;

import com.google.firebase.database.FirebaseDatabase;

/**
 * Created by hossaim3 on 1/23/2018.
 */

public class MyApplication extends Application {

    @Override
    public void onCreate() {
        super.onCreate();
        FirebaseDatabase.getInstance().setPersistenceEnabled(true);
    }
}