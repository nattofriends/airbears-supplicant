package com.nol888.airbears.supplicant;

import android.app.Notification;
import android.app.NotificationManager;
import android.app.PendingIntent;
import android.app.Service;
import android.content.BroadcastReceiver;
import android.content.Context;
import android.content.Intent;
import android.content.IntentFilter;
import android.net.ConnectivityManager;
import android.net.NetworkInfo;
import android.net.NetworkInfo.State;
import android.net.wifi.WifiInfo;
import android.net.wifi.WifiManager;
import android.os.AsyncTask;
import android.os.Binder;
import android.os.IBinder;
import android.support.v4.app.NotificationCompat;
import android.util.Log;

import com.nol888.airbears.supplicant.WLANAuthenticator.AuthenticationResult;

public class SupplicantService extends Service {
	private static final int STATIC_NOTIFICATION = 1;
	private static final String LOGTAG = "AB_SUPP::SVC";

	public static final String ACTION_AUTHENTICATE = "com.nol888.airbears.supplicant.action.AUTHENTICATE";

	public class LocalBinder extends Binder {
		public SupplicantService getService() {
			return SupplicantService.this;
		}
	}

	private final IBinder binder = new LocalBinder();

	private NotificationManager mNM;
	private WifiStateChangeReceiver mWSCR;

	private volatile AuthenticationState status = AuthenticationState.NO_CREDENTIALS;
	private volatile boolean authenticating = false;

	@Override
	public IBinder onBind(Intent arg0) {
		return binder;
	}

	@Override
	public void onCreate() {
		// Get notification manager.
		mNM = (NotificationManager) getSystemService(NOTIFICATION_SERVICE);

		// Determine whether or not we have CalNet credentials.
		CredentialStorage cs = CredentialStorage.getInstance(this);
		if (cs.hasCalnetCredentials())
			status = AuthenticationState.NOT_CONNECTED;

		// Create the static notification.
		updateNotification();

		// Create and register WiFi state change receiver.
		mWSCR = new WifiStateChangeReceiver();
		IntentFilter intentFilter = new IntentFilter();
		intentFilter.addAction(WifiManager.NETWORK_STATE_CHANGED_ACTION);
		intentFilter.addAction(WifiManager.WIFI_STATE_CHANGED_ACTION);
		registerReceiver(mWSCR, intentFilter);
	}

	@Override
	public int onStartCommand(Intent intent, int flags, int startId) {
		if (intent != null && ACTION_AUTHENTICATE.equals(intent.getAction())) {
			if (authenticating) {
				Log.i(LOGTAG, "Authentication already in progress, ignoring second request.");
			} else {
				Log.i(LOGTAG, "Performing AirBears authentication.");
				authenticating = true;

				CredentialStorage cs = CredentialStorage.getInstance(this);

				if (!cs.hasCalnetCredentials()) {
					Log.i(LOGTAG, "No CalNet credentials were stored, ignoring authentication request.");
					return START_STICKY;
				}

				new CalNetAuthenticateTask().execute(cs.getCalnetId(), cs.getCalnetPassphrase());
			}
		}
		else
			Log.i(LOGTAG, "Ignoring startService() call for uninteresting intent: " + intent);

		return START_STICKY;
	}

	@Override
	public void onDestroy() {
		super.onDestroy();

		if (mNM != null)
			mNM.cancel(STATIC_NOTIFICATION);
		if (mWSCR != null)
			unregisterReceiver(mWSCR);
	}

	public AuthenticationState getAuthenticationState() {
		return this.status;
	}

	private void setAuthenticationState(AuthenticationState newState) {
		this.status = newState;

		updateNotification();
	}

	private void updateNotification() {
		Intent notificationIntent = new Intent(this, LandingActivity.class);
		notificationIntent.addFlags(Intent.FLAG_ACTIVITY_CLEAR_TOP);
		PendingIntent contentIntent = PendingIntent.getActivity(this, 0, notificationIntent, 0);

		Notification notification = new NotificationCompat.Builder(this)
				.setSmallIcon(R.drawable.ic_launcher)
				.setContentTitle("AirBears Supplicant")
				.setContentText(getString(status.getStringId()))
				.setContentIntent(contentIntent)
				.build();
		notification.flags |= Notification.FLAG_ONGOING_EVENT;

		mNM.notify(STATIC_NOTIFICATION, notification);
	}

	public enum AuthenticationState {
		NO_CREDENTIALS {
			@Override
			public int getStringId() {
				return R.string.airbears_status_no_creds;
			}
		},
		NOT_CONNECTED {
			@Override
			public int getStringId() {
				return R.string.airbears_status_not_connected;
			}
		},
		WAITING_DNS {
			@Override
			public int getStringId() {
				return R.string.airbears_status_waiting_dns;
			}
		},
		AUTHENTICATING {
			@Override
			public int getStringId() {
				return R.string.airbears_status_authenticating;
			}
		},
		AUTHENTICATED {
			@Override
			public int getStringId() {
				return R.string.airbears_status_done;
			}
		},
		AUTHENTICATION_FAILED {
			@Override
			public int getStringId() {
				return R.string.airbears_status_invalid_creds;
			}
		},
		AUTHENTICATION_ERROR {
			@Override
			public int getStringId() {
				return R.string.airbears_status_error;
			};
		};

		public abstract int getStringId();
	}

	public class CalNetAuthenticateTask extends AsyncTask<String, Integer, AuthenticationResult> {

		@Override
		protected AuthenticationResult doInBackground(String... params) {
			setAuthenticationState(AuthenticationState.WAITING_DNS);

			WLANAuthenticator.blockOnDns();

			setAuthenticationState(AuthenticationState.AUTHENTICATING);

			return WLANAuthenticator.authenticate(params[0], params[1], false);
		}

		@Override
		protected void onPostExecute(AuthenticationResult result) {
			switch (result) {
			case SUCCESS:
				setAuthenticationState(AuthenticationState.AUTHENTICATED);
				break;
			case INVALID_CREDENTIALS:
				setAuthenticationState(AuthenticationState.AUTHENTICATION_FAILED);
				break;
			case FAILURE:
				setAuthenticationState(AuthenticationState.AUTHENTICATION_ERROR);
				break;
			}

			authenticating = false;
		}
	}

	private class WifiStateChangeReceiver extends BroadcastReceiver {
		@Override
		public void onReceive(Context c, Intent i) {
			// Wifi network connected.
			if (i.hasExtra(WifiManager.EXTRA_NETWORK_INFO)) {
				NetworkInfo info = i.getParcelableExtra(WifiManager.EXTRA_NETWORK_INFO);
				WifiManager mWM = (WifiManager) c.getSystemService(Context.WIFI_SERVICE);
				WifiInfo wlanInfo = mWM.getConnectionInfo();

				Log.d(LOGTAG, "Received network state change info: " + info);

				// We only care about Wifi networks.
				if (info.getType() == ConnectivityManager.TYPE_WIFI) {
					if (info.getState() == State.DISCONNECTED) {
						// Disconnection should show up as not connected.
						setAuthenticationState(AuthenticationState.NOT_CONNECTED);
					} else if (info.getState() == State.CONNECTED) {
						// Only care if we connected to a network called AirBears.
						if ("AirBears".equals(wlanInfo.getSSID()) || true) {
							Intent intent = new Intent(SupplicantService.this, SupplicantService.class);
							intent.setAction(ACTION_AUTHENTICATE);
							startService(intent);
						}
					}
				}
			}
			// WiFi state changed.
			else if (i.hasExtra(WifiManager.EXTRA_WIFI_STATE))
				if (i.getIntExtra(WifiManager.EXTRA_WIFI_STATE, -1) == WifiManager.WIFI_STATE_DISABLED) {
					Log.d(LOGTAG, "WiFi disabled; updating supplicant status.");
					setAuthenticationState(AuthenticationState.NOT_CONNECTED);
				}
		}
	}
}
