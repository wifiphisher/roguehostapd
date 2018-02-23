"""
Module defines the utility functions used in roguehostapd
"""

import contextlib
import io
import os
import sys
import shutil
from textwrap import dedent
import tempfile
import distutils.sysconfig
import distutils.ccompiler
try:
    from setuptools import Extension
except ImportError:
    from distutils.core import Extension
from distutils.errors import CompileError, LinkError
import roguehostapd.buildutil.build_files as build_files
import roguehostapd.buildutil.buildexception as buildexception


# code for checking if libnl-dev and libnl-genl-dev exist
LIBNL_CODE = dedent("""
#include <netlink/netlink.h>
#include <netlink/genl/genl.h>
int main(int argc, char* argv[])
{
   struct nl_msg *testmsg;
   testmsg = nlmsg_alloc();
   nlmsg_free(testmsg);
   return 0;
}
""")

# code for checking if openssl library exist
OPENSSL_CODE = dedent("""
#include <openssl/ssl.h>
#include <openssl/err.h>
int main(int argc, char* argv[])
{
    SSL_load_error_strings();
    return 0;
}
""")

LIBNAME_CODE_DICT = {
    "netlink": LIBNL_CODE,
    "openssl": OPENSSL_CODE
}

@contextlib.contextmanager
def nostdout():
    """
    Hide the stdout in the specific context

    :return: None
    :rtype: None
    """
    save_stdout = sys.stdout
    sys.stdout = io.BytesIO()
    yield
    sys.stdout = save_stdout

def check_required_library(libname, libraries=None, include_dir=None):
    """
    Check if the required shared library exists

    :param libname: The name of shared library
    :type libname: str
    :return True if the required shared lib exists else false
    :rtype: bool
    """
    build_success = True
    tmp_dir = tempfile.mkdtemp(prefix='tmp_' + libname + '_')
    bin_file_name = os.path.join(tmp_dir, 'test_' + libname)
    file_name = bin_file_name + '.c'
    with open(file_name, 'w') as filep:
        filep.write(LIBNAME_CODE_DICT[libname])
    compiler = distutils.ccompiler.new_compiler()
    distutils.sysconfig.customize_compiler(compiler)
    try:
        compiler.link_executable(
            compiler.compile([file_name],
                             include_dirs=include_dir),
            bin_file_name,
            libraries=libraries,
        )
    except CompileError:
        build_success = False
    except LinkError:
        build_success = False
    finally:
        shutil.rmtree(tmp_dir)
    if build_success:
        return True
    return False

def get_extension_module():
    """
    Get hostapd extension module
    :return: list of extension for hostapd
    :rtype: list of Extension if build success
    ..note: if the required shared library is missing this function will
    raise the custom exception: SharedLibMissError
    """

    if not check_required_library("netlink", ["nl-3", "nl-genl-3"],
                                  [build_files.LIB_NL3_PATH]):
        raise buildexception.SharedLibMissError('netlink', ['libnl-3-dev',
                                                            'libnl-genl-3-dev'])
    if not check_required_library("openssl", ["ssl"],
                                  [build_files.LIB_SSL_PATH]):
        raise buildexception.SharedLibMissError("openssl", ['libssl-dev'])

    # required shared libraries exist
    ext_module = Extension(build_files.SHARED_LIB_PATH,
                           define_macros=build_files.HOSTAPD_MACROS,
                           libraries=['rt', 'ssl', 'crypto', 'nl-3', 'nl-genl-3'],
                           sources=build_files.get_all_source_files(),
                           include_dirs=[build_files.HOSTAPD_SRC,
                                         build_files.HOSTAPD_UTILS,
                                         build_files.LIB_NL3_PATH])
    return [ext_module]


if __name__ == "__main__":
    check_required_library("netlink", ["nl-3", "nl-genl-3"],
                           [build_files.LIB_NL3_PATH])
    check_required_library("openssl", ["ssl"],
                           [build_files.LIB_SSL_PATH])
