import asyncio
import websockets
import queue
import threading
import pymysql
import datetime

class Parallelize(object):
    def __init__(self):

        self.thread_list = []
        self.diction = {
            "id":None,
            "thread": None
        }
    
    # Creates new thread with specific id
    def NewThread(self, thread_id, WorkerClass, arguments=()):
        t = threading.Thread(target=WorkerClass, args=arguments)
        t.daemon = True
        self.diction["id"] = thread_id
        self.diction["thread"] = t
        self.thread_list.append(self.diction)
    
    # Starts a thread
    def StartThread(self, thread_id):
        for thread in self.thread_list:
            if thread["id"] == thread_id:
                thread["thread"].start()
                break
    
    # Joins all open threads      
    def JoinThreads(self):
        for thread in self.thread_list: 
            thread["thread"].join()
 




class MYSQL(object):
    def __init__(self):
        user = "user"
        password = "MyPassword@123"
        host = "127.0.0.1"
        database = "electricity"
        self.cnx = pymysql.connect(host, user, password, database)
        self.cursor = self.cnx.cursor()

    # Executes a specific stored procedure
    # Saves  client id and electric value into mysql server
    def ExecProcedure(self, client_id, e_value):
        query = "CALL Add_Value({0}, {1});".format(client_id, e_value)
        self.cursor.execute(query)
        self.cnx.commit()

    # Executes a specific stored procedure
    # Saves total electricity value into mysql server
    def ExecProcedure2(self, total):
        query = "CALL Add_Total_Value ({0});".format(total)
        self.cursor.execute(query)
        self.cnx.commit()

    # Closes the connection with mysql server
    def Close(self):
        # self.cursor.close()
        self.cnx.close()





class ServerSocket(Parallelize):
    def __init__(self):
        super(ServerSocket, self).__init__()
        self.NewThread(thread_id=0, WorkerClass=self.ElectricityGather)
        self.StartThread(thread_id=0)
        self.host = "localhost" 
        self.port = 8765
    
    # Waitting for connection from clients
    # For each connection starts a new thread
    def Connection(self):
        start_server = websockets.serve(self.Worker, self.host, self.port)
        asyncio.get_event_loop().run_until_complete(start_server)
        asyncio.get_event_loop().run_forever()
    
    # Receives data from client and places them into queue
    async def Worker(self, websocket, path):
        data = await websocket.recv()
        q.put(data)
    
    # Takes data from queue and executes the stored procedure
    def ElectricityGather(self):
        date_init = datetime.datetime.now()
        total = 0
        while True:
            data = q.get()
            data = data.split(":")
            client_id = data[0]
            value = int(data[1])
            total += value
            print "client id: {0}\telectric value: {1}".format(client_id, value)
            mysqldb.ExecProcedure(client_id, value)
            if datetime.datetime.now() == date_init + datetime.timedelta(days=1):
                mysqldb.ExecProcedure2(total)
                total = 0
                date_init = datetime.datetime.now()





if __name__ == "__main__":
    q = queue.Queue()
    mysqldb = MYSQL()
    server = ServerSocket()
    server.Connection()
    mysqldb.Close()