from distutils.core import setup
import py2app

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
