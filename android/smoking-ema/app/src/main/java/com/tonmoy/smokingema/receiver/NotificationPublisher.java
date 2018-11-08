package com.tonmoy.smokingema.receiver;

import android.app.Notification;
import android.app.NotificationManager;
import android.content.BroadcastReceiver;
import android.content.Context;
import android.content.Intent;
import android.util.Log;

import com.tonmoy.smokingema.EMAAlertDialogActivity;

/**
 * Created by hossaim3 on 1/30/2018.
 */

public class NotificationPublisher extends BroadcastReceiver {

    public static String NOTIFICATION_ID = "notification_id";
    public static String NOTIFICATION = "notification";

    @Override
    public void onReceive(final Context context, Intent intent) {

        NotificationManager notificationManager = (NotificationManager) context.getSystemService(Context.NOTIFICATION_SERVICE);
        Log.d("tonmoy", "NotificationPublisher: " + intent.getStringExtra("question_set"));
        Log.d("tonmoy", "NotificationPublisher: " + intent.getIntExtra(NOTIFICATION_ID, 0));
        Notification notification = intent.getParcelableExtra(NOTIFICATION);
        int notificationId = intent.getIntExtra(NOTIFICATION_ID, 0);
        notificationManager.notify(notificationId, notification);

        showAlertDialog(context, intent.getStringExtra("question_set"));
    }

    private void showAlertDialog(final Context context, String questionSet) {
        Intent i = new Intent(context, EMAAlertDialogActivity.class);
        i.putExtra("question_set", questionSet);
        i.addFlags(Intent.FLAG_ACTIVITY_NEW_TASK);
        context.startActivity(i);
    }
}