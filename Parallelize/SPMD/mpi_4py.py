
from mpi4py import MPI as mpi
import time, datetime
from decimal import Decimal, getcontext





class Pi(object):
    def __init__(self, iterations=10000):
        self.iterations=iterations
        self.cores = comm.Get_size()-1
        self.rank = comm.Get_rank()
        print "rank: ", self.rank
    
    def Calculate(self): 
        start_iter, end_iter= comm.recv(source=0, tag=0)
        pi = Decimal(0)
        for i in range(start_iter, end_iter):
            # pi += i
            pi += (Decimal(-1)**i/(1024**i))*( Decimal(256)/(10*i+1) + Decimal(1)/(10*i+9) - Decimal(64)/(10*i+3) - Decimal(32)/(4*i+1) - Decimal(4)/(10*i+5) - Decimal(4)/(10*i+7) -Decimal(1)/(4*i+3))   
        comm.send(pi, dest=0, tag=1)
    
    def CalculateOnMainNode(self, start_iter, end_iter):
        pi = Decimal(0)
        for i in range(start_iter, end_iter):
            # pi += i
            pi += (Decimal(-1)**i/(1024**i))*( Decimal(256)/(10*i+1) + Decimal(1)/(10*i+9) - Decimal(64)/(10*i+3) - Decimal(32)/(4*i+1) - Decimal(4)/(10*i+5) - Decimal(4)/(10*i+7) -Decimal(1)/(4*i+3))
        return pi
        
    
    def ParallelCalculation(self):
        if self.rank == 0:
            start = time.time()
            start_iter = 0
            dest = 1
            mod = self.iterations%self.cores

            if mod > 0: end_iter = mod
            else: end_iter = self.iterations/self.cores

            for _ in range(self.cores):
                comm.send((start_iter, end_iter), dest=dest, tag=0)
                start_iter = end_iter
                end_iter += self.iterations/self.cores
                dest +=1
                

            pi = Decimal(0)
            for _ in range(self.cores):
                pi += comm.recv(source=mpi.ANY_SOURCE, tag=1)
            
            if mod > 0: 
                pi += self.CalculateOnMainNode(start_iter, end_iter)

                
            pi = (pi * 1/(2**6))
            print "Pi: {0}".format(pi)
            print "Entire job took: {0}".format(datetime.timedelta(seconds=(time.time()-start)))
        
        else:
            self.Calculate()





if __name__ == "__main__":
    getcontext().prec = 25
    comm = mpi.COMM_WORLD
    pi = Pi()
    pi.ParallelCalculation() 
    mpi.Finalize()