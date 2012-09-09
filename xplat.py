"""Cross-platform stuff, from http://stackoverflow.com/questions/1084697/how-do-i-store-desktop-application-data-in-a-cross-platform-way-for-python"""

import sys, os.path

APPNAME = "AirBearsSupplicant"

if sys.platform == 'darwin':
    from AppKit import NSSearchPathForDirectoriesInDomains
    # http://developer.apple.com/DOCUMENTATION/Cocoa/Reference/Foundation/Miscellaneous/Foundation_Functions/Reference/reference.html#//apple_ref/c/func/NSSearchPathForDirectoriesInDomains
    # NSApplicationSupportDirectory = 14
    # NSUserDomainMask = 1
    # True for expanding the tilde into a fully qualified path
    appdata = os.path.join(NSSearchPathForDirectoriesInDomains(14, 1, True)[0], APPNAME)
elif sys.platform == 'win32':
    appdata = os.path.join(os.environ['APPDATA'], APPNAME)
else:
    appdata = os.path.expanduser(os.path.join("~", "." + APPNAME))

if not os.path.exists(appdata):
    os.mkdir(appdata)