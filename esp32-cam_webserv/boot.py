import network
import time

# --- WiFi ---
ssid = 'TON_SSID'
password = 'TON_MOT_DE_PASSE'

wlan = network.WLAN(network.STA_IF)
wlan.active(True)
wlan.connect(ssid, password)

print("Connexion au WiFi...")
while not wlan.isconnected():
    time.sleep(1)

print('Connecté ! IP:', wlan.ifconfig()[0])