package com.nol888.airbears.supplicant;

import java.net.InetAddress;
import java.net.UnknownHostException;

import org.apache.http.client.CookieStore;
import org.apache.http.client.protocol.ClientContext;
import org.apache.http.impl.client.BasicCookieStore;
import org.apache.http.protocol.BasicHttpContext;
import org.apache.http.protocol.HttpContext;

import android.net.http.AndroidHttpClient;
import android.util.Log;

public class CalNetAuthenticator {
	private static final String LOGTAG = "AB_SUPP::CALNET";
	private static final String CAS_NO_REDIR_URL = "https://auth.berkeley.edu/cas/login";
	private static final String CAS_URL = "https://auth.berkeley.edu/cas/login?service=https%3a%2f%2fwlan.berkeley.edu%2fcgi-bin%2flogin%2fcalnet.cgi%3fsubmit%3dCalNet%26url%3d";
	private static final String WLAN_LANDING_URL = "https://wlan.berkeley.edu/cgi-bin/login/calnet.cgi?url=&count=1";
	
	private static final CookieStore cookies = new BasicCookieStore();

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
		String cas_url = cas_no_redir ? CAS_NO_REDIR_URL : CAS_URL;
		AndroidHttpClient opener = AndroidHttpClient.newInstance(System.getProperty("http.agent"));
		opener.enableCurlLogging(LOGTAG, Log.DEBUG);
		
		HttpContext ctx = new BasicHttpContext();
		ctx.setAttribute(ClientContext.COOKIE_STORE, cookies);

	}
}
