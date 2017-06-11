# roguehostapd
Roguehostapd is a fork of hostapd, the famous user space software access point. It provides Python ctypes bindings and a number of additional attack features. It was primarily developed for use in the Wifiphisher project.

## Build

To build the latest development version type the following commands:
```bash
git clone https://github.com/wifiphisher/hostapd_binder.git # Download the latest version
cd hostapd_binder # Switch to the hostapd_binder directory
python setup.py build # Build the shared library of hostapd
```
## Usage

***

```shell
python run.py -i wlan0 -ssid haha
```

Use wlan0 for spawning the OPEN rogue AP on channel 6 and the ssid is haha.

***

```shell
python run.py -i wlan0 -ssid haha -pK 12345678
```

Use wlan0 for spawning the WPA2/WPA rogue AP with passhrase 12345678

***

```shell
python run.py -i wlan0 -ssid haha -kA
```

Use wlan0 for spawning the OPEN rogue AP supporting the KARMA attack.

***

```python
HOSTAPD_CONFIG_DICT = {
    'ssid': 'haha',
    'interface': 'wlan0',
    'karma_enable': 1}
HOSTAPD_OPTION_DICT = {
    'debug_level': hostapd_constants.HOSTAPD_DEBUG_OFF
}
HOSTAPD_OBJ = Hostapd()
HOSTAPD_OBJ.start(HOSTAPD_CONFIG_DICT, HOSTAPD_OPTION_DICT)
```

The above configuration will perform the KARMA attack.

Following are all the options along with their descriptions (also available with `python run.py -h`)


| Short form | Long form | Explanation |
| :----------: | :---------: | :-----------: |
|-h | --help| show this help message and exit |
|-ssid SSID| --ssid SSID| Select the ssid for the spawn rogue AP|
|-c CHANNEL| --channel CHANNEL| Select the channel number for the spawn rogue AP|
|-bI BEACON_INT| --beacon_int BEACON_INT| Define the beacon interval in milliseconds for the spawn rogue AP|
|-i INTERFACE| --interface INTERFACE| Select the interface for the spawn rogue AP. Example: -i wlan0|
|-pK WPA_PASSPHRASE| --wpa_passphrase WPA_PASSPHRASE| Define the password for the spawn rogue AP.|
|-kA|| Enabling the KARMA attack|
|-d {0, 1, 2}|--debug_level {0, 1, 2}| Enabling the verbose debug log: --0 disable all the log --1 enable the debug log, --2 enable verbose debug log|
|-K|--key_data|Include key data in debug messages|
|-t|--timestamp|Include timestamps in some debug messages|
|-v|--version|Show hostapd version|
