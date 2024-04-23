import network
import time


if __name__=="__main__":
    wlan = network.WLAN(network.STA_IF)
    wlan.active(True)

    if wlan.isconnected():
        wlan.disconnect()

    print("[*] Start Wi-Fi Scan ...")

    authmodes = ['Open', 'WEP', 'WPA-PSK','WPA2-PSK4', 'WPA/WPA2-PSK', 'Other']
    for (ssid, bssid, channel, RSSI, authmode, hidden) in wlan.scan():
        print("* {:s}".format(ssid))
        print(authmodes[authmode])
        print("   - Auth: {} {}".format(authmodes[authmode], '(hidden)' if hidden else ''))
        print("   - Channel: {}".format(channel))
        print("   - RSSI: {}".format(RSSI))
        print("   - BSSID: {:02x}:{:02x}:{:02x}:{:02x}:{:02x}:{:02x}".format(*bssid))
        print()