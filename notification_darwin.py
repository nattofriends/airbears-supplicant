#!/usr/bin/env python

# Based on the PyObjC SystemConfiguration callback demos:
# <https://svn.red-bean.com/pyobjc/trunk/pyobjc/pyobjc-framework-SystemConfiguration/Examples/CallbackDemo/>

from log import log

from Cocoa import *
from SystemConfiguration import *
import time

# We are not main thread, therefore need to make own NSAutoreleasePool.

class NetworkStatus(object): # Actually, we're signing up for network connects and disconnects. Shouldn't be a problem, though... don't think there's a way of asking only for connect events
    MIN_ELAPSED = 0.1

    def handleNetworkConfigChange(self, store, changedKeys, info):
        pool = NSAutoreleasePool.alloc().init()
        newState = SCDynamicStoreCopyValue(store, changedKeys.objectAtIndex_(0))
        
        if newState is None:
            return # No point trying to log on if we have no connectivity -- although we have that DNS resolution check, there is no reason to continue here if we have nothing to gain
        
        # SCDynamicStore tends to notify us twice each network change, not sure exactly why. Don't respond to it if the time since last change is less than self.MIN_ELAPSED.
        new_last_updated = time.time()
        delta = new_last_updated - self.last_updated
        self.last_updated = new_last_updated
        
        if delta < self.MIN_ELAPSED:
            log("Change notification delta too little, ignoring...")
            return
    
        self.connection_callback()
        del pool

    def __init__(self, connection_callback):
        self.connection_callback = connection_callback
        self.last_updated = 0

    def register(self):
        pool = NSAutoreleasePool.alloc().init()
        store = SCDynamicStoreCreate(None, "airbears-supplicant-" + str(time.time()), self.handleNetworkConfigChange, None)
        SCDynamicStoreSetNotificationKeys(store, None, [ 'State:/Network/Global/IPv4', ])
        CFRunLoopAddSource(CFRunLoopGetCurrent(), SCDynamicStoreCreateRunLoopSource(None, store, 0), kCFRunLoopCommonModes)
        del pool
        CFRunLoopRun()