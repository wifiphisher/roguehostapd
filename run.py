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

    return parser.parse_args()


def check_args(args):
    """
    Check the given arguments for logic errors
    """

    if args.wpa_passphrase and len(args.wpa_passphrase) < 8\
            or len(args.wpa_passphrase) > 64:
        sys.exit('preshared key not valid')


def run():
    """
    Run the hostapd
    """

    args = parse_args()
    check_args(args)

    config_obj = hostapd_controller.HostapdConfig()
    for arg in vars(args):
        arg_val = getattr(args, arg)
        if arg in config_obj.configuration_dict and arg_val:
            config_obj.configuration_dict[arg] = arg_val

    config_obj.write_configs()
    hostapd_obj = hostapd_controller.Hostapd()
    hostapd_obj.start()

run()
