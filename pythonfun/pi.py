import random
import os
from time import time
from numba import njit
import numpy as np
from concurrent.futures import ThreadPoolExecutor

def interpreted_pi(n):
    c = 0
    for _ in range(n):
        x = random.uniform(0,1)
        y = random.uniform(0,1)
        if x*x+y*y<1:
            c+=1    
    return c

@njit(nogil=True)
def compiled_pi(n):
    c = 0
    for _ in range(n):
        x = random.uniform(0,1)
        y = random.uniform(0,1)
        if x*x+y*y<1:
            c+=1    
    return c

print("depth:")
n = int(input())
cores = os.cpu_count()
compiled_pi(1)

start = time()
print('\ninterpreted:\n',4*interpreted_pi(n)/n)
end = time()
print('Time taken:', "{:.3f}".format(1000*(end-start)), "ms")

start = time()
print('\ncompiled:\n',4*compiled_pi(n)/n)
end = time()
print('Time taken:', "{:.3f}".format(1000*(end-start)), "ms")

with ThreadPoolExecutor(cores) as ex:
    start = time()
    bean = ex.map(compiled_pi,np.full(shape=(cores),fill_value=int(n/cores)))
    total_in_c = sum(bean)
    end = time()
    print('\nmulti-threaded and compiled:\n',4*total_in_c/n)
    print('Time taken:', "{:.3f}".format(1000*(end-start)), "ms")
