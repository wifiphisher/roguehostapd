#!/usr/bin/env python2
"""
This module was made to wrap the hostapd
"""

import multiprocessing
import ctypes
import hostapd_constants


class HostapdConfig(object):
    """
    Handle the Hostapd configuration
    """

    def __init__(self):
        """
        Setup the class with all the given arguments
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
        """

        if 'wpa_passphrase' in config_dict:
            self.configuration_dict['wpa_key_mgmt'] = "WPA-PSK"
            self.configuration_dict['wpa_pairwise'] = "TKIP CCMP"
            self.configuration_dict['wpa'] = '3'

    def update_configs(self, config_dict):
        """
        Update the attributes based on the configuration dictionary
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
        """

        with open('/tmp/hostapd.conf', 'w') as conf:
            for key, value in self.configuration_dict.iteritems():
                if value:
                    conf.write(key + '=' + str(value) + '\n')

    @classmethod
    def is_ssid_valid(cls, ssid):
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

        self.hostapd_process = None

    def start(self):
        """
        Start the hostapd process
        """

        exe_path = ctypes.c_char_p('./hostapd-2.6/hostapd/hostapd')
        config_path = ctypes.c_char_p(hostapd_constants.HOSTAPD_CONF_PATH)
        str_arr_type = ctypes.c_char_p * 3

        hostapd_cmd = str_arr_type(
            exe_path, config_path, ctypes.c_char_p('-B'))
        hostapd_lib = ctypes.cdll.LoadLibrary(
            hostapd_constants.HOSTAPD_SHARED_LIB_PATH)
        self.hostapd_process = multiprocessing.Process(
            target=hostapd_lib.main, args=(len(hostapd_cmd), hostapd_cmd))

        self.hostapd_process.start()

    def stop(self):
        """
        Stop the hostapd process
        """

        self.hostapd_process.terminate()

if __name__ == '__main__':

    HOSTAPD_CONFIG_DICT = {
        'ssid': 'hahaha',
        'interface': 'wlan0',
        'wpa_passphrase': '12345678'}

    CONFIG_OBJ = HostapdConfig()
    CONFIG_OBJ.update_configs(HOSTAPD_CONFIG_DICT)
    CONFIG_OBJ.write_configs()
    HOSTAPD_OBJ = Hostapd()
    HOSTAPD_OBJ.start()
