import time, os, msvcrt

LOG_TO_FILE = True

LOCK_FILE = os.path.join(os.environ["APPDATA"], "airbears_supplicant_lockfile")
lock = None

LOG_FILE = os.path.join(os.environ["APPDATA"], "airbears_supplicant_log")
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
        msvcrt.locking(lock.fileno(), msvcrt.LK_NBLCK, 1) # IOError on failure
        return True # Lock succeeded
    except IOError, e:
        return False

def unlock():
    msvcrt.locking(lock.fileno(), msvcrt.LK_UNLCK, 1)
    lock.close()
    # Unlock happens before os._exit, in ui