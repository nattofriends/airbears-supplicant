package com.nol888.airbears.supplicant;

import android.app.Activity;
import android.content.Intent;
import android.os.Bundle;
import android.view.Menu;
import android.view.MenuItem;
import android.view.View;
import android.view.View.OnClickListener;
import android.widget.Button;

import com.nol888.airbears.supplicant.security.CredentialStorage;

public class LandingActivity extends Activity {

	@Override
	public void onCreate(Bundle savedInstanceState) {
		super.onCreate(savedInstanceState);
		setContentView(R.layout.activity_landing);

		Button btnEnterCreds = (Button) findViewById(R.id.btnRegister);
		btnEnterCreds.setOnClickListener(new OnClickListener() {
			public void onClick(View v) {
				Intent i = new Intent(LandingActivity.this, CredentialsActivity.class);
				startActivity(i);
			}
		});

		// TODO Query service for credential stuff.
		CredentialStorage cs = CredentialStorage.getInstance(this);
		if (!cs.hasCalnetCredentials()) {
			Intent i = new Intent(this, CredentialsActivity.class);
			startActivity(i);
		} else {
			// Query service for current status.
		}
	}

	@Override
	public boolean onCreateOptionsMenu(Menu menu) {
		getMenuInflater().inflate(R.menu.options_menu, menu);
		return true;
	}

	@Override
	public boolean onOptionsItemSelected(MenuItem item) {
		// Handle item selection
		switch (item.getItemId()) {
		case R.id.menu_exit:
			shutdown();
			return true;
		default:
			return super.onOptionsItemSelected(item);
		}
	}

	private void shutdown() {
		finish();
	}
}
