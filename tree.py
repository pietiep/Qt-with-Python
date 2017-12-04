import numpy as np
import pandas as pd
from itertools import takewhile
import copy

is_tab = '\t'.__eq__

def build_tree(lines):
    lines = iter(lines)
    stack = []
    stack_gs = []
    count = 0
    for line in lines:
        indent = len(list(takewhile(is_tab, line)))
        stack[indent:] = [line.lstrip()]
        stack_gs.append(stack[:indent+1])
    return stack_gs

def ast(l):
    y = []
    for x in l:
        if(x[-1].find("\t0")>=0):
            y.append(x)
    return y

def values(l):
    y = []
    for x in l:
        v = [pos for pos, char in enumerate(x[-1]) if char=="\t"]
        v = [x[-1][v[-1]+1:]]
        w = [_[:_.find('\t')] for _ in x]
        y.append(w + v)
    return y

def co_to_int (l):
    y = [[0 for i in line] for line in l]
    for i in range(len(l)):
        try:
             for j in range(len(l[-1])):
                 y[i][j] = int(l[i][j])
        except IndexError:
            print('IndexError')
    return y

def build_tree_test(lines):
    lines = iter(lines)
    stack = []
    stack_gs = []
    for line in lines:
        indent = len(list(takewhile(is_tab, line)))
        stack[indent:] = [line.lstrip()]  #u"bergibt  nur speicheradresse
        stack_gs.append(copy.copy(stack)) #es werden Objekte von dieser Adr. gecopiet
    return stack_gs

with open("CH3g1.txt") as f:
    content = f.readlines()
del content[17:23]

content = [line.rstrip() for line in content]

stack_gs = build_tree_test(content)
print pd.DataFrame(stack_gs).transpose()
#stack_gs = build_tree(content)
stack_gs = ast(stack_gs)
stack_gs = values(stack_gs)
stack_gs = co_to_int(stack_gs)
#print stack_gs
print pd.DataFrame(stack_gs).transpose()
