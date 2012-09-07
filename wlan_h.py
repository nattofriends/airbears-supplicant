"""Structures for wireless interface query"""

from ctypes import *
from ctypes.wintypes import *

def customresize(array, new_size):
    return (array._type_*new_size).from_address(addressof(array))

wlanapi = windll.LoadLibrary('wlanapi.dll')

ERROR_SUCCESS = 0

class GUID(Structure):
    _fields_ = [
        ('Data1', c_ulong),
        ('Data2', c_ushort),
        ('Data3', c_ushort),
        ('Data4', c_ubyte*8),
        ]

WLAN_INTERFACE_STATE = c_uint # For some reason, this came back as c_ulong
(wlan_interface_state_not_ready,
 wlan_interface_state_connected,
 wlan_interface_state_ad_hoc_network_formed,
 wlan_interface_state_disconnecting,
 wlan_interface_state_disconnected,
 wlan_interface_state_associating,
 wlan_interface_state_discovering,
 wlan_interface_state_authenticating) = map(WLAN_INTERFACE_STATE, xrange(0, 8))

class WLAN_INTERFACE_INFO(Structure):
    _fields_ = [
        ("InterfaceGuid", GUID),
        ("strInterfaceDescription", c_wchar * 256),
        ("isState", WLAN_INTERFACE_STATE)
        ]

class WLAN_INTERFACE_INFO_LIST(Structure):
    _fields_ = [
        ("NumberOfItems", DWORD),
        ("Index", DWORD),
        ("InterfaceInfo", WLAN_INTERFACE_INFO * 1)
        ]

WLAN_MAX_PHY_TYPE_NUMBER = 0x8
DOT11_SSID_MAX_LENGTH = 32
WLAN_REASON_CODE = DWORD
DOT11_BSS_TYPE = c_uint
(dot11_BSS_type_infrastructure,
 dot11_BSS_type_independent,
 dot11_BSS_type_any) = map(DOT11_BSS_TYPE, xrange(1, 4))
DOT11_PHY_TYPE = c_uint
dot11_phy_type_unknown      = 0
dot11_phy_type_any          = 0
dot11_phy_type_fhss         = 1
dot11_phy_type_dsss         = 2
dot11_phy_type_irbaseband   = 3
dot11_phy_type_ofdm         = 4
dot11_phy_type_hrdsss       = 5
dot11_phy_type_erp          = 6
dot11_phy_type_ht           = 7
dot11_phy_type_IHV_start    = 0x80000000
dot11_phy_type_IHV_end      = 0xffffffff 

DOT11_AUTH_ALGORITHM = c_uint
DOT11_AUTH_ALGO_80211_OPEN         = 1
DOT11_AUTH_ALGO_80211_SHARED_KEY   = 2
DOT11_AUTH_ALGO_WPA                = 3
DOT11_AUTH_ALGO_WPA_PSK            = 4
DOT11_AUTH_ALGO_WPA_NONE           = 5
DOT11_AUTH_ALGO_RSNA               = 6
DOT11_AUTH_ALGO_RSNA_PSK           = 7
DOT11_AUTH_ALGO_IHV_START          = 0x80000000
DOT11_AUTH_ALGO_IHV_END            = 0xffffffff

DOT11_CIPHER_ALGORITHM = c_uint
DOT11_CIPHER_ALGO_NONE            = 0x00
DOT11_CIPHER_ALGO_WEP40           = 0x01
DOT11_CIPHER_ALGO_TKIP            = 0x02
DOT11_CIPHER_ALGO_CCMP            = 0x04
DOT11_CIPHER_ALGO_WEP104          = 0x05
DOT11_CIPHER_ALGO_WPA_USE_GROUP   = 0x100
DOT11_CIPHER_ALGO_RSN_USE_GROUP   = 0x100
DOT11_CIPHER_ALGO_WEP             = 0x101
DOT11_CIPHER_ALGO_IHV_START       = 0x80000000
DOT11_CIPHER_ALGO_IHV_END         = 0xffffffff 

WLAN_AVAILABLE_NETWORK_CONNECTED = 1
WLAN_AVAILABLE_NETWORK_HAS_PROFILE = 2

WLAN_AVAILABLE_NETWORK_INCLUDE_ALL_ADHOC_PROFILES = 0x00000001
WLAN_AVAILABLE_NETWORK_INCLUDE_ALL_MANUAL_HIDDEN_PROFILES = 0x00000002

# tzhu
WLAN_INTF_OPCODE = c_uint
wlan_intf_opcode_autoconf_start                                 = 0
wlan_intf_opcode_autoconf_enabled                               = 1
wlan_intf_opcode_background_scan_enabled                        = 2
wlan_intf_opcode_media_streaming_mode                           = 3
wlan_intf_opcode_radio_state                                    = 4
wlan_intf_opcode_bss_type                                       = 5
wlan_intf_opcode_interface_state                                = 6
wlan_intf_opcode_current_connection                             = 7
wlan_intf_opcode_channel_number                                 = 8
wlan_intf_opcode_supported_infrastructure_auth_cipher_pairs     = 9
wlan_intf_opcode_supported_adhoc_auth_cipher_pairs              = 10
wlan_intf_opcode_supported_country_or_region_string_list        = 11
wlan_intf_opcode_current_operation_mode                         = 12
wlan_intf_opcode_supported_safe_mode                            = 13
wlan_intf_opcode_certified_safe_mode                            = 14
wlan_intf_opcode_hosted_network_capable                         = 15
wlan_intf_opcode_management_frame_protection_capable            = 16
wlan_intf_opcode_autoconf_end                                   = 0x0fffffff    
wlan_intf_opcode_msm_start                                      = 0x10000100    
wlan_intf_opcode_statistics                                     = 0x10000101
wlan_intf_opcode_rssi                                           = 0x10000102
wlan_intf_opcode_msm_end                                        = 0x1fffffff    
wlan_intf_opcode_security_start                                 = 0x20010000    
wlan_intf_opcode_security_end                                   = 0x2fffffff    
wlan_intf_opcode_ihv_start                                      = 0x30000000    
wlan_intf_opcode_ihv_end                                        = 0x3fffffff 

WLAN_CONNECTION_MODE = c_uint
(wlan_connection_mode_profile,
 wlan_connection_mode_temporary_profile,
 wlan_connection_mode_discovery_secure,
 wlan_connection_mode_discovery_unsecure,
 wlan_connection_mode_auto,
 wlan_connection_mode_invalid) = map(WLAN_CONNECTION_MODE, xrange(1, 7))

WLAN_OPCODE_VALUE_TYPE = c_uint
(wlan_opcode_value_type_query_only,
 wlan_opcode_value_type_set_by_group_policy,
 wlan_opcode_value_type_set_by_user,
 wlan_opcode_value_type_invalid) = map(WLAN_OPCODE_VALUE_TYPE, xrange(1, 5))

DOT11_MAC_ADDRESS = c_ubyte * 6

class DOT11_SSID(Structure):
    _fields_ = [
        ("SSIDLength", c_ulong),
        ("SSID", c_char * DOT11_SSID_MAX_LENGTH)
        ]

class WLAN_AVAILABLE_NETWORK(Structure):
    _fields_ = [
        ("ProfileName", c_wchar * 256),
        ("dot11Ssid", DOT11_SSID),
        ("dot11BssType", DOT11_BSS_TYPE),
        ("NumberOfBssids", c_ulong),
        ("NetworkConnectable", c_bool),
        ("wlanNotConnectableReason", WLAN_REASON_CODE),
        ("NumberOfPhyTypes", c_ulong),
        ("dot11PhyTypes", DOT11_PHY_TYPE * WLAN_MAX_PHY_TYPE_NUMBER),
        ("MorePhyTypes", c_bool),
        ("wlanSignalQuality", c_ulong),
        ("SecurityEnabled", c_bool),
        ("dot11DefaultAuthAlgorithm", DOT11_AUTH_ALGORITHM),
        ("dot11DefaultCipherAlgorithm", DOT11_CIPHER_ALGORITHM),
        ("Flags", DWORD),
        ("Reserved", DWORD)
        ]

class WLAN_AVAILABLE_NETWORK_LIST(Structure):
    _fields_ = [
        ("NumberOfItems", DWORD),
        ("Index", DWORD),
        ("Network", WLAN_AVAILABLE_NETWORK * 1)
        ]
        
class WLAN_ASSOCIATION_ATTRIBUTES(Structure):
    _fields_ = [
        ("dot11Ssid", DOT11_SSID),
        ("dot11BssType", DOT11_BSS_TYPE),
        ("dot11Bssid", DOT11_MAC_ADDRESS),
        ("dot11PhyType", DOT11_PHY_TYPE),
        ("uDot11PhyIndex", c_ulong),
        ("wlanSignalQuality", c_ulong),
        ("ulRxRate", c_ulong),
        ("ulTxRate", c_ulong)
        ]

class WLAN_SECURITY_ATTRIBUTES(Structure):
    _fields_ = [
        ("SecurityEnabled", c_bool),
        ("OneXEnabled", c_bool),
        ("dot11AuthAlgorithm", DOT11_AUTH_ALGORITHM),
        ("dot11CipherAlgorithm", DOT11_CIPHER_ALGORITHM)
        ]

class WLAN_CONNECTION_ATTRIBUTES(Structure):
    _fields_ = [
        ("isState", WLAN_INTERFACE_STATE),
        ("wlanConnectionMode", WLAN_CONNECTION_MODE),
        ("ProfileName", c_wchar * 256),
        ("wlanAssociationAttributes", WLAN_ASSOCIATION_ATTRIBUTES),
        ("wlanSecurityAttributes", WLAN_SECURITY_ATTRIBUTES)
        ]

WlanOpenHandle = wlanapi.WlanOpenHandle
WlanOpenHandle.argtypes = (DWORD, c_void_p, POINTER(DWORD), POINTER(HANDLE))
WlanOpenHandle.restype = DWORD

WlanEnumInterfaces = wlanapi.WlanEnumInterfaces
WlanEnumInterfaces.argtypes = (HANDLE, c_void_p, 
                               POINTER(POINTER(WLAN_INTERFACE_INFO_LIST)))
WlanEnumInterfaces.restype = DWORD

WlanGetAvailableNetworkList = wlanapi.WlanGetAvailableNetworkList
WlanGetAvailableNetworkList.argtypes = (HANDLE, POINTER(GUID), DWORD, c_void_p, 
                                        POINTER(POINTER(WLAN_AVAILABLE_NETWORK_LIST)))
WlanGetAvailableNetworkList.restype = DWORD

WlanQueryInterface = wlanapi.WlanQueryInterface
WlanQueryInterface.argtypes = (HANDLE, POINTER(GUID), WLAN_INTF_OPCODE, c_void_p, POINTER(DWORD), POINTER(POINTER(WLAN_CONNECTION_ATTRIBUTES)), POINTER(WLAN_OPCODE_VALUE_TYPE))
WlanQueryInterface.restype = DWORD

WlanFreeMemory = wlanapi.WlanFreeMemory
WlanFreeMemory.argtypes = [c_void_p]