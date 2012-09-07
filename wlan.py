"""Get the currently connected SSID(s) from active wireless adapters
From http://stackoverflow.com/questions/2851233/how-can-i-retrieve-the-signal-strength-of-nearby-wireless-lan-networks-on-window"""

from wlan_h import *
from log import log

from ctypes import *
from ctypes.wintypes import *
from sys import exit

AIRBEARS = "AirBears"

def has_airbears():
    connected = get_connected_wireless()
    log("Connected networks: " + str(connected))
    return AIRBEARS in connected

def get_connected_wireless():
    networks = []
    
    NegotiatedVersion = DWORD()
    ClientHandle = HANDLE()
    
    ret = WlanOpenHandle(1, None, byref(NegotiatedVersion), byref(ClientHandle))
    if ret != ERROR_SUCCESS:
        # exit(FormatError(ret))
        return
        
    # find all wireless network interfaces
    pInterfaceList = pointer(WLAN_INTERFACE_INFO_LIST())
    ret = WlanEnumInterfaces(ClientHandle, None, byref(pInterfaceList))
    if ret != ERROR_SUCCESS:
        # exit(FormatError(ret))
        return
        
    try:
        ifaces = customresize(pInterfaceList.contents.InterfaceInfo,
                              pInterfaceList.contents.NumberOfItems)
        # find each available network for each interface
        for iface in ifaces:
            # print "Interface: %s" % (iface.strInterfaceDescription)
            pWlanConnectionAttributes = pointer(WLAN_CONNECTION_ATTRIBUTES())
            ret = WlanQueryInterface(ClientHandle, byref(iface.InterfaceGuid), wlan_intf_opcode_current_connection, None, pointer(DWORD()), byref(pWlanConnectionAttributes), None)
            if ret != ERROR_SUCCESS: # Probably not connected
                # exit(FormatError(ret))
                continue
            try:
                connection_attributes = pWlanConnectionAttributes.contents
                ssid = connection_attributes.wlanAssociationAttributes.dot11Ssid
                ssid_string = ssid.SSID[:ssid.SSIDLength]
                networks.append(ssid_string)
            finally:
                pass
                WlanFreeMemory(pWlanConnectionAttributes)
        
    finally:
        WlanFreeMemory(pInterfaceList)
        
    return networks

if __name__ == '__main__':
    print "Connected to AirBears:", has_airbears()