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
        question varchar(50),
        answer varchar(50),
        password varchar(50),
        id INTEGER PRIMARY KEY AUTOINCREMENT
    )
''')
cursor.execute('''
CREATE TABLE IF NOT EXISTS historiques (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    data_search VARCHAR(50),
    id_user INTEGER,
    datetime VARCplaceHAR(50),
    FOREIGN KEY (id_user) REFERENCES users (id)
);
''')
cursor.execute('''
CREATE TABLE IF NOT EXISTS favorits (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    data_favorite VARCHAR(50),
    id_user INTEGER,
    datetime VARCplaceHAR(50),
    FOREIGN KEY (id_user) REFERENCES users (id)
);
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
                    username = split_values[0][1:]
                    password = split_values[1]
                    print(username,password)
                    cu1 = db.cursor()
                    cu1.execute("select username,password from users where username=? and password=?",(username,password))
                    user1 = cu1.fetchone()
                    if user1 and username == user1[0] and password == user1[1]:
                        users[username.lower()] = sock
                        print("l'utilisateur " + username + " connecté.")
                        sock.send(("Bienvenue : " + str(username)).encode('utf-8'))
                    else:
                        print("username ou mot de passe incorrect")
                        sock.send(("username ou  Mot de passe incorrect").encode('utf-8'))
                elif data.startswith("+"):
                    split_values = data.split(',')
                    username = split_values[0][1:]
                    nom = split_values[1]
                    prenom = split_values[2]
                    password = split_values[3]
                    question=split_values[4]
                    answer=split_values[5]

                    print(username, nom, prenom,question, answer,password)
                    cur1 = db.cursor()
                    cur1.execute('''INSERT INTO users(username,nom,prenom,question,answer,password) VALUES(?,?,?,?,?,?)''',(username, nom, prenom,question,answer, password))
                    db.commit()
                    sock.send(("l'utilisateur " + str(username)+" : a été ajouter avec success").encode('utf-8'))

                    print("l'utilisateur " + str(username)+" : a été ajouter avec success")
                elif data.startswith("-"):
                    split_values = data.split(',')
                    username = split_values[0][1:]
                   
                    print(username)

                    c1 = db.cursor()
                    c1.execute("select username from users where username=?",(username,))
                    user11 = c1.fetchone()
                    print(user11[0])
                    if user11 and username == user11[0]:
                       sock.send(("verified :" + str(username)).encode('utf-8'))

                    else:
                        print(" n'a march pas")

                elif data.startswith("*"):
                    split_values = data.split(',')
                    username = split_values[0][1:]
                    question = split_values[1]
                    answer = split_values[2]

                    print( username,question,answer)
                    curr2 = db.cursor()
                    curr2.execute("SELECT * FROM users WHERE username=? and question=? and answer=?",(username,question, answer))
                    user2 = curr2.fetchone()
                    if user2:
                       sock.send(("good job").encode('utf-8'))

                    else:
                        print('data of user2 not find')
                    

                

                elif data.startswith("~"):
                    split_values = data.split(',')
                    username = split_values[0][1:]
                    nvpass = split_values[1]

                    print(username,nvpass)
                    curr2 = db.cursor()
                    curr2.execute("UPDATE users SET password=? where username=?",(nvpass,username))
                    db.commit()
                    print("mot de pass update avec success")

                
                

            except Exception as e:
                print(str(e))
                continue
