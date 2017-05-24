#!/usr/bin/env python2
import os

CHANNEL = 6
SSID = 'test'
BEACON_INT = 100
HW_MODE = 'g'
WPA_PASSPHRASE = ''
INTERFACE = 'wlan0'
VALID_HW_MODES = ['a', 'b', 'g']
DN = open(os.devnull, 'w')
HOSTAPD_SHARED_LIB_PATH = './hostapd-2.6/hostapd/libhostapd.so'
HOSTAPD_CONF_PATH = '/tmp/hostapd.conf'
