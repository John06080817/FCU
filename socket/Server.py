import socket

host = '140.134.30.161'
port = 8001

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.bind((host, port))
s.listen(5)

print('wait connect...')
while True:
    conn, addr = s.accept()
    print('connect by ', addr)
    rec = []
    while True:
        data = conn.recv(3)
        rec.append(data)
        if len(rec) == 255:
            print(rec)
            rec = []