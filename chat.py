#!/usr/bin/env python3

import socket
import threading
import sys
import re

# Fonction de reception
def recevoir(socket_chat, stop):
    
    # Timout de la socket pour verification de l'etat de stop
    socket_chat.settimeout(1.0)
    while not stop.is_set():
        try:
            request, hote = socket_chat.recvfrom(2048)
            message = request.decode("utf-8")
            print(f"{hote}: {message}")
        except socket.timeout:
            continue
        except Exception as e:
            print(f"Erreur fatale dans le Thread de reception: {e}")
            stop.set()
            break
        
    socket_chat.close()

# fonction d'envoi
def envoyer(socket_chat, adresse, stop):

    while not stop.is_set():
        try:
            message = input()
            envoi = message.encode("utf-8")
            if message.lower() == "quit":
                print("Fin de la connection ...")
                socket_chat.sendto(b'Machin a quitte la discution...', adresse)
                stop.set()
                break
            socket_chat.sendto(envoi, adresse)
        except Exception as e:
            print(f"Erreur fatale dans le Thread de reception: {e}")
            stop.set()
            break
  
        
# Main
def chat():

    # prise en compte des arguments:
    if len(sys.argv) < 2:
        adresse_destinataire = input("Entrez l'ip du destinataire: ")
    else:
        adresse_destinataire = sys.argv[1]
    
    # verification de l'adresse fournie
    ip_regex = r'\b((25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)\.){3}(25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)\b'
    while True:
        if re.match(adresse_destinataire, ip_regex):
            break
        else:
            print("Ce n'est pas une adresse IPv4.\n")
            adresse_destinataire = input("Entrez l'ip du destinataire: ")

    # definition des tuples
    adresse_ecoute = ('', 3000)
    adresse_dest = (adresse_destinataire, 3000)
    
    # Ouverture du socket
    socket_chat = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    socket_chat.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    socket_chat.bind(adresse_ecoute)
    
    # Threads :
    # definition de l'evenement d'arret
    stop = threading.Event()

    # Thread de reception
    thread_recep = threading.Thread(target=recevoir, args=(socket_chat, stop))
    thread_recep.start()

    # Thread d'envoi
    thread_envoi = threading.Thread(target=envoyer, args=(socket_chat, adresse_dest, stop))
    thread_envoi.start()

    thread_envoi.join()
    thread_recep.join()

if __name__ == "__main__":
    chat()
