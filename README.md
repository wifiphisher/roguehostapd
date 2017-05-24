# hostapd_binder
Hostapd Python wrapper to simplify usage of hostapd

-- Build the hostapd shared library

    python setup.py build

-- Run the hostapd as following

    a. OPEN AP:
        ./run.py -i wlan0 -ssid haha

    b. WPA/RSN AP:
        ./run.py -i wlan0 -ssid haha -pK 12345678

