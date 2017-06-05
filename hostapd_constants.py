#!/usr/bin/env python2
"""
Define the constants for hostapd_binder
"""

import os

# hostapd configuration files
CHANNEL = 6
SSID = 'test'
KARMA_ENABLE = 0
BEACON_INT = 100
HW_MODE = 'g'
WPA_PASSPHRASE = ''
INTERFACE = 'wlan0'
VALID_HW_MODES = ['a', 'b', 'g']

# hostapd command line options
HOSTAPD_DEBUG_OFF = 0
HOSTAPD_DEBUG_ON = 1
HOSTAPD_DEBUG_VERBOSE = 2

DN = open(os.devnull, 'w')
HOSTAPD_DIR = 'hostapd-2.6/hostapd'
HOSTAPD_SHARED_LIB_PATH = os.path.join(HOSTAPD_DIR, 'libhostapd.so')
HOSTAPD_EXE_PATH = os.path.join(HOSTAPD_DIR, 'hostapd')
HOSTAPD_CONF_PATH = '/tmp/hostapd.conf'
