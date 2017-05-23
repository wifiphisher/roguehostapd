#!/usr/bin/env python2
"""
This module was made to wrap the hostapd
"""


import os
import subprocess
import time
import argparse
import hostapd_constants


class HostapdConfig(object):
    """
    Handle the Hostapd configuration
    """

    def __init__(self):
        """
        Setup the class with all the given arguments
        """

        self._ssid = hostapd_constants.SSID
        self._channel = hostapd_constants.CHANNEL
        self._beacon_int = hostapd_constants.BEACON_INT
        self._hw_mode = hostapd_constants.HW_MODE
        self._interface = hostapd_constants.INTERFACE
        self._wpa_passphrase = hostapd_constants.WPA_PASSPHRASE
        self.wpa_key_mgmt = ''
        self.wpa_pairwise = ''
        self.wpa = ''

    @property
    def ssid(self):
        """
        Get the ssid of the hostapd
        """

        return self._ssid

    @ssid.setter
    def ssid(self, value):
        """
        Set the ssid of the hostapd
        """

        if self.is_ssid_valid(value):
            self._ssid = value
        else:
            # TODO raise SSID Invalid Error
            pass

    @property
    def interface(self):
        """
        Get the interface name of the adapter which lunches hostapd
        """
        return self._interface

    @interface.setter
    def interface(self, value):
        """
        Set the interface name
        """
        self._interface = value

    @property
    def channel(self):
        """
        Get the channel number for the lunched AP
        """
        return self._channel

    @channel.setter
    def channel(self, value):
        """
        Set the channel number for the lunched AP
        """

        if value > 0:
            self._channel = value
        else:
            # TODO raise invalid channel number
            pass

    @property
    def beacon_int(self):
        """
        Get the beacon interval
        """

        return self._beacon_int

    @beacon_int.setter
    def beacon_int(self, val):
        """
        Set the beacon interval
        """

        if val > 0:
            self._beacon_int = val
        else:
            # TODO raise invalid beacon interval
            pass

    @property
    def hw_mode(self):
        """
        Get the hardware mode of the target AP
        """

        return self._hw_mode

    @hw_mode.setter
    def hw_mode(self, val):
        """
        Set the hardware mode of the target AP
        """

        if val in hostapd_constants.VALID_HW_MODES:
            self._hw_mode = val
        else:
            # TODO raise invalid hw_mode
            pass

    @property
    def wpa_passphrase(self):
        """
        Get the passphrase of AP
        """

        return self._wpa_passphrase

    @wpa_passphrase.setter
    def wpa_passphrase(self, value):
        """
        Set the passphrase of AP
        """

        self._wpa_passphrase = value

    def update_security_info(self, config_dict):
        """
        Update the security configuration if passphrase is specified
        """

        if 'wpa_passphrase' in config_dict:
            self.wpa_key_mgmt = "WPA-PSK"
            self.wpa_pairwise = "TKIP CCMP"
            self.wpa = '3'

    def update_configs(self, config_dict):
        """
        Update the attributes based on the configuration dictionary
        """

        for key, value in config_dict.iteritems():
            if key in self.__dict__:
                self.__dict__[key] = value
            else:
                raise KeyError('Unsupported hostapd configuation!')

        self.update_security_info(config_dict)

    def write_configs(self):
        """
        Write the configurations to the file
        """

        with open('/tmp/hostapd.conf', 'w') as conf:
            for key, value in self.__dict__.iteritems():
                if value:
                    conf.write(key + '=' + str(value) + '\n')

    def is_ssid_valid(self, ssid):
        """
        Check if the specified ssid is valid
        """

        return bool(len(ssid) < 33)


class Hostapd(object):
    """
    Hostapd wrapper class
    """

    def __init__(self):
        """
        Contruct the hostapd object
        """

        self.proc = None

    def start(self):
        """
        Start the hostapd process
        """

        self.proc = subprocess.Popen(
            ['hostapd', '/tmp/hostapd.conf'],
            stdout=hostapd_constants.DN,
            stderr=hostapd_constants.DN)
        try:
            time.sleep(2)
            if self.proc.poll() is not None:
                print 'Fail to start hostapd\n'
                raise Exception
        except KeyboardInterrupt:
            raise Exception

    def stop(self):
        """
        Stop the hostapd process
        """

        subprocess.call('pkill hostapd', shell=True)
        if os.path.isfile('/tmp/hostapd.conf'):
            os.remove('/tmp/hostapd.conf')


if __name__ == '__main__':
    hostapd_configuration = {
        'ssid': 'hahaha',
        'interface': 'wlan7',
        'wpa_passphrase': '12345678'}

    config_object = HostapdConfig()
    config_object.update_configs(hostapd_configuration)
    config_object.write_configs()

    hostapd = Hostapd()
    hostapd.start()
