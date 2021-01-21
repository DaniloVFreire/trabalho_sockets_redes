import threading
import socket

server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.bind(('127.0.0.1', 55555))
server.listen()

clients = []
nicknames = []
jogadores = []
palavra = ""
display = ""
tentativas = 5

def broadcast(message):
    for client in clients:
        client.send(message)

def remover(message, client):
    index = clients.index(client)
    clients.remove(client)
    client.close()
    nickname = nicknames[index]
    print(f'{nickname} left the chat!')
    broadcast(f'{nickname} left the chat!'.encode())
    nicknames.remove(nickname)
    return

def forca():
    jogadores[0].send("Escolha a palavra para a forca:")
    palavra = jogadores[0].recv(1024).decode()
    for i in palavra:
        display.append("_")
    jogadores[0:1].send("_____\n|    |\n|    0\n|   /|\\n|   / \\n|\n|_")
    pass

def comandos(message, client, nickname):
    print(message.decode())
    if (message.decode().lower()).find(";;") != -1:
        
        if (message.decode().lower()).find("help") != -1:
            client.send("\n-Os comandos existentes são:\n-;;help para listar os comandos\n;;forca para o jogo da forca\n;;sair para sair\n".encode())
        
        elif (message.decode().lower()).find("sair") != -1:
            client.send("você será desconectado em instantes".encode())
            client.send("qweirpuyaskdljfhqowieury128907346562087364lasdjkhfgeoirqwyfbv34296234592fbuefv3475".encode())
            remover(message, client)
        
        elif(message.decode().lower()).find("forca") != -1:
            broadcast(f"{nickname} começou um jogo da forca para participar digite ;;participar")
            #threading.thread(target = forca, )
            jogadores.append(client)
        
        elif(message.decode().lower()).find("participar") != -1:
            if(jogadores.count() <= 2):
                jogadores.append(client)
                broadcast("Sala completa, jogo começando".encode())
                forca()
            else:
                broadcast("Sala cheia, tente novamente mais tarde")
    else:
        broadcast(message)
    return


def handle(client,nickname):
    while True:
        try:
            message = client.recv(1024)
            comandos(message, client, nickname)
        except:
            remover(message, client)
            break

def receive():
    while True:
        client, address = server.accept()
        print(f"Uma conexão foi estabelecida com {str(address)}")
        
        nickname = client.recv(1024).decode()
        nicknames.append(nickname)
        clients.append(client)
        
        print(f'O nome do usuário é {nickname}!')
        broadcast(f'{nickname} entrou no chat!'.encode())
        client.send(f'\n\n-Bem vindo ao chat {nickname}, o chat consiste em comandos de minigame,funcionalidades e troca de mensagens,\n-para receber os possíveis comandos digite ;;help\n'.encode())
        
        thread = threading.Thread(target=handle, args=(client,nickname))
        thread.start()
    
print("O servidor está ligado")
receive()