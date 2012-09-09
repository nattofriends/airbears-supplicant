#!/usr/bin/env python

# Based on the PyObjC SystemConfiguration callback demos:
# <https://svn.red-bean.com/pyobjc/trunk/pyobjc/pyobjc-framework-SystemConfiguration/Examples/CallbackDemo/>

from Cocoa import *
from SystemConfiguration import *
import signal

def handleNetworkConfigChange(store, changedKeys, info):
	print "Global network configuration changed: ", changedKeys
	newState = SCDynamicStoreCopyValue(store, changedKeys.objectAtIndex_(0))
	print "New State: ", newState
	# Kick a change-intolerant service in the head

def clean_shutdown():
	CFRunLoopStop(CFRunLoopGetCurrent())
	sys.exit(0)

# This uses the SystemConfiguration framework to get a SCDynamicStore session
# and register for certain events. See the Appl SystemConfiguration
# documentation for details:
#
# <http://developer.apple.com/documentation/Networking/Reference/SysConfig/SCDynamicStore/CompositePage.html>
#
# TN1145 may also be of interest:
#	<http://developer.apple.com/technotes/tn/tn1145.html>

store = SCDynamicStoreCreate(None, "global-network-watcher", handleNetworkConfigChange, None)

# This is a simple script which only looks for IP-related changes but many
# other things are available. The easiest way to see what is available is to
# use the command-line scutil's list command.

# JJM: We need to add 'State:/Network/Global/IPv6' as well
SCDynamicStoreSetNotificationKeys(store, None, [ 'State:/Network/Global/IPv4', ])

# Get a CFRunLoopSource for our store session and add it to the application's runloop:
CFRunLoopAddSource(CFRunLoopGetCurrent(), SCDynamicStoreCreateRunLoopSource(None, store, 0), kCFRunLoopCommonModes)

# Add a signal handler so we can shutdown cleanly if we get a ^C:
# BUG: This does not work - it's necessary to ^Z or kill from another window
signal.signal(signal.SIGINT, clean_shutdown)

CFRunLoopRun()