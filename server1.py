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
server_sock=context.wrap_socket(server,server_side=True)

def handle_client(conn, addr):
    print(f"[NEW CONNECTION] {addr} connected.")
    connected = True
    while connected:
        try:
            msg_length = conn.recv(HEADER).decode(FORMAT)
            if not msg_length:
                break  # If the message length is not received, break out of the loop

            msg_length = int(msg_length)
            msg = conn.recv(msg_length).decode(FORMAT)

            if msg == DISCONNECT:
                connected = False
                print(f"[{addr}] Disconnecting...")
                break  # Break out of the loop when disconnect message is received

            print(f"[{addr}] {msg}")

        except ssl.SSLError as e:
            print(f"SSL error during message reception: {e}")
            break

    try:
        conn.shutdown(server_sock.SHUT_RDWR)
        conn.close()
    except ssl.SSLError as e:
        print(f"SSL error during disconnect: {e}")

    print(f"[CONNECTION CLOSED] {addr}")
def start():
    server_sock.listen()
    print(f"[LISTENING]Server is listening on {SERVER}")
    while True:
        conn,addr=server_sock.accept()
        thread=threading.Thread(target=handle_client,args=(conn,addr))
        thread.start()
        print(f"[ACTIVE CONNECTIONS] {threading.activeCount()-1}")
        
print("[STARTING] server is starting")
start()