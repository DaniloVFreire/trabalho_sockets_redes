import threading
import socket

nickname = input("Escolha o seu apelido: ")

client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

client.connect(('127.0.0.1', 55555))



def recebimento():
    client.send(nickname.encode())
    while True:
        try:
            message = client.recv(1024).decode()
            print(message)
        except:
            print("An error occurred!")
            client.close()
            break
        
def escrever():
    while True:
        message = f'{nickname}: {input("")}'
        client.send(message.encode())
        
receive_thread = threading.Thread(target=recebimento)
receive_thread.start()

write_thread = threading.Thread(target=escrever)
write_thread.start()