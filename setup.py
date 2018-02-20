"""
Module for setup hostapd shared library
"""

from distutils.core import setup
import roguehostapd.hostapd_constants as constants
import roguehostapd.buildutil.buildcommon as buildcommon

# define project information
NAME = 'roguehostapd'
PACKAGES = ['roguehostapd']
VERSION = '1.1.2'
DESCRIPTION = 'Hostapd wrapper for hostapd',
URL = 'https://github.com/wifiphisher/roguehostapd',
AUTHOR = 'Anakin',
EXT_MODULE = buildcommon.get_extension_module()

if EXT_MODULE:
    # hide the stdout of building process
    with buildcommon.nostdout():
        setup(
            name=NAME,
            packages=PACKAGES,
            version=VERSION,
            description=DESCRIPTION,
            url=URL,
            author=AUTHOR,
            ext_modules=EXT_MODULE
        )
# when the extension library build fail we still need to setup some of the pure python
# scripts so that wifiphisher can function well
else:
    print ("[" + constants.RED + "!" + constants.WHITE + "] " +
           " hostapd library build fail due to missing netlink/openssl libraries!")
    setup(
        name=NAME,
        packages=PACKAGES,
        version=VERSION,
        description=DESCRIPTION,
        url=URL,
        author=AUTHOR,
    )
