"""
Example for lunching the TKIP Access Point
"""
from roguehostapd import hostapd_controller

if __name__ == "__main__":
    HOSTAPD_CONFIG = {
        'ssid' : 'test',
        'interface': 'wlan12',
        'wpa': '1',
        'wpa_passphrase': '12345678',
    }
    HOSTAPD_OBJ = hostapd_controller.Hostapd()
    HOSTAPD_OBJ.start(HOSTAPD_CONFIG, {})
