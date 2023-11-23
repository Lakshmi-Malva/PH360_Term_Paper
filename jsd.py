import numpy as np
from scipy.stats import entropy
import os

dir = os.getcwd()

def JSD(P,Q):
    R = (P+Q)/2
    jsd = float((entropy(P,R)+entropy(Q,R))/2)
    print(jsd)
    return 

Path = dir+'/jsd.txt'
file = open(Path).readlines()
get_col = lambda col: (line.split()[col-1] for line in file[1:])

P = np.array(list(map(float,get_col(1)))); Q = np.array(list(map(float,get_col(2))))
JSD(P,Q)