"""
Module for setup hostapd shared library
"""

import shutil
try:
    from setuptools import setup
    from setuptools.command.install import install
except ImportError:
    from distutils.core import setup
    from distutils.command.install import install
from distutils.command.build_ext import build_ext
import roguehostapd.hostapd_constants as constants
import roguehostapd.buildutil.buildcommon as buildcommon
import roguehostapd.buildutil.buildexception as buildexception

# define project information
NAME = 'roguehostapd'
PACKAGES = ['roguehostapd',
            'examples',
            'roguehostapd.buildutil']
PACKAGE_DIR = {'roguehostapd': 'roguehostapd'}
PACKAGE_DATA = {'roguehostapd': ['hostapd-2_6/hostapd/hostapd.conf']}
VERSION = '1.1.2'
DESCRIPTION = 'Hostapd wrapper for hostapd'
URL = 'https://github.com/wifiphisher/roguehostapd'
AUTHOR = 'Anakin'

try:
    EXT_MODULE = buildcommon.get_extension_module()
    with buildcommon.nostdout():
        setup(
            name=NAME,
            packages=PACKAGES,
            package_dir=PACKAGE_DIR,
            package_data=PACKAGE_DATA,
            version=VERSION,
            description=DESCRIPTION,
            url=URL,
            author=AUTHOR,
            cmdclass={'build_ext': build_ext,
                      'install': install},
            ext_modules=EXT_MODULE
        )
except buildexception.SharedLibMissError as exobj:
    print ("[" + constants.RED + "!" + constants.WHITE + "] " +
           ("The development package for " + exobj.libname +
            " is missing. Please download it and restart the compilation."
            " Now if you want, you can provide the exact command for Debian-based systems."
            ' For example, "if you are on Debian-based system: \'apt-get install{}\'."'.format(
                "".join(" " + package for package in exobj.packages))))
    with buildcommon.nostdout():
        setup(
            name=NAME,
            packages=PACKAGES,
            package_dir=PACKAGE_DIR,
            package_data=PACKAGE_DATA,
            version=VERSION,
            description=DESCRIPTION,
            url=URL,
            author=AUTHOR,
        )
finally:
    shutil.rmtree('tmp')
