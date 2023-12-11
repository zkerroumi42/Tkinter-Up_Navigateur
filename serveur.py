import socket
import select
import sqlite3

port = 12345
socket_list = []
users = {}

HOST = socket.gethostbyname(socket.gethostname())
db = sqlite3.connect('db.sqlite3')

cursor = db.cursor()
cursor.execute('''
    CREATE TABLE IF NOT EXISTS users(
        username varchar(50),
        nom varchar(50),
        prenom varchar(50),
        password varchar(50),
        id INTEGER PRIMARY KEY AUTOINCREMENT
    )
''')
db.commit()

server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
server_socket.bind((HOST, port))
server_socket.listen()
print(HOST)
socket_list.append(server_socket)

while True:
    ready_to_read, _, _ = select.select(socket_list, [], [], 0)
    for sock in ready_to_read:
        if sock == server_socket:
            connect, addr = server_socket.accept()
            socket_list.append(connect)
            connect.send(("You are connected from:" + str(addr)).encode('utf-8'))
        else:
            try:
                data = sock.recv(2048).decode('utf-8')
                if data.startswith("#"):
                    split_values = data.split(',')
                    username = split_values[0][1:]  # Remove the '#' from the username
                    password = split_values[1]
                    cu1 = db.cursor()
                    cu1.execute("select username,password from users where username=? and password=?",(username,password))
                    user1 = cu1.fetchone()
                    if user1 and username == user1[0] and password == user1[1]:
                        users[username.lower()] = sock
                        print("l'utilisateur " + username + " connecté.")
                        sock.send(("Bienvenue : " + str(data[1:10])).encode('utf-8'))
                    else:
                        print("mot de passe incorrect")
                        sock.send(("Mot de passe incorrect").encode('utf-8'))
                elif data.startswith("+"):
                    split_values = data.split(',')

                    # Access individual values
                    username = split_values[0][1:]  # Remove the '+' from the username
                    nom = split_values[1]
                    prenom = split_values[2]
                    password = split_values[3]

                    print(username, password, nom, prenom)
                    cur1 = db.cursor()
                    cur1.execute('''INSERT INTO users(username,nom,prenom,password) VALUES(?,?,?,?)''',(username, nom, prenom, password))
                    db.commit()
                    sock.send(("l'utilisateur " + str(username)+"ajouter avec success").encode('utf-8'))
            except Exception as e:
                print(str(e))
                continue
