import socket
import threading

HOST = 'localhost'
PORT = 12346

server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server_socket.bind((HOST, PORT))
server_socket.listen(10)
print(f"Сервер запущено на {HOST}:{PORT}")

clients = []  # Список з'єднань
client_names = {}  # Словник {socket: name}


def broadcast(message, sender_socket=None):
    """Надсилає повідомлення усім клієнтам, крім відправника."""
    for client in clients:
        if client != sender_socket:
            try:
                client.send(f"{message}\n".encode())
            except:
                client.close()
                if client in clients:
                    clients.remove(client)


def handle_client(client_socket, address):
    try:
        client_socket.send("Введіть ваше ім’я: ".encode())
        name = client_socket.recv(1024).decode().strip()
        client_names[client_socket] = name
        print(f"{name} підключився з адреси {address}")
        broadcast(f"{name} приєднався до чату!", sender_socket=client_socket)
        client_socket.send(f"Вітаю {name} на сервері!".encode())

        while True:
            message = client_socket.recv(1024).decode().strip()
            if message:
                print(f"{name}: {message}")
                broadcast(f"{name}: {message}", sender_socket=client_socket)
    except:
        pass
    finally:
        if client_socket in clients:
            clients.remove(client_socket)
        name = client_names.get(client_socket, "Клієнт")
        broadcast(f"{name} покинув чат.")
        print(f"{name} відключився.")
        client_socket.close()


while True:
    try:
        client_socket, address = server_socket.accept()
        client_socket.setblocking(True)
        clients.append(client_socket)
        threading.Thread(target=handle_client, args=(client_socket, address), daemon=True).start()
    except KeyboardInterrupt:
        print("Сервер вимикається...")
        for client in clients:
            client.close()
        server_socket.close()
        break
