"""
Module for setup hostapd shared library
"""

import sys
from ctypes.util import find_library
from distutils.core import setup, Extension
import roguehostapd.hostapd_constants as constants
import roguehostapd.buildutil.buildcommon as buildcommon
import roguehostapd.buildutil.build_files as build_files


def check_require_shared_libs():
    """
    Check if users have required libraries
    """
    shared_libs = {"nl-3": "libnl-3-dev",
                   "nl-genl-3": "libnl-genl-3-dev",
                   "ssl": "libssl-dev"}

    for libname in shared_libs:
        if not find_library(libname):
            print ("[" + constants.RED + "!" + constants.WHITE + "] " +
                   shared_libs[libname] + " is not found in the system!")
            sys.exit()

# check users have installed the libnl and openssl shared library
check_require_shared_libs()

EXT_MODULE = Extension(build_files.SHARED_LIB_PATH,
                       define_macros=build_files.HOSTAPD_MACROS,
                       libraries=['rt', 'ssl', 'crypto', 'nl-3', 'nl-genl-3'],
                       sources=build_files.get_all_source_files(),
                       include_dirs=[build_files.HOSTAPD_SRC,
                                     build_files.HOSTAPD_UTILS,
                                     build_files.LIB_NL3_PATH])
with buildcommon.nostdout():
    setup(
        name='roguehostapd',
        packages=['roguehostapd'],
        version='1.1.2',
        description='Hostapd wrapper for hostapd',
        url='https://github.com/wifiphisher/roguehostapd',
        author='Anakin',
        ext_modules=[EXT_MODULE]
    )
