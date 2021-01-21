import threading
import socket

server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.bind(('127.0.0.1', 55555))
server.listen()

clients = []
nicknames = []
palavra = ""
display = ""
chances = 6

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

def iniciar_forca(client, nickname):
    global palavra
    global display
    client.send("Escolha a palavra para a forca:".encode())
    print(nickname)
    palavra = client.recv(1024).decode().lower()
    print(palavra)
    palavra = palavra.replace(nickname+": ", "")
    print(palavra)
    for i in palavra:
        display.append("_")
    #broadcast("_____\n|    |\n|    0\n|   /|\\n|   / \\n|\n|_".encode())
    #broadcast(display.encode())
    print("aeeeeeeeee")

def adivinhar(client):
    global palavra, display
    client.send("-Digite a letra desejada: ".encode())
    existe = 0
    while True:
        tentativa = client.recv(1024).decode()
        if len(tentativa) == 1:
            break
        else:
            client.send("-".encode())
    for i in range(len(palavra)):
        if palavra[i] == tentativa:
            existe = existe + 1
            display[i] = tentativa
    if existe == 0:
        chances = chances - 1
    if chances <= 0:
        broadcast(f"As chances acabaram, a palavra era {palavra}".encode())
        palavra = ""
        display = ""
        chances = 6
    if palavra == display:
        broadcast(f"A palavra foi adivinhada: {palavra}".encode())
        palavra = ""
        display = ""
        chances = 6
        

    pass

def comandos(message, client, nickname):
    print(message.decode().lower())
    if message.decode().lower() == (f"{nickname}: ;;help"):
        client.send("\n-Os comandos existentes são:\n;;help para listar os comandos\n;;forca para o jogo da forca\n;;sair para sair\n".encode())
        
    elif message.decode().lower() == (f"{nickname}: ;;sair"):
        client.send("você será desconectado em instantes".encode())
        client.send("qweirpuyaskdljfhqowieury128907346562087364lasdjkhfgeoirqwyfbv34296234592fbuefv3475".encode())
        remover(message, client)
        
    elif message.decode().lower() == (f"{nickname}: ;;forca"):
        broadcast(f"{nickname} começou um jogo da forca para participar digite ;;participar\n".encode())
        iniciar_forca(client, nickname)
        
    elif message.decode().lower() == (f"{nickname}: ;;adivinhar"):
        broadcast(f"{nickname} começou um jogo da forca para participar digite ;;participar\n".encode())
        adivinhar(client)
    else:
        broadcast(message)  
    """elif(message.decode().lower()).find("participar") != -1:
        if(jogadores.count() <= 2):
            jogadores.append(client)
            broadcast("Sala completa, jogo começando".encode())
                
        else:
            broadcast("Sala cheia, tente novamente mais tarde")"""



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