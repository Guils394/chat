#!/usr/bin/env python3

import socket
import threading

def recevoir(socket_chat, stop):
    
    socket_chat.settimeout(1.0)
    while not stop.is_set():
        try:
            request, hote = socket_chat.recvfrom(2048)
            message = request.decode("utf-8")
            print(f"{hote}: {message}")
        except socket.timeout:
            continue
        
    socket_chat.close()

def envoyer(socket_chat, adresse, stop):
    
           
    while not stop.is_set():
        message = input()
        envoi = message.encode("utf-8")
        if message.lower() == "quit":
            print("Fin de la connection ...")
            socket_chat.sendto(b'Machin a quitte la discution...', adresse)
            stop.set()
            break
        socket_chat.sendto(envoi, adresse)
  
        

# Main

adresse_ecoute = ('', 3000)
adresse_dest = ('localhost', 3001)
stop = threading.Event()

socket_chat = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
socket_chat.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
socket_chat.bind(adresse_ecoute)

thread_recep = threading.Thread(target=recevoir, args=(socket_chat, stop))
thread_recep.start()

thread_envoi = threading.Thread(target=envoyer, args=(socket_chat, adresse_dest, stop))
thread_envoi.start()

thread_envoi.join()
thread_recep.join()
