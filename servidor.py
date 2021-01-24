import threading
import socket

server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.bind(('127.0.0.1', 55555))
server.listen()

clients = []
nicknames = []
palavra = ""
display = ""
chances = 7
letras = ""

def broadcast(message):
    for client in clients:
        client.send(message)

def reiniciar_jogo_da_velha():
    global palavra, display, letras, chances
    palavra = ""
    display = ""
    chances = 7
    letras = ""

def remover(client):
    index = clients.index(client)
    clients.remove(client)
    client.close()
    nickname = nicknames[index]
    print(f'{nickname} saiu do chat!')
    broadcast(f'{nickname} saiu do chat!'.encode())
    nicknames.remove(nickname)
    return

def iniciar_forca(client, nickname):
    global palavra, display
    client.send("Escolha sua palavra para a forca:".encode())
    print(nickname)
    palavra = client.recv(1024).decode().lower()
    palavra = palavra.replace(nickname+": ", "")
    print(palavra)
    for i in palavra:
        display = display + "_"
    print(display)
    broadcast("______\n|    |\n|    \n|    \n|    \n|\n|_\n".encode())
    broadcast(display.encode())

def adivinhar(client, nickname):
    global palavra, display, letras, chances
    existe = 0
    aux = ""
    client.send("-Digite a letra desejada: ".encode())

    tentativa = client.recv(1024).decode()
    tentativa = tentativa.replace(nickname+": ", "")
    if palavra != '':
        if len(tentativa) > 1:
            broadcast("Não é permitida a adivinhação maior que um caractere".encode())
            return

        for i in range(len(palavra)):
            if palavra[i] == tentativa:
                existe = 1
                aux = aux + palavra[i]
            else:
                aux = aux + display[i]
        display = aux
        letras = letras + tentativa + " "

        if existe == 0:
            chances = chances - 1

        if chances == 7:
            broadcast("______\n|    |\n|    \n|    \n|   \n|\n|_".encode())
        elif chances == 6:
            broadcast("______\n|    |\n|    0\n|    \n|   \n|\n|_".encode())
        elif chances == 5:
            broadcast("______\n|    |\n|    0\n|    |\n|   \n|\n|_".encode())
        elif chances == 4:
            broadcast("______\n|    |\n|    0\n|   /|\n|   \n|\n|_".encode())
        elif chances == 3:
            broadcast("______\n|    |\n|    0\n|   /|\ \n|   n|\n|_".encode())
        elif chances == 2:
            broadcast("______\n|    |\n|    0\n|   /|\ \n|   / \n|\n|_".encode())
        elif chances == 1:
            broadcast("______\n|    |\n|    0\n|   /|\ \n|   / \ \n|\n|_".encode())
        elif chances == 0:
            broadcast("______\n|    |\n|  (X_X)\n|   /|\ \n|   / \ \n|\n|_".encode())

        broadcast(f"Palavra: {display}\n Tentativas restantes: {chances}\n Letras tentadas {letras}".encode())

        if chances <= 0:
            broadcast(f"-As chances acabaram, a palavra era {palavra}".encode())
            reiniciar_jogo_da_velha()
        if palavra == display:
            broadcast(f"-A palavra {palavra} foi adivinhada".encode())
            reiniciar_jogo_da_velha()
    else:

        return

def comandos(message, client, nickname):
    print(message.decode().lower())
    if message.decode().lower() == (f"{nickname}: ;;help"):
        client.send("\n-Os comandos existentes são:\n;;help para listar os comandos\n;;forca para o jogo da forca\n;;sair para sair do chat\n".encode())
        
    elif message.decode().lower() == (f"{nickname}: ;;sair"):
        client.send("Você será desconectado em instantes".encode())
        remover(client)
        
    elif message.decode().lower() == (f"{nickname}: ;;forca"):
        broadcast(f"{nickname} começou um jogo da forca para adivinhar uma letra da palavra digite ;;adivinhar\n".encode())
        iniciar_forca(client, nickname)
        
    elif message.decode().lower() == (f"{nickname}: ;;adivinhar"):
        adivinhar(client, nickname)

    else:
        broadcast(message)  
    return

def comunicacao(client, nickname):
    while True:
        try:
            message = client.recv(1024)
            comandos(message, client, nickname)
        except:
            remover(client)
            break

def conexao():
    while True:
        client, address = server.accept()
        print(f"Uma conexão foi estabelecida com {str(address)}")
        
        nickname = client.recv(1024).decode()
        nicknames.append(nickname)
        clients.append(client)
        
        print(f'O nome do usuário é {nickname}!')
        broadcast(f'{nickname} entrou no chat!'.encode())
        client.send(f'\n\n-Bem vindo ao chat {nickname}. O chat consiste em comandos de minigame, funcionalidades e troca de mensagens.\n-Para receber os possíveis comandos digite ;;help\n'.encode())
        
        thread = threading.Thread(target=comunicacao, args=(client, nickname))
        thread.start()

print("O servidor está ligado")
conexao()