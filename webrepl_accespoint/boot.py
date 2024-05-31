import time
import network
import webrepl
webrepl.start()

ssid = 'TRY'
password = 'try-pass'
ap = network.WLAN(network.AP_IF);
ap.active(True);
ap.config(essid=ssid,authmode=network.AUTH_WPA_WPA2_PSK, password=password)
print(ap.ifconfig())
