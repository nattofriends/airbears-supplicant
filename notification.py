import sys

if sys.platform == "win32":
    from notification_win32 import *
elif sys.platform == "darwin":
    from notification_darwin import *