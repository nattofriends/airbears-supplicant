#!/usr/bin/env python

import auth, notification, wlan
from log import log, lock

import sys, threading

NO_UI = False

if not NO_UI:
    import ui
    tb = ui.init()
    
if not lock():
    if NO_UI:
        # This is important enough to print to the screen. 
        print "Error: could not obtain lockfile, quitting"
    else:
        tb.notice("Another instance of Airbears Supplicant is already running.")
    sys.exit(-1)
else:
    log("Lockfile acquired")
    
log("Started AirBears supplicant")
log("NO_UI = " + str(NO_UI))
if not NO_UI:
    tb.notice("Welcome to AirBears Supplicant")
    
def connection_callback():
    log("Received connection notification")
    if wlan.has_airbears():
        log("Connected to AirBears")
        if not NO_UI:
            tb.notice("Logging in...")
        success = auth.authenticate_from_file()
        if not NO_UI:
            if success: 
                tb.notice("Connected and logged in to AirBears!")
            else:
                tb.notice("Login failed")
    else:
        log("Connected to not-AirBears, ignoring...")

ns = notification.NetworkStatus(connection_callback)
monitor_thread = threading.Thread(target = ns.register)
monitor_thread.start()

# UI cannot run from another thread, for some reason
if not NO_UI:
    ui.start()
    connection_callback()
