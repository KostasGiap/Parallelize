import time, datetime
from decimal import Decimal, getcontext
import multiprocessing



class Parallelize(object):
    def __init__(self):
        self.thread_list = []
        self.diction = {
            "id":None,
            "thread": None
        }
    
    # Creates new thread with specific id
    def NewThread(self, thread_id, WorkerClass, arguments=()):
        t = multiprocessing.Process(target=WorkerClass, args=arguments)
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
 



class Pi(Parallelize):
    def __init__(self):
        super(Pi, self).__init__()
        self.lock = multiprocessing.Lock()
        
    def Calculate(self, start_iter, end_iter):
        pi = Decimal(0)
        for i in range(start_iter, end_iter):
            pi += (Decimal(-1)**i/(1024**i))*( Decimal(256)/(10*i+1) + Decimal(1)/(10*i+9) - Decimal(64)/(10*i+3) - Decimal(32)/(4*i+1) - Decimal(4)/(10*i+5) - Decimal(4)/(10*i+7) -Decimal(1)/(4*i+3))
        self.lock.acquire()
        self.data.append(pi)
        self.lock.release()
        
    def ParallelCalculation(self, iterations, cores):
        print "Iterations: {0}".format(iterations)
        start_iter = 0
        end_iter = iterations/cores

        manager = multiprocessing.Manager()
        self.data = manager.list()

        for i in range(cores):
            self.NewThread(thread_id=i, WorkerClass=self.Calculate, arguments=(start_iter, end_iter))
            self.StartThread(thread_id=i)
            start_iter = end_iter
            end_iter += iterations/cores

        self.JoinThreads()
           
        if iterations%cores > 0:
            start_iter -= iterations/cores
            end_iter = start_iter + iterations%cores
            self.Calculate(start_iter, end_iter)
       
        pi = Decimal(0)
        for value in self.data:
            pi += value
    
        pi = (pi * 1/(2**6))
        
        return pi



def main():
    iterations = 10
    for _ in range(3):
        iterations *= 10
        for cores in range(1, 21):
            print "Cores: ", cores
            start = time.time()
            print "Pi: {0}".format(pi.ParallelCalculation(iterations, cores))
            print "Entire job took: {0}".format(time.time()-start)
            print "\n"



if __name__ == "__main__":
    getcontext().prec = 25
    pi = Pi()
    main()

