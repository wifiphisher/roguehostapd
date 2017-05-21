#!/usr/bin/env python2
import hostapd_constants
import subprocess
import time
import argparse

class HostapdConfig:

    def __init__(self):
        self.ssid = hostapd_constants.SSID
        self.channel = hostapd_constants.CHANNEL
        self.beacon_int = hostapd_constants.BEACON_INT
        self.hw_mode = hostapd_constants.HW_MODE
        self.interface = hostapd_constants.INTERFACE
        self.wpa_passphrase = hostapd_constants.WPA_PASSPHRASE

    @property
    def ssid(self):
        return __ssid

    @ssid.setter
    def ssid(self, value):
        if self.is_ssid_valid(value):
            self.__ssid = value
        else:
            #TODO raise SSID Invalid Error
            pass

    @property
    def interface(self):
        return __interface

    @interface.setter
    def interface(self, value):
        self.__interface = value

    @property
    def channel(self):
        return __channel

    @channel.setter
    def channel(self, value):
        if channel > 0:
            self.__channel = value
        else:
            #TODO raise invalid channel number
            pass

    @property
    def beacon_int(self):
        return __beacon_int

    @beacon_int.setter
    def beacon_int(self, val):
        if val > 0:
            self.__beacon_int = val
        else:
            #TODO raise invalid beacon interval
            pass

    @property
    def hw_mode(self):
        return self.__hw_mode 

    @hw_mode.setter
    def hw_mode(self, val):
        if val in constants.VALID_HW_MODES:
            self.__hw_mode = val
        else:
            #TODO raise invalid hw_mode
            pass

    @property
    def wpa_passphrase(self):
        return self.__wpa_passphrase

    @wpa_passphrase.setter
    def wpa_passphrase(self, value):
        self.__wpa_passphrase = value

    def update_security_info(self, config_dict):
        if 'wpa_passphrase' in config_dict:
            self.wpa_key_mgmt = "WPA-PSK"
            self.wpa_pairwise = "TKIP CCMP"
            self.wpa = '3'

    def update_configs(self, config_dict):
        for key, value in config_dict.iteritems():
            if key in self.__dict__:
                self.__dict__[key] = value
            else:
                raise KeyError('Unsupported hostapd configuation!')

        self.update_security_info(config_dict)

    def write_configs(self):
        with open('/tmp/hostapd.conf', 'w') as conf:
            for key, value in self.__dict__.iteritems():
                if value:
                    conf.write(key + '=' + str(value) + '\n')

    def is_ssid_valid(self, ssid):
        if len(ssid) < 33:
            return True
        else:
            return False

class Hostapd:

    def __init__(self):
        self.proc = None

    def start(self):
        self.proc = subprocess.Popen(['hostapd', '/tmp/hostapd.conf'],
                        stdout=hostapd_constants.DN,
                        stderr=hostapd_constants.DN)
        try:
            time.sleep(2)
            if self.proc.poll() != None:
                print('Fail to start hostapd\n')
                raise Exception
        except KeyboardInterrupt:
                raise Exception

    def stop(self):
        subprocess.call('pkill hostapd', shell=True)
        if os.path.isfile('/tmp/hostapd.conf'):
            os.remove('/tmp/hostapd.conf')


if __name__ == '__main__':
    config = {
                'ssid' : 'hahaha',\
                'interface' : 'wlan7',\
                'wpa_passphrase' : '12345678'}

    a = HostapdConfig()
    a.update_configs(config)
    a.write_configs()

    hostapd = Hostapd()
    hostapd.start()



