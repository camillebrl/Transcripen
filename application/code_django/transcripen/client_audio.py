import socket
from datetime import datetime

#IP =socket.gethostbyname(socket.gethostname())
IP = '192.168.43.65'
PORT = 4455
ADDR = (IP,PORT)
#FORMAT = "utf-8"
SIZE = 1024

def start_client_transmission():
    print("[STARTING] Client is starting")
    client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client.connect(ADDR)
    print ("[LISTENING] Client is connected")


    WAVE_OUTPUT_FILENAME = datetime.now().strftime("../../../audio_received/%d%b%Y_%Hh%Mmin.wav")
    print(WAVE_OUTPUT_FILENAME)
    with open(WAVE_OUTPUT_FILENAME,'wb') as f:
        while True:
            l = client.recv(SIZE)
            if not l : break
            f.write(l) 
    print("[RECV] File received")

    client.close()
    print("[DISCONNECTED] Connection closed")
   

if __name__ =="__main__":
    start_client_transmission()
        
