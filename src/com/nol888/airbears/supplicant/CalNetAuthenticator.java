package com.nol888.airbears.supplicant;

import java.net.InetAddress;
import java.net.UnknownHostException;

import android.util.Log;

public class CalNetAuthenticator {
	private static final String LOGTAG = "AB_SUPP::CALNET";

	private CalNetAuthenticator() {
		throw new IllegalStateException("Don't do this.");
	}

	public static void blockOnDns() {
		for (;;) {
			try {
				Log.d(LOGTAG, "Testing DNS resolution...");
				InetAddress.getByName("www.google.com");
				Log.d(LOGTAG, "DNS is up!");
				
				return;
			} catch (UnknownHostException e) {
				Log.d(LOGTAG, "DNS resolution failed, trying again in 2 seconds.");

				try {
					Thread.sleep(2000);
				} catch (InterruptedException ex) {
				}
			}
		}
	}

	public static void authenticate(String id, String password, boolean cas_no_redir) {

	}
}
