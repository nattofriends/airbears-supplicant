# AirBears Supplicant

AirBears Supplicant does what it says on the tin.
It stores your CalNet credentials and automatically logs you in when you 
connect to the AirBears network, saving you from having to log into CalNet
each time! And it's not like other hacky solutions that require you to press a
bookmarklet in your web browser.

On Credentials
--------------
In order to be able to authenticate to CalNet with your CalNet ID and passphrase, the Supplicant needs to be able to store them around in a way that it can access later. This is a problem inherent with password managers, browser "Remember your password?" dialogs, and the like. Please be warned that your CalNet ID and passphrase will be stored on disk (not in plain text). 

Platform Dependencies
---------------------
AirBears Supplicant is designed for Windows, and makes use of several Windows components to receive network change notifications and query wireless interfaces.

Build Dependencies
------------------
AirBears Supplicant runs on 32-bit Python 2.7. The following are build dependencies: wxPython 2.9.4.0, py2exe 0.6.9, and pywin32 2.1.7. `build_exe.py` is a py2exe configuration script, which will build the application into `dist/airbears_supplicant.exe`. To build the application, run `build.bat`.