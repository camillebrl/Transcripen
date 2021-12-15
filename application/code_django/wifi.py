import os
import socket
import time

#IP =socket.gethostbyname(socket.gethostname())
IP = '192.168.43.65'
PORT = 4455
ADDR = (IP,PORT)
#FORMAT = "utf-8"
SIZE = 1024

def main():
    print("[STARTING] Server is starting")
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    server.bind(ADDR)
    server.listen()
    print ("[LISTENING] Server is listening")


    conn, addr = server.accept()
    print("[NEW CONNECTION]" + str(addr) + " connected.")
        
    for filename in os.listdir("audio_folder"):
        file = os.path.join("audio_folder", filename)
        with open(file, 'rb') as f:
            for l in f: conn.sendall(l)
        os.remove(file)
    print("[RECV] File sended")

    conn.close()
    print("[DISCONNECTED] Connection closed")
        
    server.close()

if __name__ =="__main__":
    while(True):
        main()
        time.sleep(30)
