import socket
import keyboard
import geocoder


HEADER=64
PORT=12345
SERVER="192.168.56.1" ##"192.168.228.219"
FORMAT="utf-8"
DISCONNECT="!DISCONNECT"
ADDR=(SERVER, PORT)

client=socket.socket(socket.AF_INET,socket.SOCK_STREAM)
client.connect(ADDR)

def send(msg):
    message=msg.encode(FORMAT)
    msg_length=len(message)
    send_length=str(msg_length).encode(FORMAT)
    send_length += b' ' *(HEADER-len(send_length))
    client.send(send_length)
    client.send(message)

def acc_sim():
    return keyboard.is_pressed('`')

def terminate():
    return keyboard.is_pressed('=')

def accident():
        coord=get_live_location()
        coord=str(coord[0])+","+str(coord[1])
        return coord

def run():
    send("running")

def get_live_location():
    # Get current GPS coordinates using geocoder
    location = geocoder.ip('me')
    return location.latlng

def start():
    i=0
    while True:
        i+=1
        if acc_sim():
            coord=accident()
            send("accident detected at")
            send(coord)
            break
        elif terminate():
            send("simulation terminated")
            break
        elif i%6000==0:
            run()
    send(DISCONNECT)

start()