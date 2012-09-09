#!/usr/bin/env python

"""Via https://github.com/allfro/sploitego/blob/master/src/sploitego/webtools/geolocate.py"""

from log import log

AIRBEARS = "AirBears"

from Foundation import NSBundle, objc

CoreWLANBundle = NSBundle.bundleWithPath_(objc.pathForFramework('/System/Library/Frameworks/CoreWLAN.framework'))
if CoreWLANBundle is None:
    raise SystemError("Unable to load wireless bundle. Maybe it's not supported?") # CoreWLAN is 10.6+ only
CoreWLANBundle.load()

def has_airbears():
    connected = get_connected_wireless()
    if connected is None:
        return False
    log("Active connected network: " + connected)
    return AIRBEARS == connected
    

def get_connected_wireless(): # I _think_ I might have to call [CWInterface interface] every time...
    CWInterface = CoreWLANBundle.classNamed_('CWInterface')
    if CWInterface is None:
        raise SystemError('Unable to load CWInterface.') # Possibly < 10.6?
        
    default_interface = CWInterface.interface()
    if default_interface is None or not default_interface:
        # raise SystemError('Unable to load wireless interface.') # If it's not there, don't complain
        return ""
        
    return default_interface._.ssid

