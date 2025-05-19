import wifi_config
import machine

try:
    if not wifi_config.connect_to_saved_wifi():
        wifi_config.start_config_portal()

except Exception as e:
    print("Erreur lors de la tentative de connexion Wi-Fi:", e)
    wifi_config.start_config_portal()

