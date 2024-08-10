#!/usr/bin/env python3

import socket
import threading
import time

def recevoir(addresse, stop):
    socket_recep = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    socket_recep.bind(addresse)
    socket_recep.listen()
    client, infos = socket_recep.accept()
    hote = socket.gethostname()
    print("Connecte a ", hote)

    while not stop.is_set():
        request = client.recv(2048)
        message = request.decode("utf-8")
        if message.lower() == "quit":
            print(f"Connection terminee par {hote}")
            stop.set()
            break
        print(f"{hote}: {message}")
        
    client.close()
    socket_recep.close()

def envoyer(addresse, stop):
    socket_env = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    count = "."
    while True:
        try:
            socket_env.connect(addresse)
            break
        except:
            print("Connection en attente"+count)
            count = count + "."
            time.sleep(1)

    while not stop.is_set():
        message = input()
        envoi = message.encode("utf-8")
        socket_env.sendall(envoi)
        if message.lower() == "quit":
            print("Fin de la connection ...")
            stop.set()
            break
        
    socket_env.close()
    
        

# Main

adresse_ecoute = ('', 3000)
adresse_envoi = ('localhost', 3001)
stop = threading.Event()


thread_recep = threading.Thread(target=recevoir, args=(adresse_ecoute, stop))
thread_recep.start()

thread_envoi = threading.Thread(target=envoyer, args=(adresse_envoi, stop))
thread_envoi.start()

thread_envoi.join()
thread_recep.join()
