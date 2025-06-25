import socket
from time import sleep

server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server_socket.bind(("localhost",12346))
server_socket.setblocking(False)


server_socket.listen(10)
print("Сервер очікує на підключення")
clients = []

while True:
    try:
        connection,  address = server_socket.accept()
        print("підключився клієнт:", address)
        connection.setblocking(False)
        clients.append([connection,address])

        client_name = connection.recv(1024).decode()
        connection.send(f"Вітаю {client_name} на сервері".encode())
        print(f"{client_name} підключився до сервера")
    except:
        pass

    for client in clients:
        try:
            client[0].send(f"Онлайн: {client[1]}".encode())
        except:
            print(f"Відключився від сервера: {client[1]}")
            clients.remove(client)

    sleep(0.5)

command = connection.recv(1024).decode()



connection.close()
server_socket.close()
