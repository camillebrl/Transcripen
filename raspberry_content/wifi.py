########################################################################################################################
########################################################################################################################
########################################################################################################################
# Cet algorithme permet d'envoyer les audios enregistrés dans la Raspberry à l'application
########################################################################################################################
########################################################################################################################
########################################################################################################################


import os
import socket
import time

#IP =socket.gethostbyname(socket.gethostname())
IP = '192.168.43.65' # On doit indiquer l'IP de la raspberry sur le réseau en question. On aurait pu mettre socket.gethostbyname(socket.gethostname()), mais on avait un IP défini pour la démo, donc on l'a laissé
PORT = 4455 # port associé à l'adresse IP
ADDR = (IP, PORT)

def main():
    print("[STARTING] Server is starting")
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    server.bind(ADDR)
    server.listen()
    print ("[LISTENING] Server is listening")
    conn, addr = server.accept() # attente d'acceptation de la connection via l'application : pas de timeout, reste à cette étape tant que l'utilisateur n'a pas cliqué sur "récupérer les fichiers audio"
    print("[NEW CONNECTION]" + str(addr) + " connected.")
    for filename in os.listdir("audio_folder"): # On itère sur les fichiers dans audio_folder de la raspberry
        file = os.path.join("audio_folder", filename) # pour avoir le nom total du fichier (de son path) sur la raspberry
        with open(file, 'rb') as f:
            for l in f: conn.sendall(l) # envoie tout le fichier (envoie jusqu'à ce que l'intégralité du fichier soit envoyée. Si tout n'est pas envoyé, erreur.)
        os.remove(file) # Une fois le fichier envoyé, on le supprime de la raspberry
    print("[RECV] File sended")
    conn.close() # Il faut fermer la connection, sinon on ne pourra pas la rappeler
    print("[DISCONNECTED] Connection closed")
    server.close() # il faut également arrêter le serveur pour pouvoir le re-appeler

if __name__ =="__main__":
    while(True):
        main()
        time.sleep(30) # une fois qu'on a envoyé les fichiers de la raspberry, on attend 30 secondes avant de renouveler le processus (connection au serveur, recherche d'acceptation, etc.)
