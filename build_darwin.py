from distutils.core import setup
import py2app, sys

try:
    import wx
except ImportError:
    print "wxPython is required to build AirBearsSupplicant."
    sys.exit(-1)
    
if wx.VERSION[0:2] < (2, 9):
    print "wxPython 2.9 or above is required.")
    sys.exit(-1)
    
# Needs a Cocoa check here

setup(
    app = ['main.py'],
    data_files = ['assets/tag.png'],
    options = {
        "py2app": {
            "iconfile": "assets/tag.icns",
            "plist": { # This really should be specified as a Info.plist... even an inline file as the Windows manifest would be fine...
                "CFBundleShortVersionString": "0.0.1",
                "CFBundleIdentifier": "org.warosu.AirBearsSupplicant",
                "CFBundleDevelopmentRegion": "English",
                "CFBundleExecutable": "AirBears Supplicant",
                "CFBundleDisplayName": "AirBears Supplicant",
                "LSUIElement": "1",
            }
        }
    }
)
