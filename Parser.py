import os, joblib
import numpy as np
from pathlib import Path
from gen_ids import *

'''Below are the modified versions of Parser.py from CSB-SCLC/Fast-Bool: https://github.com/uday2607/CSB-SCLC/tree/master'''

def InputParser(Input_File):
    '''parser parameters for simulation and transition matrix building'''
    INPUT = {'network': 'rules',
             'node_values': '1,-1',
             'rounds': 0,
             'steps': 1,
             'mode': 'Sync',
             'model': 'Ising',
             'Parallel_Process': False,
             'Number_processes': 1,
             'ss_file': 'Stable_States.xlsx',
             'iterations': 1
             }  # define parameters

    for each_line in open(Input_File).readlines():
        para_name = each_line.split('=')[0].strip()
        para_value = each_line.split('=')[1].strip()
        if para_name in list(INPUT.keys()):
            # Creating key-pair values for Inputs
            INPUT[para_name] = para_value
        else:
            print("Error: Unknown Parameters: %s" % para_name)
            exit()  # Exits out of code so that OP can rectify the errors

    try:
        INPUT['network'] = str(INPUT['network'])
        INPUT['node_values'] = str(INPUT['node_values'])
        INPUT['rounds'] = int(INPUT['rounds'])
        INPUT['steps'] = int(INPUT['steps'])
        INPUT['mode'] = str(INPUT['mode'])
        INPUT['model'] = str(INPUT['model'])
        INPUT['Parallel_Process'] = True if INPUT['Parallel_Process'] == 'True' else False
        INPUT['Number_processes'] = int(INPUT['Number_processes'])
        INPUT['ss_file'] = str(INPUT['ss_file'])
        INPUT['iterations'] = int(INPUT['iterations'])
        #INPUT['rand_mod_ew'] = np.array([float(i) for i in (INPUT['rand_mod_ew']).split(',')])
        
        for empty_keys in list(INPUT.keys()):
            if INPUT[empty_keys] == [''] or INPUT[empty_keys] == [['']]:
                # Formatting all the inputs into desired form
                INPUT[empty_keys] = []
            # [''] or [['']] for empty cases
    except BaseException:
        print("Error: Invalid input data types!")
        exit()  # Exits out of code so that OP can rectify the errors

    values = ['1,-1', '1,0']
    if INPUT['node_values'] in values:
        INPUT['node_values'] = [
            float(i) for i in (
                INPUT['node_values']).split(',')]
    else:
        print("Wrong Node Values! Use 1,-1 or 1,0")
        exit()  # Exits out of code so that OP can rectify the errors

    if INPUT['mode'] not in ['Async', 'Sync']:
        print("Wrong simulation method! Use 'Sync' or 'ASync'")
        exit()  # Exits out of code so that OP can rectify the errors

    Models = ['Ising', 'InhibitoryDominant', 'ActivatoryDominant']
    if INPUT['model'] not in Models:
        print("Wrong model! Use 'Ising','InhibitoryDominant' or 'ActivatoryDominant'")
        exit()  # Exits out of code so that OP can rectify the errors

    return INPUT

################################################################################
def ReadRules(network, model, iters_no):
    ''' Reads .ids and .topo file to get nodes and interactions '''

    current_dir = os.getcwd()  # current working directory
    path = current_dir + "/INPUT/"
    adjw_path = current_dir + "/OUTPUT/" + network + '/Adjacency_mat/' 
    try: os.makedirs(adjw_path)
    except: pass

    file = network
    if os.path.isfile(path + file +'.ids'): pass
    else: gen_ids_file(file)
    NODES = [x.split('\t')[0] for x in open(
            Path(path + file + '.ids')).readlines()]  # Contains all the nodes (from .ids)
    NODES = sorted(NODES) #sorting the nodes alphabetically
    
    #INTERMAT = np.ascontiguousarray([[0] * len(NODES)] * len(NODES))  # Interaction matrix
    INTERMAT = np.zeros((len(NODES),len(NODES)))
    Models = ['Ising', 'InhibitoryDominant','ActivatoryDominant']  # All Models
    # Differnt edge weights for different models
    Edge_weights = [[1.0, -1.0], [1.0, -1000.0], [1000.0, -1.0]]
    Source = ['Source']; Target = ['Target']; Rand_ew = ['Edge Weights']

    for line in open(
        Path(path + file + '.topo')).readlines()[1:]:  # reads interactions from .topo file
        res = line.split()
        if res[2] == '1': wild_ew = Edge_weights[Models.index(model)][0]
        if res[2] == '2': wild_ew = Edge_weights[Models.index(model)][1]
        INTERMAT[NODES.index(res[1])][NODES.index(res[0])] = wild_ew
    joblib.dump(INTERMAT,adjw_path+'Adj_mat_wild')

    return NODES, INTERMAT



