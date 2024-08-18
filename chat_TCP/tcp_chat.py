#!/usr/bin/env python3

import socket
import threading
import time
import sys, re, json
#test

# Fonctions

# Thread reception avec ouverture socket TCP
def recevoir(addresse, stop):
    socket_recep = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    socket_recep.bind(addresse)
    socket_recep.listen()
    client, infos = socket_recep.accept()
    print("\nConnecte a ", infos[0])

    # Recepetion d'un message en json
    while not stop.is_set():
        try:
            request = client.recv(2048)
            recept_json = request.decode("utf-8")
            recept = json.loads(recept_json)
            pseudo = recept.get("pseudo")
            message = recept.get("message")
            if message.lower() == "quit":
                print(f"Connection terminee par {infos[0]}:{pseudo}")
                stop.set()
                break
            print(f"{pseudo}: {message}")
        except Exception as e:
            print(f"Erreur fatale dans le socket de reception: {e}")
            stop.set()
            break
        
    client.close()
    socket_recep.close()


# Thread envoi, ouverture socket TCP
def envoyer(addresse, pseudo, stop):
    
    socket_env = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    count = "."
    # Attente de l'hote
    while True:
        try:
            socket_env.connect(addresse)
            break
        except ConnectionRefusedError:
            print("Connection en attente"+count, end='\r')
            count = count + "."
            time.sleep(1)
        except Exception as e:
            print(f"Erreur fatale de connection: {e}")
            stop.set()
            break

            # Envoi d'un message en json format pseudo message
    while not stop.is_set():
        try:
            message = input()
            message_json = json.dumps({'pseudo':pseudo, 'message':message})
            envoi = message_json.encode("utf-8")
            
            if message.lower() == "quit":
                print("Fin de la connection ...")
                socket_env.sendall(envoi)
                stop.set()
                break
            socket_env.sendall(envoi)
        except Exception as e:
            print(f"Erreur fatale dans le thread d' envoi: {e}")
            stop.set()
            break
    socket_env.close()
    
        

# Main

def chat():
        # prise en compte des arguments:
    if len(sys.argv) < 2:
        adresse_destinataire = input("Entrez l'ip du destinataire: ")
    else:
        adresse_destinataire = sys.argv[1]
    
    # verification de l'adresse fournie
    regex = r'^((25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)\.){3}(25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)$'
    
    while not re.match(regex, adresse_destinataire):
            print("Ce n'est pas une adresse IPv4.\n")
            adresse_destinataire = input("Entrez l'ip du destinataire: ")

    pseudo = ""
    regex = r'^[a-zA-Z0-9]+$'
    while not re.match(regex, pseudo):
        pseudo = input("Entrez votre pseudo (pas de caractere special): ")
    

    # definition des tuples
    adresse_ecoute = ('', 3000)
    adresse_dest = (adresse_destinataire, 3000)
    
       
    stop = threading.Event()

    thread_recep = threading.Thread(target=recevoir, args=(adresse_ecoute, stop))
    thread_recep.start()

    thread_envoi = threading.Thread(target=envoyer, args=(adresse_dest, pseudo, stop))
    thread_envoi.start()

    thread_envoi.join()
    thread_recep.join()

if __name__ == "__main__":
    chat()