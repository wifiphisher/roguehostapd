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
