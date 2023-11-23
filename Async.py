import numpy as np
import os,time
from Utility_funcs import *
from sort_ss import *

'''This code is a modified and reduced version of Async.py from CSB-SCLC/Fast-Bool: https://github.com/uday2607/CSB-SCLC/tree/master
to allow inclusion of random weightage of edges and automatic sorting of stable states based on node patterns'''

start_time = time.time()

def Dynamics(IniVector,inter_mat,steps,values,node_num):
    ''' Updates the initial vector for given time steps and gives the steady state vectors '''

    ''' For numba functionality '''
    inter_mat = inter_mat.astype('float64') #For better calculations
    values = np.array(values) #For numba

    prevVector = IniVector #Initial vector

    for i in range(steps): #Time dynamics for given steps
        nextVector = IterOneAsync(inter_mat, prevVector,values)
        if i < steps-1: prevVector = nextVector
        #adding this trajectory to the State traj vector

    if np.all(prevVector == nextVector): #Fixed Point Attractors
        return (True, vect2str(IniVector,node_num), vect2str(nextVector,node_num)) #Fixed Point steady state. IniVector is the basin of the Steady state
    else:
        return (False, False, False) #If it is not a steady state don't return anything

def Simulation(nodes,inter_mat,input,folder):
    ''' Runs dynamics for given number of initial conditions '''

    print("Preparing Simulation rules...\n")
    import multiprocess as mp

    node_num = len(nodes)
    steps = input['steps'] #Number of time Steps
    if input['rounds']: rounds = input['rounds']
    else: rounds = 2**len(nodes)
    #Number of simulation Runs
    run_power = np.ceil(np.ceil(highestPowerof2(rounds))/2) #So that we can create a nested for loop for multiple processes
    values = input['node_values'] #Values of node

    basin_dic = {}  # store attractor for each state, key as basin state, value as attractor state.
    SteadyState = {}  # store steadystate and its frequency
    frustration = {} # store frustration of each stable stable, stable state as key, frustration as value

    if input['Parallel_Process']:
        print("\nParallel Process support is enabled. Number of Individual processes is %s" % input['Number_processes'])
        process = input['Number_processes']
        pool = mp.Pool(processes = process) #Creating No of processors
    else:
        print("\nParallel Process support is not enabled. Runs take a lot of time....")
        pool = mp.Pool(processes = 1) #Creating 1 process

    print("Preparing %s runs...." %2**(run_power))
    print("Fireing the runs for each initial condition. May take some time")
    index = 0 #index of run

    for i in range(int(2**(run_power))):
        value = i*100/2**(run_power)
        print(" %0.4f percent complete" %value, end = '\r', flush = True)
        jobs = []; run_index = []; initial_vector = []
                
        for j in range(int(rounds/2**(run_power))):
            IniVector = GetIni(nodes,values)
            run_index.append(j); initial_vector.append(IniVector)
            index += 1
            jobs.append(pool.apply_async(Dynamics,args=(IniVector,inter_mat,steps,values,node_num)))

        [result.wait() for result in jobs]
        for results in jobs:
            result = results.get()
            if result[0]:
                if result[2] in SteadyState: #If steady state is already found and basin is different, then we store the basin
                    basin_dic[result[1]] = result[2]
                    SteadyState[result[2]] += 1 #Frequency increased
                else:
                    basin_dic[result[1]] = result[2] #Adding basin and attractors
                    SteadyState[result[2]] = 1
                    frustration[result[2]] = Frustration(result[2],inter_mat)

    pool.close() #Very important to close the pool. Or multiple instances will be running

    return SteadyState,frustration

def SummaryAsync(nodes,inter_mat,input,folder):
    ''' Summarises all the info of this Asynchronous update dynamics '''

    print("Summarizing the results.....\n")
    SteadyState,frustration = Simulation(nodes,inter_mat,input,folder)

    current_dir = os.getcwd() #current working directory
    path = current_dir + "/OUTPUT/" + folder
    try: os.makedirs(path) #If folder doesn't exist then create it
    except: pass
    file = f'Summary_Async.xlsx'
    
    color_arr,init_clr_len,row_label = node_sort(input,folder,file,nodes,SteadyState,frustration)
    update(input,color_arr,init_clr_len,folder,row_label)

    time_taken = (time.time() - start_time)
    print("Total Time elapsed: %0.4f " %time_taken)
    return
