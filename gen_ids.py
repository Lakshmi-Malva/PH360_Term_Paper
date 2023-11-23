import numpy as np
import os
from pathlib import Path

def element_exists(lst, element):
  try:
    lst.index(element)
    return True
  except ValueError:
    return False

def gen_ids_file(file):
    Nodes = []
    current_dir = os.getcwd()  
    path = current_dir + "/INPUT/"
    for line in open(
        Path(
            path +
            file +
            '.topo')).readlines()[
            1:]:  # reads interactions from .topo file
        res = line.split()
        for i in range(len(res)-1):
            find = str(element_exists(Nodes,res[i]))
            if find == 'False': Nodes.append(res[i])

    Nodes = np.array(sorted(Nodes))
    label = np.arange(len(Nodes))
    data = np.column_stack([Nodes,label])
    np.savetxt(path+file+'.ids', data, delimiter = '\t',fmt = '%s')
    return 