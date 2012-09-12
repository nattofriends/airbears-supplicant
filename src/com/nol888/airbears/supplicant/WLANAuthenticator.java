package com.nol888.airbears.supplicant;

import java.io.BufferedReader;
import java.io.IOException;
import java.io.InputStreamReader;
import java.net.InetAddress;
import java.net.UnknownHostException;
import java.util.ArrayList;
import java.util.List;

import org.apache.http.HttpResponse;
import org.apache.http.NameValuePair;
import org.apache.http.client.CookieStore;
import org.apache.http.client.HttpClient;
import org.apache.http.client.entity.UrlEncodedFormEntity;
import org.apache.http.client.methods.HttpGet;
import org.apache.http.client.methods.HttpPost;
import org.apache.http.client.methods.HttpUriRequest;
import org.apache.http.client.params.ClientPNames;
import org.apache.http.client.protocol.ClientContext;
import org.apache.http.impl.client.BasicCookieStore;
import org.apache.http.message.BasicNameValuePair;
import org.apache.http.params.BasicHttpParams;
import org.apache.http.protocol.BasicHttpContext;
import org.apache.http.protocol.HttpContext;

import android.net.http.AndroidHttpClient;
import android.util.Log;

public class WLANAuthenticator {
	private static final String LOGTAG = "AB_SUPP::CALNET";
	private static final String CAS_NO_REDIR_URL = "https://auth.berkeley.edu/cas/login";
	private static final String CAS_URL = "https://auth.berkeley.edu/cas/login?service=https%3a%2f%2fwlan.berkeley.edu%2fcgi-bin%2flogin%2fcalnet.cgi%3fsubmit%3dCalNet%26url%3d";
	private static final String WLAN_LANDING_URL = "https://wlan.berkeley.edu/cgi-bin/login/calnet.cgi?url=&count=1";

	private static final CookieStore cookies;
	private static final HttpContext ctx;
	private static final BasicHttpParams params;

	static {
		cookies = new BasicCookieStore();
		ctx = new BasicHttpContext();
		params = new BasicHttpParams();
		
		ctx.setAttribute(ClientContext.COOKIE_STORE, cookies);
		params.setBooleanParameter(ClientPNames.HANDLE_REDIRECTS, true);
	}

	private WLANAuthenticator() {
		throw new IllegalStateException("Don't do this.");
	}

	public static void blockOnDns() {
		for (;;) {
			try {
				Log.i(LOGTAG, "Testing DNS resolution...");
				InetAddress.getByName("sleepyti.me");
				Log.i(LOGTAG, "DNS is up!");

				return;
			} catch (UnknownHostException e) {
				Log.i(LOGTAG, "DNS resolution failed, trying again in 2 seconds.");

				try {
					Thread.sleep(2000);
				} catch (InterruptedException ex) {
				}
			}
		}
	}

	public static AuthenticationResult authenticate(String id, String password, boolean cas_no_redir) {
		String cas_url = cas_no_redir ? CAS_NO_REDIR_URL : CAS_URL;

		AndroidHttpClient opener = AndroidHttpClient.newInstance(System.getProperty("http.agent"));

		try {
			// Retrieve the CalNet login page.
			String response_string = makeRequest(opener, new HttpGet(cas_url), true);

			// If we're already logged in, log and return true.
			if (response_string.contains("already logged in to")) {
				Log.i(LOGTAG, "Already logged in before authentication (WLAN authentication redirect succeeded)");

				opener.close();
				return AuthenticationResult.SUCCESS;
			}

			// Otherwise, attempt the authentication.
			int startConversationIndex = response_string.indexOf("_cNoOpConversation");
			int endConversationIndex = response_string.indexOf("\"", startConversationIndex);
			String noOpConversation = response_string.substring(startConversationIndex, endConversationIndex);

			HttpPost calnetLoginPost = new HttpPost(cas_url);

			List<NameValuePair> loginNameValuePairs = new ArrayList<NameValuePair>(3);
			loginNameValuePairs.add(new BasicNameValuePair("username", id));
			loginNameValuePairs.add(new BasicNameValuePair("password", password));
			loginNameValuePairs.add(new BasicNameValuePair("lt", noOpConversation));
			loginNameValuePairs.add(new BasicNameValuePair("_eventId", "submit"));

			calnetLoginPost.setEntity(new UrlEncodedFormEntity(loginNameValuePairs));

			response_string = makeRequest(opener, calnetLoginPost, true);

			if (response_string.contains("you provided are incorrect")) {
				Log.i(LOGTAG, "Authentication failed.");

				opener.close();
				return AuthenticationResult.INVALID_CREDENTIALS;
			}
			if (cas_no_redir && response_string.contains("successfully logged into")) {
				Log.i(LOGTAG, "Authentication complete. (Caller requested no WLAN redirect.)");

				opener.close();
				return AuthenticationResult.SUCCESS;
			}

			response_string = makeRequest(opener, new HttpGet(WLAN_LANDING_URL), true);

			if (response_string.contains("already logged in to")) {
				Log.i(LOGTAG, "Already logged in. (WLAN authentication redirect succeeded.)");
			} else {
				Log.i(LOGTAG, "Authentication complete.");
			}

			opener.close();
			return AuthenticationResult.SUCCESS;
		} catch (Exception e) {
			Log.e(LOGTAG, "Unable to perform authentication request flow!", e);
			
			try {
				opener.close();
			} catch (Exception ex) {
			}

			return AuthenticationResult.FAILURE;
		}
	}


	private static String makeRequest(HttpClient client, HttpUriRequest request, boolean follow_redirects) throws IOException {
		if (follow_redirects)
			request.setParams(params);

		Log.d(LOGTAG, request.getRequestLine().toString());
		HttpResponse response = client.execute(request, ctx);
		Log.d(LOGTAG, response.getStatusLine().toString());
		
		BufferedReader rd = new BufferedReader(new InputStreamReader(response.getEntity().getContent()));
		String line = "";
		StringBuilder sb = new StringBuilder();
		while ((line = rd.readLine()) != null) {
			sb.append(line);
		}
		rd.close();
		response.getEntity().consumeContent();
		if (sb.length() == 0)
			throw new RuntimeException("Server returned empty page! bug?");

		return sb.toString();
	}

	public enum AuthenticationResult {
		SUCCESS,
		INVALID_CREDENTIALS,
		FAILURE
	}
}
