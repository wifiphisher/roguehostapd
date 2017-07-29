"""
Module for setup hostapd shared library

* Originally we build the shared library by leveraging on
  disutils.command.build but we change to setuptools.command.install
  for the following two reasons:

  1. It seems that setuptools.command maintains the backward compatibility
     for the older version of pip but the distutils.command.intall does't
     do for that

  2. If we use the setuptools.command.build, the users will get the
     shared library by "pip install" but they will fail when use the
     "python setup.py install" since this command only copy the files
     to the "/usr/local/lib/python2.7/dist-package" instead of building
     the shared library first.

  So we choose to do the compilation work in install command.
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

# check users have installed the libnl and openssl shared library
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
        # Before installing, we compile the hostapd shared library first
        self.execute(compile_hostapd, [],
                     'Compiling hostapd shared library')
        # copy all the files to the /usr/local/lib/python2.7/dist-package
        install.run(self)

# Add package_data to include the shared library we have built
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
