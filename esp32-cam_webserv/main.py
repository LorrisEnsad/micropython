# http://192.168.x.x/photo pour voir la photo
# curl http://192.168.x.x/photo -o image.jpg


import socket
import esp32
import esp32.camera

# --- Initialisation de la caméra ---
esp32.camera.init(0, format=esp32.camera.JPEG)

# --- Fonction pour capturer une image ---
def take_pic():
    buf = esp32.camera.capture()
    return buf  # bytes JPEG

# --- Serveur HTTP ---
addr = socket.getaddrinfo('0.0.0.0', 80)[0][-1]
s = socket.socket()
s.bind(addr)
s.listen(1)

print('Serveur en attente de requêtes...')

while True:
    cl, addr = s.accept()
    print('Client : ', addr)
    request = cl.recv(1024)
    request = str(request)

    if 'GET /photo' in request:
        img = take_pic()
        cl.send('HTTP/1.1 200 OK\r\nContent-Type: image/jpeg\r\n\r\n')
        cl.send(img)
    else:
        cl.send('HTTP/1.1 200 OK\r\nContent-Type: text/html\r\n\r\n')
        cl.send('Utilisez /photo pour prendre une photo')

    cl.close()
