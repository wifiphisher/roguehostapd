#!/usr/bin/env python2
"""
This module was made to wrap the hostapd
"""

import os
import threading
import ctypes
from roguehostapd.config.hostapdconfig import HostapdConfig
import roguehostapd.config.hostapdconfig as hostapdconfig


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
        self.config_obj = HostapdConfig()

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

    def is_alive(self):
        """
        API for check if the hostapd thread is running
        :param self: A Hostapd object
        :type self: Hostapd
        :return: True if the hostapd is running else False
        :rtype: bool
        """
        return self.hostapd_thread.is_alive()

    def create_hostapd_conf_file(self, hostapd_config, options):
        """
        Create the roguehostapd configuration file
        :param self: A Hostapd object
        :type self: Hostapd
        :param hostapd_config: Hostapd configuration for hostapd.conf
        :type hostapd_config: dict
        :param options: Hostapd command line options
        :type options: dict
        :return: None
        :rtype: None
        """
        self.config_obj.init_config()
        self.config_obj.write_configs(hostapd_config, options)

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

        # update the hostapd configuration based on user input
        self.create_hostapd_conf_file(hostapd_config, options)
        # get the hostapd command to lunch the hostapd
        hostapd_cmd = [hostapdconfig.HOSTAPD_EXECUTION_PATH,
                       hostapdconfig.ROGUEHOSTAPD_RUNTIME_CONFIGPATH]
        for key in self.config_obj.options:
            if self.config_obj.options[key]:
                hostapd_cmd += self.config_obj.options[key]
        num_of_args = len(hostapd_cmd)
        str_arr_type = ctypes.c_char_p * num_of_args
        hostapd_cmd = str_arr_type(*hostapd_cmd)

        # get the hostapd shared library
        self.hostapd_lib = ctypes.cdll.LoadLibrary(
            hostapdconfig.HOSTAPD_LIBPATH)

        # init hostapd lib info
        self.hostapd_lib.get_assoc_karma_data.restype = ctypes.POINTER(
            KarmaData)

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
        self.hostapd_lib.eloop_terminate()
        if self.hostapd_thread.is_alive():
            self.hostapd_thread.join(5)

        if os.path.isfile(hostapdconfig.ROGUEHOSTAPD_RUNTIME_CONFIGPATH):
            os.remove(hostapdconfig.ROGUEHOSTAPD_RUNTIME_CONFIGPATH)
        if os.path.isfile(hostapdconfig.ROGUEHOSTAPD_DENY_MACS_CONFIGPATH):
            os.remove(hostapdconfig.ROGUEHOSTAPD_DENY_MACS_CONFIGPATH)

if __name__ == '__main__':

    HOSTAPD_CONFIG_DICT = {
        'ssid': 'test',
        'interface': 'wlan0',
        'karma_enable': 1,
        'deny_macs': ['00:00:00:11:22:33']
        }

    HOSTAPD_OPTION_DICT = {
        'debug_verbose': True,
        'key_data': True,
        'timestamp': False,
        'version': False,
        'mute': True,
        'eloop_term_disable': True}
    HOSTAPD_OBJ = Hostapd()
    HOSTAPD_OBJ.start(HOSTAPD_CONFIG_DICT, HOSTAPD_OPTION_DICT)
    import time
    while True:
        try:
            time.sleep(1)
        except KeyboardInterrupt:
            HOSTAPD_OBJ.stop()
            break
