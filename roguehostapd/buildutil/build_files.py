"""
Module for defining the required hostapd macros and source files
"""
import os


# define directory macros
HOSTAPD_DIR = 'roguehostapd/hostapd-2_6'
HOSTAPD_SRC = os.path.join(HOSTAPD_DIR, 'src')
HOSTAPD_MAIN = os.path.join(HOSTAPD_DIR, 'hostapd')
HOSTAPD_AP = os.path.join(HOSTAPD_SRC, 'ap')
HOSTAPD_UTILS = os.path.join(HOSTAPD_SRC, 'utils')
HOSTAPD_WPS = os.path.join(HOSTAPD_SRC, 'wps')
HOSTAPD_DRVS = os.path.join(HOSTAPD_SRC, 'drivers')
HOSTAPD_COMMON = os.path.join(HOSTAPD_SRC, 'common')
HOSTAPD_L2_PACKET = os.path.join(HOSTAPD_SRC, 'l2_packet')
HOSTAPD_EAPOL_AUTH = os.path.join(HOSTAPD_SRC, 'eapol_auth')
HOSTAPD_RADIUS = os.path.join(HOSTAPD_SRC, 'radius')
HOSTAPD_EAP_SERVER = os.path.join(HOSTAPD_SRC, 'eap_server')
HOSTAPD_EAP_COMMON = os.path.join(HOSTAPD_SRC, 'eap_common')
HOSTAPD_CRYPTO = os.path.join(HOSTAPD_SRC, 'crypto')
SHARED_LIB_PATH = os.path.join(HOSTAPD_MAIN, 'libhostapd')
LIB_NL3_PATH = '/usr/include/libnl3'
LIB_SSL_PATH = '/usr/include/openssl'

# files under hostapd-2.6/hostapd
MAIN_FILES = ['main.c', 'config_file.c', 'eap_register.c', 'ctrl_iface.c']
# files under hostapd-2.6/src/l2_packet
L2_PACKET_FILES = ['l2_packet_linux.c']
# files under hostapd-2.6/src/ap
AP_FILES = ['hostapd.c',
            'wpa_auth_glue.c',
            'ap_list.c',
            'dfs.c',
            'ap_drv_ops.c',
            'utils.c',
            'authsrv.c',
            'ieee802_1x.c',
            'ap_config.c',
            'eap_user_db.c',
            'ieee802_11_auth.c',
            'ieee802_11.c',
            'sta_info.c',
            'wpa_auth.c',
            'tkip_countermeasures.c',
            'ap_mlme.c',
            'wpa_auth_ie.c',
            'preauth_auth.c',
            'pmksa_cache_auth.c',
            'ieee802_11_shared.c',
            'beacon.c',
            'accounting.c',
            'bss_load.c',
            'rrm.c',
            'drv_callbacks.c',
            'neighbor_db.c',
            'ieee802_11_ht.c',
            'ctrl_iface_ap.c',
            'hw_features.c',
            'wmm.c',
            'karma_handlers.c',
            'wps_hostapd.c']
# files under hostapd-2.6/src/common
COMMON_FILES = ['hw_features_common.c',
                'ctrl_iface_common.c',
                'ieee802_11_common.c',
                'wpa_common.c']
# files under hostapd-2.6/src/drivers
DRV_FILES = ['drivers.c',
             'driver_common.c',
             'driver_wired.c',
             'driver_nl80211.c',
             'driver_nl80211_capa.c',
             'driver_nl80211_event.c',
             'driver_nl80211_monitor.c',
             'driver_nl80211_scan.c',
             'driver_hostap.c',
             'netlink.c',
             'linux_ioctl.c',
             'rfkill.c']
# files under hostapd-2.6/src/utils
UTIL_FILES = ['eloop.c',
              'common.c',
              'os_unix.c',
              'ip_addr.c',
              'wpabuf.c',
              'wpa_debug.c',
              'radiotap.c',
              'base64.c',
              'uuid.c']
# files under hostapd-2.6/src/eapol_auth
EAPOL_AUTH_FILES = ['eapol_auth_sm.c', 'eapol_auth_dump.c']
# files under hostapd-2.6/src/radius
RADIUS_FILES = ['radius.c', 'radius_client.c', 'radius_das.c']
# files under hostapd-2.6/src/eap_server
EAP_SERVER_FILES = ['eap_server_md5.c',
                    'eap_server_tls.c',
                    'eap_server_peap.c',
                    'eap_server_ttls.c',
                    'eap_server_mschapv2.c',
                    'eap_server_gtc.c',
                    'eap_server.c',
                    'eap_server_tls_common.c',
                    'eap_server_methods.c',
                    'eap_server_identity.c',
                    'eap_server_wsc.c']
# files under hostapd-2.6/src/eap_common
EAP_COMMON_FILES = ['eap_peap_common.c',
                    'eap_common.c',
                    'chap.c',
                    'eap_wsc_common.c']
# files under hostapd-2.6/src/crypto
CRYPTO_FILES = ['ms_funcs.c',
                'tls_openssl.c',
                'crypto_openssl.c',
                'sha1-prf.c',
                'sha256-prf.c',
                'sha256-kdf.c',
                'sha256-tlsprf.c',
                'random.c']
# files under hostapd-2.6/src/wps
WPS_FILES = ['wps.c',
             'wps_common.c',
             'wps_attr_parse.c',
             'wps_attr_build.c',
             'wps_attr_process.c',
             'wps_dev_attr.c',
             'wps_enrollee.c',
             'wps_registrar.c',
             'wps_upnp.c',
             'wps_upnp_ssdp.c',
             'wps_upnp_event.c',
             'upnp_xml.c',
             'wps_upnp_web.c',
             'http_server.c',
             'http_client.c',
             'httpread.c',
             'wps_upnp_ap.c']
# required hostapd macros
HOSTAPD_MACROS = [('HOSTAPD', '1'),
                  ('CONFIG_NO_VLAN', '1'),
                  ('CONFIG_CTRL_IFACE', '1'),
                  ('CONFIG_CTRL_IFACE_UNIX', '1'),
                  ('EAP_SERVER_MD5', '1'),
                  ('EAP_SERVER_TLS', '1'),
                  ('EAP_SERVER_PEAP', '1'),
                  ('EAP_SERVER_TTLS', '1'),
                  ('EAP_SERVER_MSCHAPV2', '1'),
                  ('EAP_SERVER_WSC', '1'),
                  ('EAP_SERVER_IDENTITY', '1'),
                  ('EAP_SERVER', '1'),
                  ('PKCS12_FUNCS', '1'),
                  ('CONFIG_SHA256', '1'),
                  ('CONFIG_DRIVER_WIRED', '1'),
                  ('CONFIG_LIBNL20', '1'),
                  ('CONFIG_DRIVER_HOSTAP', '1'),
                  ('CONFIG_KARMA_ATTACK', '1'),
                  ('CONFIG_WIFIPHISHER_COMMON', '1'),
                  ('CONFIG_DRIVER_HOSTAP', '1'),
                  ('CONFIG_DRIVER_NL80211', '1'),
                  ('CONFIG_LIBNL32', '1'),
                  ('CONFIG_EAP', '1'),
                  ('CONFIG_ERP', '1'),
                  ('CONFIG_EAP_MD5', '1'),
                  ('CONFIG_EAP_TLS', '1'),
                  ('CONFIG_EAP_MSCHAPV2', '1'),
                  ('CONFIG_EAP_PEAP', '1'),
                  ('CONFIG_EAP_GTC', '1'),
                  ('CONFIG_EAP_TTLS', '1'),
                  ('CONFIG_WPS', '1'),
                  ('CONFIG_WPS_UPNP', '1'),
                  ('CONFIG_PKCS12', '1'),
                  ('CONFIG_IPV6', '1'),
                  ('CONFIG_IEEE80211N', '1'),
                  ('NEED_AP_MLME', '1')]


def get_file_list(directory, file_list):
    """
    Get the paths of required source files under specific directory
    :param directory: Directory of the require files
    :param file_list: Required files
    :type directory: str
    :param file_list: list
    :return: A file path list for the specific directory
    :rtype: list
    """
    return [os.path.join(directory, filename) for filename in file_list]


def get_all_source_files():
    """
    Get all the source files for building the shared library
    :return: A list of source files
    :rtype: list
    """

    ret_files = []
    ret_files.extend(get_file_list(HOSTAPD_MAIN, MAIN_FILES))
    ret_files.extend(get_file_list(HOSTAPD_L2_PACKET, L2_PACKET_FILES))
    ret_files.extend(get_file_list(HOSTAPD_AP, AP_FILES))
    ret_files.extend(get_file_list(HOSTAPD_COMMON, COMMON_FILES))
    ret_files.extend(get_file_list(HOSTAPD_DRVS, DRV_FILES))
    ret_files.extend(get_file_list(HOSTAPD_UTILS, UTIL_FILES))
    ret_files.extend(get_file_list(HOSTAPD_EAPOL_AUTH, EAPOL_AUTH_FILES))
    ret_files.extend(get_file_list(HOSTAPD_RADIUS, RADIUS_FILES))
    ret_files.extend(get_file_list(HOSTAPD_EAP_SERVER, EAP_SERVER_FILES))
    ret_files.extend(get_file_list(HOSTAPD_EAP_COMMON, EAP_COMMON_FILES))
    ret_files.extend(get_file_list(HOSTAPD_CRYPTO, CRYPTO_FILES))
    ret_files.extend(get_file_list(HOSTAPD_WPS, WPS_FILES))
    return ret_files
