#!/usr/bin/env python2
"""
This module was made to wrap the hostapd
"""

import os
import threading
import ctypes
import hostapd_constants


class KarmaData(ctypes.Structure):
    """
    Handle the hostapd return mac/ssid data
    """
    pass


KarmaData._fields_ = [
    ("is_assoc", ctypes.c_ubyte),
    ("ssid_len", ctypes.c_size_t),
    ("ssid", ctypes.c_ubyte * 32),
    ("mac_addr", ctypes.c_ubyte * 6),
    ("next_data", ctypes.POINTER(KarmaData))]


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
        # configurations for hostapd.conf
        self.configuration_dict = {
            # required configurations
            'ssid': hostapd_constants.SSID,
            'channel': hostapd_constants.CHANNEL,
            'beacon_int': hostapd_constants.BEACON_INT,
            'hw_mode': hostapd_constants.HW_MODE,
            'interface': hostapd_constants.INTERFACE,
            # karma attack
            'karma_enable': hostapd_constants.KARMA_ENABLE,
            # security related configuratoins
            'wpa_passphrase': '',
            'wpa_key_mgmt': '',
            'wpa_pairwise': '',
            'wpa': ''
            }

        # configuration for hostapd command line options
        self.options = {
            'debug_level':  None,
            'key_data': None,
            'timestamp': None,
            'version': None,
            }

        # hostapd debug level
        self.debug_level = hostapd_constants.HOSTAPD_DEBUG_OFF

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

        if 'wpa_passphrase' in config_dict and config_dict['wpa_passphrase']:
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
            if (key in self.configuration_dict) and value:
                self.configuration_dict[key] = value
            elif key not in self.configuration_dict:
                raise KeyError('Unsupported hostapd configuation!')

        self.update_security_info(config_dict)

    def _update_debug_level(self, options):
        """
        Update the debug level from options dictionary

        :param self: A HostapdConfig object
        :type self: HostapdConfig
        :param options: configurations for command line options
        :type options: dict
        :return: None
        :rtype: None
        """
        self.debug_level = options['debug_level']
        if self.debug_level == hostapd_constants.HOSTAPD_DEBUG_VERBOSE:
            self.options['debug_level'] = tuple(['-ddd'])

    def update_options(self, options):
        """
        Update the comand line options

        :param self: A HostapdConfig object
        :type self: HostapdConfig
        :param options: configurations for command line options
        :type options: dict
        :return: None
        :rtype: None
        ..note: update the command line options
        """

        for key in options:
            if key in self.options and options[key]:
                if key == 'debug_level':
                    self._update_debug_level(options)
                elif key == 'key_data':
                    self.options[key] = tuple(['-K'])
                elif key == 'timestamp':
                    self.options[key] = tuple(['-t'])
                elif key == 'version':
                    self.options[key] = tuple(['-v'])

    def write_configs(self, config_dict, options):
        """
        Write the configurations to the file

        :param self: A HostapdConfig object
        :type self: HostapdConfig
        :param config_dict: configurations for hostapd.conf
        :type config_dict: dict
        :param options: hostapd command line options
        :type options: dict
        :return: None
        :rtype: None
        ..note: write the configuration file in the path /tmp/hostapd.conf
        """

        self.update_options(options)
        self.update_configs(config_dict)
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

        self.config_obj = None
        self.hostapd_thread = None
        self.hostapd_lib = None

    @staticmethod
    def _parse_karma_data(karma_data):
        """
        get the associated clients' mac address and essid

        :param self: A Hostapd object
        :type self: Hostapd
        :param karma_data: A KarmaData object
        :type karma_data: KarmaData

        :return: A list of tuple of essid and mac address tuple
        :rtype: list
        """

        ret = []
        if karma_data:
            current = karma_data
            while current:
                if current.contents.is_assoc:
                    # convert ssid_len to integer
                    ssid_len = int(current.contents.ssid_len)
                    # convert mac address to string
                    mac_addr = current.contents.mac_addr
                    mac_l = [format(mac_addr[i], 'x') for i in range(6)]
                    mac_str = ':'.join(mac_l)

                    # convert ssid to string
                    ssid_buf = current.contents.ssid
                    ssid_list = [ssid_buf[i] for i in range(ssid_len)]
                    ssid = ''.join(map(chr, ssid_list))
                    ret.append((mac_str, ssid))
                current = current.contents.next_data
        return ret

    def get_karma_data(self):
        """
        get the data for the KARMA attack victims from hostapd

        :param self: A Hostapd object
        :type self: Hostapd

        :return: A list of tuple of essid and mac address tuple
        :rtype: list
        """

        karma_data = self.hostapd_lib.get_assoc_karma_data()
        mac_ssid_pairs = self._parse_karma_data(karma_data)
        return mac_ssid_pairs

    def start(self, hostapd_config, options):
        """
        Start the hostapd process

        :param self: A Hostapd object
        :type self: Hostapd
        :param hostapd_config: Hostapd configuration for hostapd.conf
        :type hostapd_config: dict
        :param options: Hostapd command line options
        :type options: dict
        :return: None
        :rtype: None
        ..note: the start function uses ctypes to load the shared library
        of hostapd and use it to call the main function to lunch the AP
        """

        self.config_obj = HostapdConfig()
        self.config_obj.write_configs(hostapd_config, options)

        work_dir = os.path.dirname(os.path.abspath(__file__))
        exe_path = os.path.join(work_dir, hostapd_constants.HOSTAPD_EXE_PATH)
        shared_lib_path = os.path.join(
            work_dir, hostapd_constants.HOSTAPD_SHARED_LIB_PATH)

        config_path = hostapd_constants.HOSTAPD_CONF_PATH

        # get the hostapd command to lunch the hostapd
        hostapd_cmd = [exe_path, config_path]
        for key in self.config_obj.options:
            if self.config_obj.options[key]:
                hostapd_cmd += self.config_obj.options[key]
        num_of_args = len(hostapd_cmd)
        str_arr_type = ctypes.c_char_p * num_of_args
        hostapd_cmd = str_arr_type(*hostapd_cmd)

        # get the hostapd shared library
        self.hostapd_lib = ctypes.cdll.LoadLibrary(shared_lib_path)

        # init hostapd lib info
        self.hostapd_lib.get_assoc_karma_data.restype = ctypes.POINTER(
            KarmaData)

        # turn off the debug log if debug level not specified
        if not self.config_obj.debug_level:
            self.hostapd_lib.stdout_off()

        # start the hostapd thread
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
        # turn off the hostapd debug log if the debug_level is not turnned on
        if not self.config_obj.debug_level:
            self.hostapd_lib.stdout_off()

        self.hostapd_lib.eloop_terminate()

        if os.path.isfile(hostapd_constants.HOSTAPD_CONF_PATH):
            os.remove(hostapd_constants.HOSTAPD_CONF_PATH)

if __name__ == '__main__':

    HOSTAPD_CONFIG_DICT = {
        'ssid': 'hahaha',
        'interface': 'wlan0',
        'karma_enable': 1,
        'wpa_passphrase': '12345678'}

    HOSTAPD_OPTION_DICT = {
        'debug_level': hostapd_constants.HOSTAPD_DEBUG_VERBOSE,
        'key_data': True,
        'timestamp': False,
        'version': False}

    HOSTAPD_OBJ = Hostapd()
    HOSTAPD_OBJ.start(HOSTAPD_CONFIG_DICT, HOSTAPD_OPTION_DICT)
