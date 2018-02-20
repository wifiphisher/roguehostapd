"""
Module defines the custom exceptions for building hostapd
"""


class SharedLibMissError(Exception):
    """
    Define the Netlink shared library missing exception
    """
    def __init__(self, libname, packages):
        """
        Initialize the NetlinkMissError object
        param self: A SharedLibMissError object
        param libname: Required library name
        param packages: The packages required by the lib
        type self: SharedLibMissError
        type libname: str
        type packages: list
        return: None
        rtype: None
        """
        super(SharedLibMissError, self).__init__(libname, packages)
        self.libname = libname
        self.packages = packages
