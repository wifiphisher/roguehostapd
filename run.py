#!/usr/bin/env python2
"""
Module for running or stopping hostapd
"""

import argparse
import sys
import hostapd_controller


def parse_args():
    """
    Parse the arguments from command line
    """

    parser = argparse.ArgumentParser()

    # add options for hostapd.conf
    parser.add_argument(
        "-ssid", "--ssid", help="Specify the service set identifier of the AP")

    parser.add_argument(
        "-c", "--channel", help="Specify the channel of the AP")

    parser.add_argument(
        "-bI", "--beacon_int", help="Specify the beacon in millisecond")

    parser.add_argument(
        "-i", "--interface", help="Interface used to lunch AP")

    parser.add_argument(
        "-pK", "--wpa_passphrase", help="WPA/RSN passhrase")

    parser.add_argument(
        "-kA", "--karma_enable", action='store_const', const=1,
        help="Enabling karma attack")

    # add hostapd command line options
    parser.add_argument(
        "-d", "--debug_level", action='store_true',
        help="Enabling the verbose debug log")

    parser.add_argument(
        "-K", "--key_data", action='store_true',
        help="include key data in debug messages")

    parser.add_argument(
        "-t", "--timestamp", action='store_true',
        help="include timestamps in some debug messages")

    parser.add_argument(
        "-v", "--version", action='store_true',
        help="show hostapd version")

    return parser.parse_args()


def get_configuration_dicts(arg_dict):
    """
    Get the dictionary for hostapd.conf and cmd line options
    """

    config_obj = hostapd_controller.HostapdConfig()
    hostapd_dict = {}
    options = {}
    for key, val in arg_dict.iteritems():
        if key in config_obj.configuration_dict:
            hostapd_dict[key] = val
        elif key in config_obj.options:
            options[key] = val

    return hostapd_dict, options


def check_args(args):
    """
    Check the given arguments for logic errors
    """

    if args.wpa_passphrase and (
            len(args.wpa_passphrase) < 8 or len(args.wpa_passphrase) > 64):

        sys.exit('preshared key not valid')


def run():
    """
    Run the hostapd
    """

    args = parse_args()
    check_args(args)
    hostapd_dict, options = get_configuration_dicts(vars(args))
    hostapd_obj = hostapd_controller.Hostapd()
    hostapd_obj.start(hostapd_dict, options)

run()
