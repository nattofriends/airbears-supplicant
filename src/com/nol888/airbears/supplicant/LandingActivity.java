package com.nol888.airbears.supplicant;

import android.app.Activity;
import android.app.Service;
import android.content.ComponentName;
import android.content.Intent;
import android.content.ServiceConnection;
import android.os.Bundle;
import android.os.Handler;
import android.os.IBinder;
import android.view.Menu;
import android.view.MenuItem;
import android.view.View;
import android.view.View.OnClickListener;
import android.widget.Button;
import android.widget.TextView;

import com.nol888.airbears.supplicant.security.CredentialStorage;

public class LandingActivity extends Activity {
	private final long UI_UPDATE_MILLIS = 20;

	private ServiceConnection mConnection = new ServiceConnection() {
		@Override
		public void onServiceConnected(ComponentName className, IBinder service) {
			supp_service = ((SupplicantService.LocalBinder) service).getService();
		}

		@Override
		public void onServiceDisconnected(ComponentName className) {
			supp_service = null;
		}
	};
	private Runnable mUpdateUI = new Runnable() {
		@Override
		public void run() {
			if(supp_service != null) {
				TextView status_text = (TextView) findViewById(R.id.statusText);
				status_text.setText(supp_service.getAuthenticationState().getStringId());
			}

			mHandler.postDelayed(this, UI_UPDATE_MILLIS);
		}
	};

	private SupplicantService supp_service;
	private Handler mHandler = new Handler();

	@Override
	public void onCreate(Bundle savedInstanceState) {
		super.onCreate(savedInstanceState);
		setContentView(R.layout.activity_landing);

		// Add event listeners.
		Button btnEnterCreds = (Button) findViewById(R.id.btnRegister);
		btnEnterCreds.setOnClickListener(new OnClickListener() {
			@Override
			public void onClick(View v) {
				Intent i = new Intent(LandingActivity.this, CredentialsActivity.class);
				startActivity(i);
			}
		});

		// Bind to instance of the supplicant service.
		Intent i = new Intent(this, SupplicantService.class);
		bindService(i, mConnection, Service.BIND_AUTO_CREATE);
		startService(i);

		// If we don't have credentials, go ahead and prompt the user for it.
		CredentialStorage cs = CredentialStorage.getInstance(this);
		if (!cs.hasCalnetCredentials()) {
			i = new Intent(this, CredentialsActivity.class);
			startActivity(i);
		}
		
		// Register UI update timer.
		mHandler.postDelayed(mUpdateUI, UI_UPDATE_MILLIS);
	}

	@Override
	public void onPause() {
		super.onPause();

		mHandler.removeCallbacks(mUpdateUI);
	}

	@Override
	public void onDestroy() {
		super.onDestroy();

		unbindService(mConnection);
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
		stopService(new Intent(this, SupplicantService.class));

		finish();
	}
}
