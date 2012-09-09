"""Logging and run lock stuff."""

import xplat

import time, os, sys

if sys.platform == "win32":
    import msvcrt
else:
    import fcntl

LOG_TO_FILE = True

LOCK_FILE = os.path.join(xplat.appdata, "airbears_supplicant_lockfile")
lock = None

LOG_FILE = os.path.join(xplat.appdata, "airbears_supplicant_log")
if LOG_TO_FILE:
    file = open(LOG_FILE, "a")

def log(msg):
    formatted = "{0}  {1}".format(time.asctime(), msg)
    if LOG_TO_FILE:
        file.write(formatted + "\n")
        file.flush()
        os.fsync(file.fileno())
    else:
        print formatted

def lock(): # This really shouldn't be here
    global lock
    lock = open(LOCK_FILE, "w")
    try:
        if sys.platform == "win32":
            msvcrt.locking(lock.fileno(), msvcrt.LK_NBLCK, 1) # IOError on failure
        else:
            fcntl.lockf(lock.fileno(), fcntl.LOCK_EX | fcntl.LOCK_NB)
        return True # Lock succeeded
    except IOError, e:
        return False

def unlock():
    if sys.platform == "win32":
        msvcrt.locking(lock.fileno(), msvcrt.LK_UNLCK, 1)
    else:
        fcntl.flock(lock.fileno(), fcntl.LOCK_UN)
    lock.close()
    os.unlink(LOCK_FILE)
    # Unlock happens before os._exit, in ui