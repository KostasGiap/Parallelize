import socket
import datetime
import random
import sys



class ClientSocket():
    def __init__(self, client_id):
        self.client_id = str(client_id)
        self.s = socket.socket(socket.AF_INET, socket.SOCK_STREAM) 

    # Connects to the server and then sends data every minute
    def Connect(self, host, port):
        self.s.connect((host, port))
        try:
            while True:
                time = datetime.datetime.now()
                self.show(seconds=str(time.second))
                if time.second == 0:
                    electicity_counter = str(random.randint(1, 1000))
                    data = "{0}:{1}".format(self.client_id, electicity_counter)
                    self.s.send(data)
                    while time.second == 0:
                        time = datetime.datetime.now()
                        
        except KeyboardInterrupt:
            self.s.send('exit')
            self.s.close()

    # Shows current seconds
    def show(self, seconds):
        if len(seconds) < 2:
            seconds = "0"+seconds
        sys.stdout.write('\r')
        sys.stdout.write("seconds: "+seconds)
        sys.stdout.flush()



if __name__ == "__main__":
    client = ClientSocket(client_id=random.randint(1, 100))
    client.Connect(host="localhost", port=8080)
