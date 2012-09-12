package com.nol888.airbears.supplicant;

import android.app.Notification;
import android.app.NotificationManager;
import android.app.PendingIntent;
import android.app.Service;
import android.content.Intent;
import android.os.Binder;
import android.os.IBinder;
import android.support.v4.app.NotificationCompat;
import android.util.Log;

import com.nol888.airbears.supplicant.security.CredentialStorage;

public class SupplicantService extends Service {
	private static final int STATIC_NOTIFICATION = 1;
	private static final String LOGTAG = "AB_SUPP::SVC";

	public class LocalBinder extends Binder {
		public SupplicantService getService() {
			return SupplicantService.this;
		}
	}

	private final IBinder binder = new LocalBinder();
	private NotificationManager mNM;

	private AuthenticationState status = AuthenticationState.NO_CREDENTIALS;

	@Override
	public IBinder onBind(Intent arg0) {
		return binder;
	}

	@Override
	public void onCreate() {
		// Determine whether or not we have CalNet credentials.
		CredentialStorage cs = CredentialStorage.getInstance(this);
		if (cs.hasCalnetCredentials())
			status = AuthenticationState.NOT_CONNECTED;

		// Create the static notification.
		mNM = (NotificationManager) getSystemService(NOTIFICATION_SERVICE);

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

	@Override
	public int onStartCommand(Intent intent, int flags, int startId) {
		Log.i(LOGTAG, "Received start id " + startId + ": " + intent);

		// We want this service to continue running until it is explicitly
		// stopped, so return sticky.
		return START_STICKY;
	}

	@Override
	public void onDestroy() {
		super.onDestroy();

		if (mNM != null)
			mNM.cancel(STATIC_NOTIFICATION);
	}

	public AuthenticationState getAuthenticationState() {
		return this.status;
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
		};

		public abstract int getStringId();
	}
}
