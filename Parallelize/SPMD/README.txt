1) sudo apt-get install python-mpi4py

2) pip install mpi4py

3) to run the script type: mpiexec --oversubscribe -n 20 python mpi4py_pi.py
   where the --oversubscribe option is used to ignore the number of available slots when deciding the number of processes to launch
   and -n parameter is the number of cores that you want to use	
