import socket
import threading


def send_message():
    while True:
        messege = input()
        if messege.lower() == "exit":
            client_socket.close()
            break
        client_socket.send(messege.encode())


client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

name = input("Для підключення на сервер введіть своє ім'я: ")
client_socket.connect(("localhost",12346))

client_socket.send(name.encode())
response=client_socket.recv(1024).decode()
print("Відповідь від сервера", response)

threading.Thread(target=send_message).start()

while True:
   try:
       message = client_socket.recv(1024).decode().strip()
       if message:
           print(message)
   except:
       break








client_socket.close()