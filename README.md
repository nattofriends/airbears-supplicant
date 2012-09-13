# AirBears Supplicant

AirBears Supplicant does what it says on the tin.
It stores your CalNet credentials and automatically logs you in when you connect to the AirBears network, saving you from having to log into CalNet each time!
Now in a handy Android version.

## About this Fork

This is a separate branch of the excellent Windows/Mac [Airbears Supplicant](https://github.com/nattofriends/airbears-supplicant) written by nattofriends. (Why I forked the repository, I don't even know, as this app really has no code in common at all to the Python PC version.)

## Binaries

Binaries are available on the [downloads page](https://github.com/nol888/airbears-supplicant/downloads). GitHub has a rather handy QR code feature that allows you to directly download the .apk on your Android phone, so I recommend you install the application that way. You will need to ensure that `Allow non-Market applications to be installed` or similar option is enabled.

## Usage Information

To set up, simply open the application and enter your CalNet ID and Passphrase. You do not have to be connected to AirBears for the initial setup. The app with then attempt to log into to CalNet to verify your entered information. If it cannot log in, you will be notified and you will be prompted to re-enter your passphrase. You may cancel this if you wish.

Once you have done that, simply move in range of any AirBears access point and the application will automatically authenticate. The main screen does not have to be showing for this to occur. If for some reason, authentication fails due to a network error, you can use the Options menu to force a re-authentication.

If you want to exit the Supplicant (in case you are paranoid about battery usage) simply open the options menu and select "Exit Airbears Supplicant". Note that the application will no longer be running in the background, and if you need to re-authenticate to AirBears, you will need to do it manually. (Or re-open the app.)

## Some Implementation Notes

### Credential Storage

AirBears Supplicant uses the standard [Android KeyStore](http://developer.android.com/reference/java/security/KeyStore.html) to securely store your CalNet credentials.

### Platform Dependencies

Currently, Airbears Supplicant targets Android 2.2 and above. This may change in the future, but as I own a device running Android 2.3, the SDK level will never rise above that.

### Additional Permissions

The `INTERNET` permission is required, the reason for which is hopefully obvious. To facilitate automatic authentication, AirBears Supplicant also requires the `ACCESS_WIFI_STATE` to subscribe to state change notifications, and read the SSID of the network you are currently connected to. AirBears Supplicant will never transmit your password to any third-party besides the CalNet Authentation Service.

## Bug Reports

If reporting a bug, please use a freely available Android Log Collector utility (I recommend [Log Collector](https://play.google.com/store/apps/details?id=com.xtralogic.android.logcollector&hl=en), an open-source application) to assist with triage and resolution. You can manually send only the lines that have a tag beginning with AB_SUPP if you wish.