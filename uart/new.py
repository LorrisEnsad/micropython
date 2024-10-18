from machine import UART, Pin
import time

# Configuration
last_channels = None
THRESHOLD = 500
BUFFER_SIZE = 64

# Dictionnaire pour nommer les canaux
CHANNEL_NAMES = {
    0: "Throttle",
    1: "Roll",
    2: "Pitch",
    3: "Yaw",
    4: "Aux1",
    5: "Aux2",
    6: "Aux3",
    7: "Aux4",
    8: "Aux5",
    9: "Aux6",
    10: "Aux7",
    11: "Aux8",
    12: "Aux9",
    13: "Aux10",
    14: "Aux11",
    15: "Aux12"
}

def decode_crsf_channels(payload):
    if len(payload) < 22:
        return None
    try:
        channels = []
        # CRSF est codé en little-endian, donc on traite les données par petits morceaux
        for i in range(16):
            # Chaque canal est codé sur 11 bits, répartis sur plusieurs octets
            byte_index = i * 11 // 8
            bit_offset = i * 11 % 8

            # Extraire les 11 bits du canal
            channel_value = (payload[byte_index] | (payload[byte_index + 1] << 8)) >> bit_offset
            channel_value &= 0x7FF  # Garder seulement les 11 bits

            # Mise à l'échelle des valeurs des canaux
            scaled_value = 1000 + (channel_value * 1000 // 0x7FF)
            channels.append(scaled_value)
        
        return channels
    except:
        return None

def print_all_channels(current_channels):
    global last_channels
    
    if last_channels is None:
        last_channels = current_channels.copy()
        return
    
    # Vérifie si au moins un canal a changé significativement
    changes_detected = False
    for i, (current, last) in enumerate(zip(current_channels, last_channels)):
        if abs(current - last) > THRESHOLD:
            changes_detected = True
            last_channels[i] = current
    
    # Si changement détecté, affiche tous les canaux
    if changes_detected:
        print("\033[2J\033[H")  # Efface l'écran et repositionne le curseur
        print("─"*50)
        for i, value in enumerate(current_channels):
            channel_name = CHANNEL_NAMES.get(i, f"Canal{i}")
            print(f"{channel_name:8}: {value:4}")
        print("─" * 50)

# Configuration UART
uart = UART(1, baudrate=420000, tx=Pin(21), rx=Pin(20), 
           bits=8, parity=None, stop=1, timeout=100)

last_print_time = 0
PRINT_INTERVAL = 100  # ms

while True:
    if uart.any():
        try:
            data = uart.read(BUFFER_SIZE)
            if data:
                channels = decode_crsf_channels(data)
                if channels:
                    current_time = time.ticks_ms()
                    if time.ticks_diff(current_time, last_print_time) > PRINT_INTERVAL:
                        print_all_channels(channels)
                        last_print_time = current_time
        except Exception as e:
            uart.flush()
    time.sleep_ms(1)