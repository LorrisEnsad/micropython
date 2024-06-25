# https://docs.micropython.org/en/latest/library/espnow.html

import select
import espnow
import network

ssid = 'domo'
pssw = 'th1Sp4((!'

sta_if = network.WLAN(network.STA_IF)
macaddress = sta_if.config('mac')

def do_connect():
    if not sta_if.isconnected():
        print('connecting to network...')
        sta_if.active(True)
        sta_if.connect(ssid, pssw)
        while not sta_if.isconnected():
            pass
    print('network config:', sta_if.ifconfig())

do_connect()


####### SENDER #######
# e = espnow.ESPNow()
# e.active(True)
# peer = b'\xbb\xbb\xbb\xbb\xbb\xbb'   # MAC address of peer's wifi interface
# e.add_peer(peer)      # Must add_peer() before send()

# e.send(peer, "Starting...")
# for i in range(100):
#     e.send(peer, str(i)*20, True)
# e.send(peer, b'end')

####### RECEIVER #######
# e = espnow.ESPNow()
# e.active(True)

# while True:
#     host, msg = e.recv()
#     if msg:             # msg == None if timeout in recv()
#         print(host, msg)
#         if msg == b'end':
#             break

####### CALLBACK #######
# def recv_cb(e):
#     while True:  # Read out all messages waiting in the buffer
#         mac, msg = e.irecv(0)  # Don't wait if no messages left
#         if mac is None:
#             return
#         print(mac, msg)
# e.irq(recv_cb)