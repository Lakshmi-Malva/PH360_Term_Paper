''' Contains the utility codes for Asynchronous updating including those required for iterations '''
import numpy as np
import numba as nb
import random, math

def vect2str(vect,node_num):
    if len(vect) == node_num: pass
    elif len(vect) < node_num:
        if type(vect)==np.array: vect = vect.tolist()
        diff = node_num - len(vect)
        temp = []
        for _ in range(diff):
            temp.append(-1)
        vect = temp + vect
    else: 
        print('Wrong array')
        exit()
    vect = np.array(vect)
    string = ''
    for i in range(len(vect)):
        if vect[i]>=0: string = string+str(int(vect[i]))
        else: string = string+'0'
    return string

def str2vect(string,node_num):
    if len(string) == node_num: pass
    elif len(string) < node_num:
        string = string.zfill(node_num)
    else: 
        print('Wrong string')
        exit()
    vect = []
    for i in range(len(string)):
        if string[i]=='0': vect.append(-1)
        else: vect.append(int(string[i]))
    return np.array(vect)

def get_col(col,file,n):
    return list(line.split()[col-1] for line in file[n:])
    
################################################################################################################

'''Below are the codes from CSB-SCLC: https://github.com/uday2607/CSB-SCLC/tree/master'''
def IterOneAsync(inter_mat,vect,values):
    '''Iteration for one time step using Asynchronous updating'''

    vect1 = vect[:]
    #inter_mat.shape[0] = column no.; So, index picks out a random row
    index = int(inter_mat.shape[0] * random.random()) #index of the node which will get updated
    # same matrix mult but with one row and vect1
    value = np.dot(inter_mat[index], vect1)   #value of activations/inhibitions
    #sigma Jij.Sj ><= 1 ,-1, previous vector
    if value > 0: vect1[index] = int(values[0])
    elif value < 0: vect1[index] = int(values[1])
    else: True

    return vect1

def GetIni(nodes,values):
    ''' Gives an initial condition '''

    values = np.array(values)
    # Genearting a boolean vector of size node num
    # the elements will be randomly chosen from the elements of values
    ini_vect = np.random.choice(values,len(nodes))
    return ini_vect


def parallel_nonzero_count(arr):
    #will make the multi-dim array into 1-D, flattens row wise
    flattened = arr.ravel()
    sum = 0
    for i in range(flattened.size):
        sum += flattened[i] != 0
    return sum

def frust(boolvect1,inter_mat):
    ''' Calculates frustration of a vector '''

    # By calculating number of non-zero elements we can know number of edges in a network
    edges = parallel_nonzero_count(inter_mat)
    # transpose in Numpy produces the same mtrix for 1xn mtrix. So we use reshaping
    #basically transpose
    boolvect2 = boolvect1.reshape((-1, 1))
    # reshape((-1,1)) means columns to rows and single column
    frust_mat = (np.multiply((np.multiply(inter_mat,boolvect2)),boolvect1))
    # Frustration for a node = sigma JijSiSj
    result = (frust_mat < 0).sum() # Checking how many nodes are Frustrated

    return result/edges # returns relative frustration

def Frustration(vect,inter_mat):
    ''' Returns frustration using the njit function '''
    vect = str2vect(vect,inter_mat.shape[0])
    num = frust(vect,inter_mat)
    return num

def highestPowerof2(n):
    ''' Find the highest Power of 2 '''
    p = int(math.log(n, 2))
    return p
################################################################################################################