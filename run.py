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

    parser.add_argument(
        "-kA", "--karma_enable", action='store_const', const=1,
        help="Enabling karma attack")

    return parser.parse_args()


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

    config_obj = hostapd_controller.HostapdConfig()
    config_obj.write_configs(vars(args))
    hostapd_obj = hostapd_controller.Hostapd()
    hostapd_obj.start()

run()
