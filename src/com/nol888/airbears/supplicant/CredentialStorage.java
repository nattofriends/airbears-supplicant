package com.nol888.airbears.supplicant;

import java.io.BufferedReader;
import java.io.BufferedWriter;
import java.io.File;
import java.io.FileInputStream;
import java.io.FileOutputStream;
import java.io.IOException;
import java.io.InputStreamReader;
import java.io.OutputStreamWriter;
import java.nio.charset.Charset;
import java.security.GeneralSecurityException;
import java.security.KeyStore;
import java.security.KeyStore.ProtectionParameter;
import java.security.KeyStore.SecretKeyEntry;
import java.security.KeyStoreException;
import java.security.SecureRandom;

import javax.crypto.spec.SecretKeySpec;

import android.content.Context;
import android.util.Log;

import com.ostermiller.RandPass;

public class CredentialStorage {
	private static final String LOGTAG = "AB_SUPP::CredentialStorage";

	private static class CredentialStorageLoader {
		private final static CredentialStorage instance = new CredentialStorage();
	}

	private static final ProtectionParameter entryProtection = new KeyStore.PasswordProtection("秘密です。".toCharArray());

	private Context c;
	private KeyStore ks;
	private char[] keystorekey = new char[512];

	private CredentialStorage() {
		if (CredentialStorageLoader.instance != null)
			throw new IllegalAccessError("CredentialStorage should not be instantiated.");
	}

	private synchronized void init(Context c) {
		if (ks != null)
			return;

		this.c = c;

		// Load/generate key and keystore.
		try {
			FileInputStream fis = c.openFileInput("keystore.key");
			BufferedReader reader = new BufferedReader(new InputStreamReader(fis, Charset.defaultCharset()));
			int chars = reader.read(keystorekey);

			Log.i(LOGTAG, "Successfully read " + chars + " chars from file.");

			reader.close();
			fis.close();
		} catch (IOException e) {
			Log.i(LOGTAG, "Keystore key was inaccessable, generating a new key.", e);

			RandPass rp = new RandPass(new SecureRandom(), RandPass.PRINTABLE_ALPHABET);
			rp.getPassChars(keystorekey);

			try {
				FileOutputStream fos = c.openFileOutput("keystore.key", Context.MODE_PRIVATE);
				BufferedWriter writer = new BufferedWriter(new OutputStreamWriter(fos, Charset.defaultCharset()));
				writer.write(keystorekey);
				writer.close();
				fos.close();
			} catch (IOException e2) {
				Log.e(LOGTAG, "Unable to save keystore key... D:", e2);
			}
		}

		try {
			File keystoreFile = new File(c.getFilesDir(), "keystore.keystore");
			if (!keystoreFile.exists())
			{
				ks = KeyStore.getInstance(KeyStore.getDefaultType());
				ks.load(null, keystorekey);

				saveKeystore();
			} else {
				ks = KeyStore.getInstance(KeyStore.getDefaultType());
				ks.load(c.openFileInput("keystore.keystore"), keystorekey);

				Log.i(LOGTAG, "Successfully loaded keystore from file.");
			}
		} catch (IOException e) {
			Log.i(LOGTAG, "Keystore was inaccessable, generating new keystore.");

			try {
				ks = KeyStore.getInstance(KeyStore.getDefaultType());
				ks.load(null, keystorekey);

				saveKeystore();
			} catch (Exception ex) {
				Log.e(LOGTAG, "Unable to store new keystore, giving up.", ex);
			}

		} catch (Exception e) {
			Log.e(LOGTAG, "Error loading or creating keystore.", e);
		}
	}

	public boolean hasCalnetCredentials() {
		stateCheck();

		try {
			return ks.containsAlias("calnet-username") && ks.containsAlias("calnet-himitsu");
		} catch (KeyStoreException e) {
			Log.e(LOGTAG, "Error accessing keystore!", e);

			return false;
		}
	}

	public String getCalnetId() {
		stateCheck();

		try {
			SecretKeySpec sks = (SecretKeySpec) ((SecretKeyEntry) ks.getEntry("calnet-username", entryProtection)).getSecretKey();
			String s = new String(sks.getEncoded(), "utf-8");

			return s;
		} catch (Exception e) {
			Log.e(LOGTAG, "Couldn't retrieve CalNet ID.", e);
		}

		return "";
	}

	public String getCalnetPassphrase() {
		stateCheck();

		try {
			SecretKeySpec sks = (SecretKeySpec) ((SecretKeyEntry) ks.getEntry("calnet-himitsu", entryProtection)).getSecretKey();
			String s = new String(sks.getEncoded(), "utf-8");

			return s;
		} catch (Exception e) {
			Log.e(LOGTAG, "Couldn't retrieve CalNet passphrase.", e);
		}

		return "";
	}

	public synchronized void setCalnetId(String id) {
		try {
			SecretKeySpec sks = new SecretKeySpec(id.getBytes("utf-8"), "himitsu");
			ks.setEntry("calnet-username", new SecretKeyEntry(sks), entryProtection);
			saveKeystore();
		} catch (Exception e) {
			Log.e(LOGTAG, "Couldn't save CalNet ID.", e);
		}
	}

	public synchronized void setCalnetPassphrase(String pw) {
		try {
			SecretKeySpec sks = new SecretKeySpec(pw.getBytes("utf-8"), "himitsu");
			ks.setEntry("calnet-himitsu", new SecretKeyEntry(sks), entryProtection);
			saveKeystore();
		} catch (Exception e) {
			Log.e(LOGTAG, "Couldn't save CalNet ID.", e);
		}
	}

	private void stateCheck() {
		if (ks == null)
			throw new IllegalStateException("ks is null!");
	}

	private void saveKeystore() throws IOException, GeneralSecurityException {
		FileOutputStream fis = c.openFileOutput("keystore.keystore", Context.MODE_PRIVATE);
		ks.store(fis, keystorekey);
		Log.i(LOGTAG, "Successfully updated/created keystore.");
	}

	public static CredentialStorage getInstance(Context c) {
		if (CredentialStorageLoader.instance.ks == null)
			CredentialStorageLoader.instance.init(c);

		return CredentialStorageLoader.instance;
	}

}
