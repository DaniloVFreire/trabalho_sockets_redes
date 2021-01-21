import threading
import socket

nickname = input("Escolha o seu apelido: ")

client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

client.connect(('127.0.0.1', 55555))

def receive():
    client.send(nickname.encode())
    while True:
        try:
            message = client.recv(1024).decode()
            if message == "qweirpuyaskdljfhqowieury128907346562087364lasdjkhfgeoirqwyfbv34296234592fbuefv3475":
                client.close()
                break
            print(message)
        except:
            print("An error occurred!")
            client.close()
            break
        
def write():
    while True:
        message = f'{nickname}: {input("")}'
        client.send(message.encode())
        
receive_thread = threading.Thread(target=receive)
receive_thread.start()

write_thread = threading.Thread(target=write)
write_thread.start()