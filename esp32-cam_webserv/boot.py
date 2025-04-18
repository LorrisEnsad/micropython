import network
import time

# --- WiFi --- 
ssid = 'SSID_'
password = 'pass'

wlan = network.WLAN(network.STA_IF)
wlan.active(True)
wlan.connect(ssid, password)

print("Connexion au WiFi...")
while not wlan.isconnected():
    time.sleep(1)

print('Connecté ! IP:', wlan.ifconfig()[0])