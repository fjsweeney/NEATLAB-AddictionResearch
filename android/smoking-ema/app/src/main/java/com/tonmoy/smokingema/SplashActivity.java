package com.tonmoy.smokingema;

import android.content.Intent;
import android.os.Bundle;
import android.support.v7.app.AppCompatActivity;
import android.view.View;
import android.widget.Button;
import android.widget.Toast;

import com.firebase.ui.auth.AuthUI;
import com.firebase.ui.auth.ErrorCodes;
import com.firebase.ui.auth.IdpResponse;
import com.google.firebase.auth.FirebaseAuth;
import com.google.firebase.auth.FirebaseUser;

import java.util.Arrays;
import java.util.List;

public class SplashActivity extends AppCompatActivity implements View.OnClickListener {
    private FirebaseAuth mAuth;
    private static final int RC_SIGN_IN = 123;
    Button buttonUserLogin;

    // Choose authentication providers
    List<AuthUI.IdpConfig> providers = Arrays.asList(
            new AuthUI.IdpConfig.Builder(AuthUI.EMAIL_PROVIDER).build()
            // new AuthUI.IdpConfig.Builder(AuthUI.PHONE_VERIFICATION_PROVIDER).build(),
            // new AuthUI.IdpConfig.Builder(AuthUI.GOOGLE_PROVIDER).build(),
            //  new AuthUI.IdpConfig.Builder(AuthUI.FACEBOOK_PROVIDER).build(),
            // new AuthUI.IdpConfig.Builder(AuthUI.TWITTER_PROVIDER).build()
    );

    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        setContentView(R.layout.activity_splash);
        buttonUserLogin = (Button) findViewById(R.id.buttonLogin);
        buttonUserLogin.setOnClickListener(this);
        mAuth = FirebaseAuth.getInstance();
        FirebaseAuth auth = FirebaseAuth.getInstance();
        if (auth.getCurrentUser() != null) {
           startActivity(new Intent(SplashActivity.this, HomeActivity.class));
           // startActivity(new Intent(SplashActivity.this, AddQuestionActivity.class));
            finish();
        } else {
            startActivityForResult(
                    AuthUI.getInstance()
                            .createSignInIntentBuilder()
                            .setAvailableProviders(providers)
                            .build(),
                    RC_SIGN_IN);
        }

    }

    @Override
    public void onStart() {
        super.onStart();
        // Check if user is signed in (non-null) and update UI accordingly.
        FirebaseUser currentUser = mAuth.getCurrentUser();
        updateUI(currentUser);
    }

    private void updateUI(FirebaseUser currentUser) {

    }

    @Override
    protected void onActivityResult(int requestCode, int resultCode, Intent data) {
        super.onActivityResult(requestCode, resultCode, data);

        if (requestCode == RC_SIGN_IN) {
            IdpResponse response = IdpResponse.fromResultIntent(data);

            if (resultCode == RESULT_OK) {
                // Successfully signed in
                FirebaseUser user = FirebaseAuth.getInstance().getCurrentUser();
                startActivity(new Intent(SplashActivity.this, HomeActivity.class));
                finish();
            } else {
                // Sign in failed
                if (response == null) {
                    // User pressed back button
                    Toast.makeText(this, "Sign in cancelled", Toast.LENGTH_LONG);
                    return;
                }
                if (response.getErrorCode() == ErrorCodes.NO_NETWORK) {
                    Toast.makeText(this, "no internet connection", Toast.LENGTH_LONG);
                    return;
                }

                if (response.getErrorCode() == ErrorCodes.UNKNOWN_ERROR) {
                    Toast.makeText(this, "unknown error", Toast.LENGTH_LONG);
                    return;
                }

            }
        }
    }

    @Override
    public void onClick(View view) {
        if (view == buttonUserLogin) {
            startActivityForResult(
                    AuthUI.getInstance()
                            .createSignInIntentBuilder()
                            .setAvailableProviders(providers)
                            .build(),
                    RC_SIGN_IN);
        }
    }
}
