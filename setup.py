"""
Module for setup hostapd shared library
"""

import os
import sys
from distutils.command.install import install
from ctypes.util import find_library
from subprocess import call
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
                   shared_libs[libname] + " is not found in the system!"
                  )
            sys.exit()

check_require_shared_libs()

class HostapdInstall(install):
    """
    Class for build the shared library of hostapd
    """

    def run(self):

        install.run(self)
        make_cmd = ['make', 'hostapd_lib']
        cp_cmd = ['cp', 'defconfig', '.config']

        def compile_hostapd():
            """
            Compile the shared library of hostapd
            """
            call(cp_cmd, cwd=HOSTAPD_BUILD_PATH)
            call(make_cmd, cwd=HOSTAPD_BUILD_PATH)

        self.execute(compile_hostapd, [], 'Compiling hostapd shared library')

setup(
    name='roguehostapd',
    packages=['roguehostapd'],
    version='1.1.2',
    package_data={'hostapd': ['hostapd-2.6/hostapd/libhostapd.so']},
    include_package_data=True,
    description='Hostapd wrapper for hostapd',
    url='https://github.com/wifiphisher/roguehostapd',
    author='Anakin',
    cmdclass={
        'install': HostapdInstall,
        }
)
