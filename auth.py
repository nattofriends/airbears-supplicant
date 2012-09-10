#!/usr/bin/env python

"""Authentication to AirBears"""

import xplat
from log import log
import zlib, hashlib, os, urllib, urllib2, re, cookielib, time, socket, urlparse, sys

CREDENTIAL_FILE = os.path.join(xplat.appdata, "airbears_credentials")
CAS_URL = "https://auth.berkeley.edu/cas/login?service=https%3a%2f%2fwlan.berkeley.edu%2fcgi-bin%2flogin%2fcalnet.cgi%3fsubmit%3dCalNet%26url%3d"
WLAN_LANDING_URL = "https://wlan.berkeley.edu/cgi-bin/login/calnet.cgi?url=&count=1"

cookies = cookielib.CookieJar()
opener = urllib2.build_opener(urllib2.HTTPCookieProcessor(cookies))

def write_auth(username, password):
    # Needs to do something appropriately if cannot write here
    sha256 = hashlib.sha256()
    with open(CREDENTIAL_FILE, "w") as creds_file:
        compressed_creds = zlib.compress("{0}\xff{1}".format(username, password))
        sha256.update(compressed_creds)
        creds_file.write(sha256.digest() + compressed_creds)
        log("Wrote credentials to file")
        
def read_auth():
    """Read authentication credentials from CREDENTIAL_FILE. Also verifies that the dats is still intact"""
    if not os.path.exists(CREDENTIAL_FILE):
        log("Credentials file does not exist")
        return None
        
    sha256 = hashlib.sha256()
    with open(CREDENTIAL_FILE) as creds_file:
        contents = creds_file.read()
        hash = contents[:sha256.digest_size]
        credentials = contents[sha256.digest_size:]
        
        # Verify hash correct
        sha256.update(credentials)
        if hash != sha256.digest():
            log("Credentials are damaged")
            return None
        
        credentials = zlib.decompress(credentials).split("\xff")
        log("Read credentials from file")
        return credentials

        
def authenticate_from_file():
    credentials = read_auth()
    if credentials == None:
        return False
    return authenticate(*credentials) # ~_~
    
def authenticate(username, password, cas_no_redir = False): # [username, password] please
    """Attempt to authenticate."""
    credentials = [username, password]
    
    if cas_no_redir:
        log("Caller requested no redirection")
        
    # Wait a bit
    # Ideally we should be able to inquire when DNS resolution is up. Either loop-try the first access, or do something beforehand. cancel that. we can just loop-try until getaddrinfo stops failing.
    cas_host = urlparse.urlparse(CAS_URL).netloc
    while True:
        try:
            socket.getaddrinfo(cas_host, 443)
            break
        except:
            pass
    # time.sleep(1)
    log("DNS resolution is up, attempting authentication...")
    field_names = ["username", "password", "_eventId", "lt"]
    # credentials = read_auth()
    # if credentials == None:
        # log("Credentials are damaged")
        # return False
    
    # I think you might be able to hit the WLAN_LANDING_URL here and see if we're good to go...
    
    # Some CalNet nonsense
    # Source: http://www.nik3daz.com/timetable.py
    credentials.append("submit")
    
    # Now create the cookie jar and opener in module init so they can stay with us.
    
    # In case we want to only check the login, not ask CalNet to redirect back to WLAN (does not resolve externally).
    # For example, if someone runs this for the first time at home, and enters their credentials there.
    # It's odd to tell them that they have to wait until they are able to reach AirBears just to store their CalNet credentials
    if cas_no_redir:
        cas_real_url = urlparse.urlunparse(urlparse.urlparse(CAS_URL)[0:3] + (None, None, None))
    else:
        cas_real_url = CAS_URL
        
    # Slight possibility somehow we've already logged in...
    # The reason this happens is because I think the network state changes again on AirBears login.
    # So we get another notification and try to log in again.
    first_calnet_login = opener.open(cas_real_url).read()
    if first_calnet_login.find("already logged in to") != -1:
        log("Already logged in before attempting authentication (WLAN authentication redirect succeeded)")
        # Do this anyway
        content = opener.open(WLAN_LANDING_URL).read()
        # Hope we see it again, I am too lazy to check
        return True

    # Otherwise, attempt the authentication
    calnet_noop = re.findall(r'_cNoOpConversation.*?"', first_calnet_login)[0].replace('"', '')
    credentials.append(calnet_noop)
    post_values = urllib.urlencode(zip(field_names, credentials))
    cas_result = opener.open(cas_real_url, post_values).read()
    
    if cas_result.find("you provided are incorrect") != -1:
        log("Authentication failed")
        return False
        
    if cas_no_redir and cas_result.find("successfully logged into") != -1:
        log("Authentication complete (caller requested no WLAN redirect)")
        return True
    else: 
        content = opener.open(WLAN_LANDING_URL).read()
        if content.find("already logged in to") != -1:
            log("Already logged in (WLAN authentication redirect succeeded)")
        else:
            log("Authentication complete")
        return True

if __name__ == '__main__':
    # authenticate()
    print "Your CalNet credentials will be overwritten without checking for their validity."
    new_user = raw_input("CalNet ID: ")
    new_pass = raw_input("CalNet passphrase: ")
    write_auth(new_user, new_pass)
    print "Press any key to continue."
    if sys.platform == "win32":
        import msvcrt
        msvcrt.getch()
    elif sys.platform == "darwin":
        import sys, tty, termios
        fd = sys.stdin.fileno()
        old_settings = termios.tcgetattr(fd)
        try:
            tty.setraw(fd)
            sys.stdin.read(1)
        finally:
            termios.tcsetattr(fd, termios.TCSADRAIN, old_settings)
