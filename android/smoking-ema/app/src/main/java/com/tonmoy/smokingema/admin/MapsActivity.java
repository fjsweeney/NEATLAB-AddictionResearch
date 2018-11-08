package com.tonmoy.smokingema.admin;

import android.graphics.Color;
import android.support.v4.app.FragmentActivity;
import android.os.Bundle;
import android.util.Log;
import android.view.View;
import android.widget.Button;
import android.widget.EditText;

import com.google.android.gms.maps.CameraUpdate;
import com.google.android.gms.maps.CameraUpdateFactory;
import com.google.android.gms.maps.GoogleMap;
import com.google.android.gms.maps.OnMapReadyCallback;
import com.google.android.gms.maps.SupportMapFragment;
import com.google.android.gms.maps.model.LatLng;
import com.google.android.gms.maps.model.LatLngBounds;
import com.google.android.gms.maps.model.MarkerOptions;
import com.google.android.gms.maps.model.PolylineOptions;
import com.google.firebase.auth.FirebaseAuth;
import com.google.firebase.database.DataSnapshot;
import com.google.firebase.database.DatabaseError;
import com.google.firebase.database.DatabaseReference;
import com.google.firebase.database.FirebaseDatabase;
import com.google.firebase.database.Query;
import com.google.firebase.database.ValueEventListener;
import com.tonmoy.smokingema.R;
import com.tonmoy.smokingema.model.UsersLocation;

import java.text.ParseException;
import java.text.SimpleDateFormat;
import java.util.ArrayList;
import java.util.Calendar;
import java.util.Date;
import java.util.List;

public class MapsActivity extends FragmentActivity implements OnMapReadyCallback, View.OnClickListener {

    private GoogleMap mMap;
    Button buttonUpdate;
    EditText edittextLimit, edittextStartDate;
    int colorList[] = {Color.BLACK, Color.BLUE, Color.GREEN, Color.CYAN, Color.GRAY};

    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        setContentView(R.layout.activity_maps);
        edittextLimit = (EditText) findViewById(R.id.edittextLimit);
        edittextStartDate = (EditText) findViewById(R.id.edittextStartDate);
        buttonUpdate = (Button) findViewById(R.id.buttonUpdate);
        buttonUpdate.setOnClickListener(this);
        // Obtain the SupportMapFragment and get notified when the map is ready to be used.
        SupportMapFragment mapFragment = (SupportMapFragment) getSupportFragmentManager()
                .findFragmentById(R.id.map);
        mapFragment.getMapAsync(this);

        String dateFormat = "MM/dd/yyyy HH:mm";
        long timeInMilliseconds = System.currentTimeMillis();
        Log.d("tonmoy", getDate(timeInMilliseconds, dateFormat));
        edittextStartDate.setText(getDate(timeInMilliseconds, dateFormat));
    }


    /**
     * Manipulates the map once available.
     * This callback is triggered when the map is ready to be used.
     * This is where we can add markers or lines, add listeners or move the camera. In this case,
     * we just add a marker near Sydney, Australia.
     * If Google Play services is not installed on the device, the user will be prompted to install
     * it inside the SupportMapFragment. This method will only be triggered once the user has
     * installed Google Play services and returned to the app.
     */
    @Override
    public void onMapReady(GoogleMap googleMap) {
        mMap = googleMap;

        // Add a marker in Sydney and move the camera
        LatLng sydney = new LatLng(-34, 151);
        mMap.addMarker(new MarkerOptions().position(sydney).title("Marker in Sydney"));
        mMap.moveCamera(CameraUpdateFactory.newLatLng(sydney));
        long timeInMilliseconds = System.currentTimeMillis();
        timeInMilliseconds -= 1000 * 60 * 60 * 5; //last 5 hours previous data
        getLocationInfo(timeInMilliseconds, 50);
//        mMap.addPolyline(new PolylineOptions()
//                .color(Color.BLUE)
//                .width(5)
//                .add(MELBOURNE, ADELAIDE, PERTH, DARWIN));
    }

    private void getLocationInfo(long date, int limit) {
        Log.d("tonmoy", "uploadLocationInfo get called");
        FirebaseDatabase database = FirebaseDatabase.getInstance();
        String currentUserId = FirebaseAuth.getInstance().getCurrentUser().getUid();
        DatabaseReference refUsersLocation = database.getReference().child("users_data").child(currentUserId).child("location");
//
//        for (Location location : locations) {
//            UsersLocation usersLocation = new UsersLocation();
//            usersLocation.accuracy = location.hasAccuracy() ? location.getAccuracy() + "" : "n/a";
//            usersLocation.altitude = location.hasAltitude() ? location.getAltitude() + "" : "n/a";
//            usersLocation.latitude = location.getLatitude() + "";
//            usersLocation.longitude = location.getLongitude() + "";
//            usersLocation.speed = location.hasSpeed() ? location.getSpeed() + "" : "n/a";
//            usersLocation.provider = location.getProvider();
//            usersLocation.timeUTC = location.getTime() + "";
//            refUsersLocation.child(usersLocation.timeUTC).setValue(usersLocation);
//        }


        Query lastQuery = refUsersLocation.orderByKey().limitToLast(limit);
        lastQuery.addListenerForSingleValueEvent(new ValueEventListener() {
            @Override
            public void onDataChange(DataSnapshot dataSnapshot) {
                List<LatLng> latLngs = new ArrayList<LatLng>();
                LatLng lastLoc = null;
                mMap.clear();
                LatLngBounds.Builder bounds = new LatLngBounds.Builder();

                for (DataSnapshot ds : dataSnapshot.getChildren()) {
                    UsersLocation loc = ds.getValue(UsersLocation.class);
                    Log.d("tonmoy", loc.time);
                    LatLng lt = new LatLng(Double.parseDouble(loc.latitude), Double.parseDouble(loc.longitude));
                    latLngs.add(lt);
                    bounds.include(lt);
                    lastLoc = new LatLng(Double.parseDouble(loc.latitude), Double.parseDouble(loc.longitude));
                }
                int colorSelector = 0;
                for (int i = 0; i < latLngs.size(); ) {
                    int j = 0;
                    int color = colorList[colorSelector % 5];
                    colorSelector++;
                    PolylineOptions polylineOptions = new PolylineOptions()
                            .color(color)
                            .width(8);
                    for (; j < 20; j++) {
                        if (i + j >= latLngs.size()) {
                            break;
                        }
                        polylineOptions.add(latLngs.get(i + j));
                    }
                    mMap.addPolyline(polylineOptions);
                    //j--;
                    i += j;
                }
                CameraUpdate cu = CameraUpdateFactory.newLatLngBounds(bounds.build(), 2);
                mMap.animateCamera(cu);
                // mMap.moveCamera(CameraUpdateFactory.newLatLngZoom(lastLoc, 18));
            }

            @Override
            public void onCancelled(DatabaseError databaseError) {
                //Handle possible errors.
            }
        });
    }

    @Override
    public void onClick(View view) {
        if (view == buttonUpdate) {
            String datetime = edittextStartDate.getText().toString();
//            String arr[]=datetime.split(" ");
//            String date = arr[0];
//            String time = arr[1];
//            String dateArr[]=date.split("/");
//            String timeArr[] = time.split(":");
            String sdf = "MM/dd/yyyy HH:mm";
            long timeInMilliseconds = getMilliSecondsFromDate(datetime, sdf);
            String dateFormat = "EEE MMM dd HH:mm:ss z yyyy";
            Log.d("tonmoy", getDate(timeInMilliseconds, dateFormat));
            getLocationInfo(timeInMilliseconds, Integer.parseInt(edittextLimit.getText().toString()));
        }
    }

    public static String getDate(long milliSeconds, String dateFormat) {
        // Create a DateFormatter object for displaying date in specified format.
        SimpleDateFormat formatter = new SimpleDateFormat(dateFormat);

        // Create a calendar object that will convert the date and time value in milliseconds to date.
        Calendar calendar = Calendar.getInstance();
        calendar.setTimeInMillis(milliSeconds);
        return formatter.format(calendar.getTime());
    }

    public static long getMilliSecondsFromDate(String dateTime, String dateFormat) {
        SimpleDateFormat sdf = new SimpleDateFormat(dateFormat);
        long timeInMilliseconds = System.currentTimeMillis();
        try {
            Date mDate = sdf.parse(dateTime);
            timeInMilliseconds = mDate.getTime();
            System.out.println("Date in milli :: " + timeInMilliseconds);
        } catch (ParseException e) {
            e.printStackTrace();
        }
        return timeInMilliseconds;
    }

}
