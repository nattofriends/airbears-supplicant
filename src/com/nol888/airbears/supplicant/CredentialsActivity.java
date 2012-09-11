package com.nol888.airbears.supplicant;

import android.app.Activity;
import android.os.Bundle;
import android.view.View;
import android.view.View.OnClickListener;
import android.widget.Button;
import android.widget.EditText;
import android.widget.Toast;

import com.nol888.airbears.supplicant.security.CredentialStorage;

public class CredentialsActivity extends Activity {

    @Override
    public void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
		setContentView(R.layout.activity_credentials);
		
		overridePendingTransition(R.anim.slide_in_up, R.anim.hold);
		
		CredentialStorage cs = CredentialStorage.getInstance(this);
		if (cs.hasCalnetCredentials()) {
			EditText txtUsername = (EditText) findViewById(R.id.txtUsername);
			txtUsername.setText(cs.getCalnetId());
		}

		Button btnSave = (Button) findViewById(R.id.btnSave);
		btnSave.setOnClickListener(new OnClickListener() {
			@Override
			public void onClick(View v) {
				// save/update calnet account
				CredentialStorage cs = CredentialStorage.getInstance(CredentialsActivity.this);
				EditText txtUsername = (EditText) findViewById(R.id.txtUsername);
				EditText txtPassword = (EditText) findViewById(R.id.txtPassword);
				
				
				cs.setCalnetId(txtUsername.getText().toString());
				cs.setCalnetPassphrase(txtPassword.getText().toString());

				Toast.makeText(CredentialsActivity.this, "CalNet credentials updated successfully!", Toast.LENGTH_SHORT).show();
			}
		});
    }
    
    @Override
	protected void onPause() {
		super.onPause();

		overridePendingTransition(R.anim.hold, R.anim.slide_out_down);
	}
    
}
