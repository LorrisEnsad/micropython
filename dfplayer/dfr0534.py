from machine import UART
import time


class DFR0534 :
    def __init__(self, rx=20, tx=21) :
        self.uart1 = UART(1, baudrate=9600, tx=21, rx=20)
        self.ANSWER_WAIT_TIME = .02 # why .02 ?
        #print(self.is_playing())
    
    def is_playing(self) :
        commande = b'\xaa\x01\x00\xab'
        self.uart1.write(commande) #Envoie de la commande 
        time.sleep(self.ANSWER_WAIT_TIME) #Attente de la réponse
        answer = self.uart1.read()#Lecture de la réponse 
        
        if answer==b'\xaa\x01\x01\x00\xac' :
            return False
        else : #Remplacer par un elif, et rajouter un cas pour dire 'connexion non établie'
            return True
    
    def play(self):
        commande = b'\xaa\x02\x00\xac'
        self.uart1.write(commande)
    
    def pause(self) :
        commande = b'\xaa\x03\x00\xad'
        self.uart1.write(commande)

    def stop(self):
        commande = b'\xaa\x04\x00\xae'
        self.uart1.write(commande)

    def play_prev(self):
        commande = b'\xaa\x05\x00\xaf'
        self.uart1.write(commande)

    def play_next(self):
        commande = b'\xaa\x06\x00\xb0'
        self.uart1.write(commande)

    def play_track(self,track):
        #print('attempt of playing track', track)
        track = max(0,int(track))
        commande = b'\xaa\x07\x02\x00' + bytes([track, track + 0xb3])
        #print(commande)
        self.uart1.write(commande)
    
    # need x08→x12 >.<
    
    def set_volume(self, v) :
        v= int(v)
        v = min(30,max(0,v))
        commande = b'\xaa\x13\x01' + bytes([v, v + 0xbe])
        #print(commande)
        self.uart1.write(commande)

    def volume_up(self) :
        commande = b'\xaa\x14\x00\xbe'
        self.uart1.write(commande)
    
    def volume_down(self):
        commande = b'\xaa\x15\x00\xbf'
        self.uart1.write(commande)
    
#Sur le même modèle, le reste des commandes listées ici https://wiki.dfrobot.com/Voice_Module_SKU__DFR0534
#peuvent être implémentées.    