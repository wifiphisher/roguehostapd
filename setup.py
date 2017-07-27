"""
Module for setup hostapd shared library
"""

import os
import sys
from ctypes.util import find_library
from subprocess import call
from setuptools.command.install import install
from setuptools import setup
import roguehostapd.hostapd_constants as constants

BASEPATH = os.path.dirname(os.path.abspath(__file__))
HOSTAPD_BUILD_PATH = os.path.join(BASEPATH, 'roguehostapd/hostapd-2.6/hostapd')


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

check_require_shared_libs()


class HostapdInstall(install):
    """
    Class for build the shared library of hostapd
    """

    def run(self):
        """
        Build and install the shared library of hostapd
        """

        def compile_hostapd():
            """
            Compile the shared library of hostapd
            """
            call(constants.CP_CMD, cwd=HOSTAPD_BUILD_PATH)
            call(constants.MAKE_CMD, cwd=HOSTAPD_BUILD_PATH)

        self.execute(compile_hostapd, [],
                     'Compiling hostapd shared library')
        install.run(self)

setup(
    name='roguehostapd',
    packages=['roguehostapd'],
    version='1.1.2',
    package_data={'roguehostapd': ['hostapd-2.6/hostapd/libhostapd.so']},
    include_package_data=True,
    description='Hostapd wrapper for hostapd',
    url='https://github.com/wifiphisher/roguehostapd',
    author='Anakin',
    cmdclass={
        'install': HostapdInstall,
        }
)
