import os, sys, time, random
import numpy as np
from pathlib import Path
from Parser import *


random.seed(os.urandom(10))  # Best Random seed

''' I am trying to automize everything. Let's Hope it is faster '''
''' Using many parts from SimpleBool package '''
'''I am using Class which makes I think makes my life a lot easier. Let's See'''
''' Using Class for these operations is a terible Idea. Never do it!!! '''
'''I hope Iron Man is with me throughout the Journey'''

# global variables. Nodes record names of all nodes. InterMat record edge
# weights of all the interactions
global NODES, INTERMAT

if __name__ == '__main__':
    #sys.argv is the list of all arguments you give in the terminal, i.e., command line, like python 'name of the file' 'other args'
    #so sys.argv is list of 'name of the file' and 'other args'
    #sys.argv[0] is the name of the program.
    if sys.argv[1]:
        in_file = sys.argv[1] #Either you can give the name of the file (Remember, not zero as zero means name of python file)
    else:
        in_file = 'bool.in' #Or it takes in the default file

    INPUT = InputParser(in_file)
    network = INPUT['network']; Iters_no = INPUT['iterations']

    iters_no = 1 
    while iters_no <= Iters_no:
        print(f'Rand Run No.:{iters_no}')
        NODES, INTERMAT = ReadRules(network, INPUT['model'], iters_no=iters_no)
        if INPUT['mode'] == 'Async':
            from Async import SummaryAsync
            SummaryAsync(NODES, INTERMAT,INPUT,folder=network)
            print("All the analysis is done. Bye ;)")
        iters_no = iters_no + 1