#!/usr/bin/env python2
"""
This module was made to wrap the hostapd
"""

import os
import threading
import ctypes
import hostapd_constants


class HostapdConfig(object):
    """
    Handle the Hostapd configuration
    """

    def __init__(self):
        """
        Setup the class with all the given arguments

        :param self: A HostapdConfig object
        :type self: HostapdConfig
        :return: None
        :rtype: None
        """

        self.configuration_dict = {
            'ssid': hostapd_constants.SSID,
            'channel': hostapd_constants.CHANNEL,
            'beacon_int': hostapd_constants.BEACON_INT,
            'hw_mode': hostapd_constants.HW_MODE,
            'interface': hostapd_constants.INTERFACE,
            'wpa_passphrase': hostapd_constants.WPA_PASSPHRASE,
            'wpa_key_mgmt': '',
            'wpa_pairwise': '',
            'wpa': ''
            }

    def update_security_info(self, config_dict):
        """
        Update the security configuration if passphrase is specified

        :param self: A HostapdConfig object
        :param config_dict: hostapd configuration dictionary
        :type self: HostapdConfig
        :type config_dict: dict
        :return: None
        :rtype: None
        """

        if 'wpa_passphrase' in config_dict:
            self.configuration_dict['wpa_key_mgmt'] = "WPA-PSK"
            self.configuration_dict['wpa_pairwise'] = "TKIP CCMP"
            self.configuration_dict['wpa'] = '3'

    def update_configs(self, config_dict):
        """
        Update the attributes based on the configuration dictionary

        :param self: A HostapdConfig object
        :param config_dict: hostapd configuration dictionary
        :type self: HostapdConfig
        :type config_dict: dict
        :return: None
        :rtype: None
        """

        for key, value in config_dict.iteritems():
            if key in self.configuration_dict:
                self.configuration_dict[key] = value
            else:
                raise KeyError('Unsupported hostapd configuation!')

        self.update_security_info(config_dict)

    def write_configs(self):
        """
        Write the configurations to the file

        :param self: A HostapdConfig object
        :type: HostapdConfig
        :return: None
        :rtype: None
        ..note: write the configuration file in the path /tmp/hostapd.conf
        """

        with open(hostapd_constants.HOSTAPD_CONF_PATH, 'w') as conf:
            for key, value in self.configuration_dict.iteritems():
                if value:
                    conf.write(key + '=' + str(value) + '\n')

    @classmethod
    def is_ssid_valid(cls, ssid):
        """
        Check if the specified ssid is valid

        :param cls: A HostapdConfig class
        :param ssid: The service set identifier
        :type cls: HostapdConfig class
        :type ssid: str
        :return: True if the ssid is valid
        :rtype: bool
        """

        return bool(len(ssid) < 33)


class Hostapd(object):
    """
    Hostapd wrapper class
    """

    def __init__(self):
        """
        Contruct the class

        :param self: A Hostapd object
        :type self: Hostapd
        :return: None
        :rtype: None
        """

        self.hostapd_thread = None
        self.hostapd_lib = None

    def start(self):
        """
        Start the hostapd process

        :param self: A Hostapd object
        :type self: Hostapd
        :return: None
        :rtype: None
        ..note: the start function uses ctypes to load the shared library
        of hostapd and use it to call the main function to lunch the AP
        """

        work_dir = os.path.dirname(os.path.abspath(__file__))
        exe_path = os.path.join(work_dir, hostapd_constants.HOSTAPD_EXE_PATH)

        config_path = hostapd_constants.HOSTAPD_CONF_PATH
        str_arr_type = ctypes.c_char_p * 2

        hostapd_cmd = str_arr_type(exe_path, config_path)

        self.hostapd_lib = ctypes.cdll.LoadLibrary(
            hostapd_constants.HOSTAPD_SHARED_LIB_PATH)

        self.hostapd_thread = threading.Thread(
            target=self.hostapd_lib.main, args=(len(hostapd_cmd), hostapd_cmd))

        self.hostapd_thread.start()

    def stop(self):
        """
        Stop the hostapd

        :param self: A Hostapd object
        :type self: Hostapd
        :return: None
        :rtype: None
        ..note: the stop function uses the eloop_terminate function in hostapd
        shared library to stop AP.
        """

        self.hostapd_lib.eloop_terminate()

if __name__ == '__main__':

    HOSTAPD_CONFIG_DICT = {
        'ssid': 'hahaha',
        'interface': 'wlan7',
        'wpa_passphrase': '12345678'}

    CONFIG_OBJ = HostapdConfig()
    CONFIG_OBJ.update_configs(HOSTAPD_CONFIG_DICT)
    CONFIG_OBJ.write_configs()
    HOSTAPD_OBJ = Hostapd()
    HOSTAPD_OBJ.start()
