# AirBears Supplicant

AirBears Supplicant does what it says on the tin.
It stores your CalNet credentials and automatically logs you in when you 
connect to the AirBears network, saving you from having to log into CalNet
each time! Now in a handy Android version.

About this Fork
--------
This is a separate branch of the excellent Windows/Mac [Airbears Supplicant](https://github.com/nattofriends/airbears-supplicant) written by nattofriends. (Why I forked the repository, I don't even know, as this app really has no code in common at all to the Python PC version.

Credentials
--------------
AirBears Supplicant uses the Android Account Manager to securely store your CalNet ID and passphrase. As a result, it requires several AccountManager related permissions, including, but not limited to, `AUTHENTICATE_ACCOUNTS`, `GET_ACCOUNTS`, `MANAGE_ACCOUNTS`, and `USE_CREDENTIALS`.

Platform Dependencies
---------------------
Currently, Airbears Supplicant targets Android 2.2 and above. This may change in the future, but as I own a device running Android 2.3, the SDK level will never rise above that.

Additional Permissions
----------------------
The `INTERNET` permission is required, and its use is self explanatory. AirBears Supplicant will never transmit your password to any third-party besides the CalNet Authentation Service.