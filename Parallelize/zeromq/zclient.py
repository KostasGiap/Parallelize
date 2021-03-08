import sys
import random
import datetime
import zmq

class ClientSocket():
    def __init__(self, client_ip):
        self.host = "localhost"
        self.port = 5555
        self.client_ip = str(client_ip)
        print ("client id: " + self.client_ip)

    def Connect(self):
        context = zmq.Context()
        self.socket = context.socket(socket_type=zmq.REQ)
        self.socket.connect("tcp://{0}:{1}".format(self.host, self.port))
        self.Electricity()
    
    def Electricity(self):
        while True:
            time = datetime.datetime.now()
            self.show(seconds=str(time.second))
            if time.second == 0:
                electicity_counter = str(random.randint(10, 1000))
                data = self.client_ip +":"+ electicity_counter
                self.socket.send(data) 
                confirm = self.socket.recv() 
                while time.second == 0:
                    time = datetime.datetime.now() 

    # Shows current seconds
    def show(self, seconds):
        if len(seconds) < 2:
            seconds = "0"+seconds
        sys.stdout.write('\r')
        sys.stdout.write("seconds: "+seconds)
        sys.stdout.flush()
        
        
                
            
if __name__ == "__main__":
    client = ClientSocket(client_ip=random.randint(1, 10000))   
    client.Connect() 
    