import socket
from lib import *
from lib import IP, PORT


trama = "0"
data = ""
write = False
current_switch = "4"

class TCPIPconnection():
    def __init__(self):
        # TCP/IP socket declaration
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.connect(IP,PORT)
        # self.check_connection()
        
    def connect(self, ip, port):
        # Connecting to server
        self.server_address = (ip, port)
        print('connecting to {} port {}'.format(*self.server_address))
        self.sock.connect(self.server_address)

    def check_connection(self):
        # Sending a message to the ESP8266 and printing the response.
        # This should be a string: 'Connected'
        self.sock.send("connecting".encode('ascii'))
        msg = self.sock.recv(1024)
        print(msg.decode('ascii'))

    def communicate(self):
        global trama, data
        self.sock.send(str(trama).encode('ascii'))
        data = self.sock.recv(1024).decode('ascii')
        
       
        
        # print("--------")
        # print("trama: ", type(str(trama)), trama)
        # print("data: ", type(data), type(data[0]), data)
        # print("items: ", items.led, items.tv, items.air[1],items.appliance, items.blind[1])
        
        
    def to_list(self,string):
        list1=[]
        list1[:0]=string
        return list1
    
    # def updateItems(self):
    #     global items, data
    #     items.led = int(data[1])
    #     items.tv = int(data[2])
    #     items.air[0] = items.air_onoff = int(data[3])
    #     items.appliance = int(data[4])
    #     items.blind = int(data[4])


    def close(self):
        self.sock.close()


def readTrama():
    global trama
    
    with open('trama1.txt', 'r') as f:
        aux = f.read()
        print("trama: ", aux)
        if len(aux) > 1:
            trama = aux
        
            

def writeTrama():
    global data, current_switch

    
    with open('trama2.txt', 'w') as f:
        f.write(current_switch + data)
        if current_switch == "3":
            current_switch = "4"
        elif current_switch == "4":
            current_switch = "3"

 
tcpip = TCPIPconnection()

while True:
    
    readTrama()  
    #if not trama.startswith(current_switch):
    trama = trama[1:]
    tcpip.communicate()

    
    print("data: ", data)

 


    