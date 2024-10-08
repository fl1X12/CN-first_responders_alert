import socket
import threading
import ssl

HEADER=64
PORT=12345
SERVER="192.168.228.219" ##socket.gethostbyname(socket.gethostname())   
ADDR =(SERVER,PORT)
FORMAT="utf-8"
DISCONNECT="!DISCONNECT"

context=ssl.SSLContext(ssl.PROTOCOL_TLS_SERVER)
context.load_cert_chain(certfile="C:/Users/shanm/OneDrive/Desktop/teja/code main/CN/server.pem",keyfile="C:/Users/shanm/OneDrive/Desktop/teja/code main/CN/key.pem") 


server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.bind(ADDR)


def handle_client(conn,addr):
    print(f"[NEW CONNECTION] {addr} connected.")
    conn_ssl=context.wrap_socket(conn,server_side=True)
    connected=True
    while connected:
        msg_length=conn_ssl.recv(HEADER).decode(FORMAT)
        if msg_length:
            msg_length=int(msg_length)
            msg=conn_ssl.recv(msg_length).decode(FORMAT)
            if(msg==DISCONNECT):
                connected=False
            print(f"[{addr}] {msg}")
    try:
        conn_ssl.shutdown(socket.SHUT_RDWR)
        conn.close()
    except ssl.SSLError as e:
        print(f"SSL error during disconnect :{e}")

def start():
    server.listen()
    print(f"[LISTENING]Server is listening on {SERVER}")
    while True:
        conn,addr=server.accept()
        thread=threading.Thread(target=handle_client,args=(conn,addr))
        thread.start()
        print(f"[ACTIVE CONNECTIONS] {threading.activeCount()-1}")
        
print("[STARTING] server is starting")
start()