# AirBears Supplicant

AirBears Supplicant does what it says on the tin.
It stores your CalNet credentials and automatically logs you in when you 
connect to the AirBears network, saving you from having to log into CalNet
each time! And it's not like other hacky solutions that require you to press a
bookmarklet in your web browser.

Binaries
--------
If you don't feel like building this, you should [download the binary here](http://slush.warosu.org/stuff/airbears_supplicant.exe). A Mac binary is Coming Soon. An [android version](https://github.com/nol888/airbears-supplicant/downloads) is available (source in the [android branch](https://github.com/nattofriends/airbears-supplicant/tree/android)).

Credentials
--------------
In order to be able to authenticate to CalNet with your CalNet ID and passphrase, the Supplicant needs to be able to store them around in a way that it can access later. This is a problem inherent with password managers, browser "Remember your password?" dialogs, and the like. Please be warned that your CalNet ID and passphrase will be stored on disk (not in plain text). 

Platform Dependencies
---------------------
AirBears Supplicant works on Windows and Mac OS X, using platform-specific code to receive network change events and query the wireless interface. This functionality requires Windows XP SP2 or higher, or Mac OS X 10.6 or higher.

Build Dependencies
------------------
AirBears Supplicant runs on Python 2.7. 
py2exe and py2app are used on their respective platforms to create "binary" files for distribution.

wxPython 2.9 or greater is necessary to build. OS X builds current use wxPython Cocoa and has not been tested with wxPython Carbon.

On Windows, the most recent version of pywin32 (2.1.7) is also required.

There is a simple `Makefile` which will build for both platforms. 
