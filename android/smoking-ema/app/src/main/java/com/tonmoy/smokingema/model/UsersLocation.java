package com.tonmoy.smokingema.model;

/**
 * Created by hossaim3 on 1/23/2018.
 */

public class UsersLocation {
    public double timeUTC;
    public String latitude;
    public String longitude;
    public String accuracy;
    public String altitude;
    public String speed;
    public String provider;
    public String time;

    public UsersLocation() {

    }

    public UsersLocation(double timeUTC, String time, String latitude, String longitude, String accuracy, String altitude, String speed, String provider) {
        this.timeUTC = timeUTC;
        this.time = time;
        this.latitude = latitude;
        this.longitude = longitude;
        this.accuracy = accuracy;
        this.altitude = altitude;
        this.speed = speed;
        this.provider = provider;
    }
}
