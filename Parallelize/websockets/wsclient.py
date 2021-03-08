import asyncio
import websockets
import time, datetime
import random
import sys

     



class ClientSocket():
    def __init__(self, client_ip):
        self.uri = "ws://localhost:8765"
        self.client_ip = str(client_ip)
        print ("client id: " + self.client_ip)

    def Connect(self):
        while True: 
            time = datetime.datetime.now()
            self.show(seconds=str(time.second))
            if time.second == 0:
                electicity_counter = str(random.randint(10, 1000))
                data = self.client_ip +":"+ electicity_counter
                asyncio.get_event_loop().run_until_complete(self.Send(data))
                while time.second == 0:
                    time = datetime.datetime.now() 
        
    async def Send(self, data):
        async with websockets.connect(self.uri) as websocket:
            await websocket.send(data)

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
    