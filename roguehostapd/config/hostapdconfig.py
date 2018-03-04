"""
Module handles hostapd configuration
"""

import re
import collections
import os
import json
from ConfigParser import SafeConfigParser

def get_default_settings():
    """
    Get the project default settings
    """
    config = SafeConfigParser()
    config.read(ROGUEHOSTAPD_DEFAULT_CONFIGPATH)
    default_settings = collections.defaultdict()
    for section in config.sections():
        default_settings[section] = {}
        for key, val in config.items(section):
            default_settings[section][key] = json.loads(val)
    return default_settings

# the configuration paths
CONFIG_DIR = os.path.dirname(__file__)
HOSTAPD_CONFIG_PATH = os.path.join(CONFIG_DIR, 'hostapd.conf')
ROGUEHOSTAPD_DEFAULT_CONFIGPATH = os.path.join(CONFIG_DIR, 'config.ini')
ROGUEHOSTAPD_RUNTIME_CONFIGPATH = os.path.join('/tmp', 'hostapd.conf')
ROGUEHOSTAPD_DENY_MACS_CONFIGPATH = os.path.join('/tmp', 'hostapd.deny')
DEFAULT_SETTINGS = get_default_settings()
# the roguehostapd package
TOP_DIR = os.path.dirname(CONFIG_DIR)
HOSTAPD_DIR = os.path.join(TOP_DIR, "hostapd-2_6")
HOSTAPD_LIBPATH = os.path.join(HOSTAPD_DIR, 'hostapd', 'libhostapd.so')
HOSTAPD_EXECUTION_PATH = os.path.join(HOSTAPD_DIR, 'hostapd', 'hostapd')
# terminal colors
WHITE = "\033[0m"
RED = "\033[31m"
TAN = "\033[93m"


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
        self.configuration_dict = collections.defaultdict()
        # configuration for hostapd command line options
        self.options = collections.defaultdict()
        # custom action and relies on transformation by roguehostapd
        self.custom_action = {
            # enable wps
            'wpspbc': self.update_wps_configuration,
            # the deny mac addresses
            'deny_macs': self.update_black_macs,
            'wpa2password': self.update_security_info,
        }

    def init_config(self):
        """
        Parse the hostapd.conf file in the hostapd source code and
        update to the attribute configuation_dict

        :param self: A HostapdConfig object
        :type self: HostapdConfig
        :return: None
        :rtype: None
        """
        # reset the configurations
        self.configuration_dict = collections.defaultdict()
        self.options = collections.defaultdict()
        # initialize the fullset hostapd configuration dictionary
        with open(HOSTAPD_CONFIG_PATH, 'r') as filep:
            for line in filep:
                m_obj = re.match(r'#([\S-]+)=[\S-].*$', line)
                if m_obj:
                    key = m_obj.group(1)
                    self.configuration_dict[key] = ''
        # init the option dictionary
        self.options.update(DEFAULT_SETTINGS['options'])
        # initialize the basic information
        self.configuration_dict.update(DEFAULT_SETTINGS['hostapd_config'])
        # initialize the rougehostapd custom config
        self.configuration_dict.update(DEFAULT_SETTINGS['custom_config'])

    def update_black_macs(self):
        """
        Update the black mac addresses for hostapd

        :param self: A HostapdConfig object
        :type self: HostapdConfig
        :return: None
        :rtype: None
        """
        if 'deny_macs' in self.configuration_dict and self.configuration_dict['deny_macs']:
            self.configuration_dict['macaddr_acl'] = 0
            self.configuration_dict['deny_mac_file'] = ROGUEHOSTAPD_DENY_MACS_CONFIGPATH
            # write the denied mac addresses in the output
            with open(ROGUEHOSTAPD_DENY_MACS_CONFIGPATH, 'w') as writer:
                for mac_addr in self.configuration_dict['deny_macs']:
                    writer.write(mac_addr+'\n')

    def update_wps_configuration(self):
        """
        Update the WPS configuration for hostapd

        :param self: A HostapdConfig object
        :type self: HostapdConfig
        :return: None
        :rtype: None
        """
        if 'wpspbc' in self.configuration_dict and self.configuration_dict['wpspbc']:
            # enable WPS
            self.configuration_dict['wps_state'] = '2'
            self.configuration_dict['ap_setup_locked'] = '1'
            self.configuration_dict['uuid'] = '12345678-9abc-def0-1234-56789abcdef0'
            self.configuration_dict['device_name'] = 'Wireless AP'
            self.configuration_dict['manufacturer'] = 'Company'
            self.configuration_dict['model_name'] = 'WAP'
            self.configuration_dict['model_number'] = '123'
            self.configuration_dict['serial_number'] = '12345'
            self.configuration_dict['device_type'] = '6-0050F204-1'
            self.configuration_dict['os_version'] = '01020300'
            self.configuration_dict['config_methods'] =\
                'label virtual_display virtual_push_button keypad'
            self.configuration_dict['eap_server'] = '1'

    def update_security_info(self):
        """
        Update the security configuration if passphrase is specified

        :param self: A HostapdConfig object
        :type self: HostapdConfig
        :return: None
        :rtype: None
        """

        if 'wpa2password' in self.configuration_dict and self.configuration_dict['wpa2password']:
            self.configuration_dict['wpa_passphrase'] = self.configuration_dict['wpa2password']
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
        # run custom callbacks
        for custom_config in self.custom_action:
            self.custom_action[custom_config]()

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

        for key in self.options:
            if key in options and not options[key]:
                self.options[key] = ''
            elif (key in self.options and self.options[key]) or\
                    (key in options and options[key]):
                if key == 'debug_verbose':
                    self.options['debug_verbose'] = tuple(['-ddd'])
                elif key == 'key_data':
                    self.options[key] = tuple(['-K'])
                elif key == 'timestamp':
                    self.options[key] = tuple(['-t'])
                elif key == 'version':
                    self.options[key] = tuple(['-v'])
                elif key == 'mute':
                    self.options[key] = tuple(['-s'])
                elif key == 'eloop_term_disable':
                    self.options[key] = tuple(['-E'])
            elif key in self.options and not self.options[key]:
                self.options[key] = ''
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
        ..note: config_dict and options are two user input dictionaries.
        These two input dictionaries will erase the default setting from
        config.json
        """

        self.update_options(options)
        self.update_configs(config_dict)
        with open(ROGUEHOSTAPD_RUNTIME_CONFIGPATH, 'w') as conf:
            for key, value in self.configuration_dict.iteritems():
                if value and key not in self.custom_action:
                    conf.write(key + '=' + str(value) + '\n')
