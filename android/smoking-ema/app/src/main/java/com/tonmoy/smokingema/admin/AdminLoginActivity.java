package com.tonmoy.smokingema.admin;

import android.content.Intent;
import android.support.v7.app.AppCompatActivity;
import android.os.Bundle;
import android.view.View;
import android.widget.Button;
import android.widget.EditText;

import com.tonmoy.smokingema.R;

public class AdminLoginActivity extends AppCompatActivity implements View.OnClickListener {
    Button buttonAdminLogin;
    EditText editTextPassword;

    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        setContentView(R.layout.activity_admin_login);

        buttonAdminLogin = (Button) findViewById(R.id.buttonAdminLogin);
        editTextPassword= (EditText) findViewById(R.id.editTextPassword);
        buttonAdminLogin.setOnClickListener(this);
    }

    @Override
    public void onClick(View view) {
        if (view == buttonAdminLogin && editTextPassword.getText().toString().equals("1234562018")) {
            startActivity(new Intent(AdminLoginActivity.this, AdminActivity.class));
            this.finish();
        }
    }
}
