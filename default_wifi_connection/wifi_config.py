import network
import ujson
import time
import socket
import ubinascii
import machine

CONFIG_FILE = "wifi_config.json"

def url_decode(s):
    res = ""
    i = 0
    while i < len(s):
        c = s[i]
        if c == '+':
            res += ' '
        elif c == '%' and i + 2 < len(s):
            hex_val = s[i+1:i+3]
            try:
                res += chr(int(hex_val, 16))
                i += 2
            except:
                res += '%'
        else:
            res += c
        i += 1
    return res

def connect_to_saved_wifi():
    try:
        with open(CONFIG_FILE, 'r') as f:
            config = ujson.load(f)
        ssid = config["ssid"]
        password = config["password"]
    except:
        return False

    sta_if = network.WLAN(network.STA_IF)
    sta_if.active(True)
    sta_if.connect(ssid, password)

    for _ in range(20):  # wait up to ~10s
        if sta_if.isconnected():
            print("Connecté à", ssid)
            print(sta_if.ifconfig())
            return True
        time.sleep(0.5)
    return False


def start_config_portal():
    ap = network.WLAN(network.AP_IF)
    ap.active(True)
    ap.config(essid="ESP32_Config", password="12345678")
    print("Point d'accès actif:", ap.ifconfig())

    addr = socket.getaddrinfo('0.0.0.0', 80)[0][-1]
    s = socket.socket()
    s.bind(addr)
    s.listen(1)

    print("Serveur Web actif")

    while True:
        cl, addr = s.accept()
        request = cl.recv(1024).decode()
        if "ssid=" in request and "password=" in request:

            raw_ssid = request.split("ssid=")[1].split("&")[0]
            raw_password = request.split("password=")[1].split(" ")[0]
            ssid = url_decode(raw_ssid)
            password = url_decode(raw_password)

            with open(CONFIG_FILE, 'w') as f:
                ujson.dump({"ssid": ssid, "password": password}, f)

            response = """<html><meta charset="UTF-8"><body><h1>Reboot...</h1></body></html>"""
            cl.send("HTTP/1.0 200 OK\r\nContent-type: text/html\r\n\r\n")
            cl.send(response)
            cl.close()
            time.sleep(3)
            s.close()
            time.sleep(1)
            machine.reset()
            return

        else:
            sta_if = network.WLAN(network.STA_IF)
            sta_if.active(True)
            networks = sta_if.scan()

            ssid_options = ""
            for net in networks:
                ssid_str = net[0].decode('utf-8')
                ssid_options += f"<option value='{ssid_str}'>{ssid_str}</option>"

            # HTML
            html = f"""
                <html>
                    <head>
                        <meta charset="UTF-8">
                        <title>Config WiFi</title>
                        <script>
                            function togglePassword() {{
                                var pwdField = document.getElementById("password");
                                var toggleText = document.getElementById("toggleText");
                                if (pwdField.type === "password") {{
                                    pwdField.type = "text";
                                    toggleText.innerText = "masquer";
                                }} else {{
                                    pwdField.type = "password";
                                    toggleText.innerText = "afficher";
                                }}
                            }}
                        </script>
                    </head>
                    <body>
                        <h1>Configurer le WiFi</h1>
                        <form>
                            SSID : 
                            <select name='ssid'>
                                {ssid_options}
                            </select><br><br>
                            Mot de passe : 
                            <input name='password' id='password' type='password'>
                            <button type="button" onclick="togglePassword()" style="border:none;background:none;color:blue;cursor:pointer;">
                                <span id="toggleText">afficher</span>
                            </button>
                            <br><br>
                            <input type='submit' value='Se connecter'>
                        </form>
                    </body>
                </html>
                """
            cl.send("HTTP/1.0 200 OK\r\nContent-type: text/html\r\n\r\n")
            cl.send(html)
            cl.close()