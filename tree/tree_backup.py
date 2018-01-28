import numpy as np
import pandas as pd
from itertools import takewhile

is_tab = '\t'.__eq__

def build_tree(lines):
    lines = iter(lines)
    stack = []
    stack_gs = []
    count = 0
    for line in lines:
        indent = len(list(takewhile(is_tab, line)))
#        stack.append(line.lstrip())
        stack[indent:] = [line.lstrip()]
        stack_gs.append(stack[:indent+1])
    print(stack_gs)
    return stack_gs

def ast(l):
    y = []
    for x in l:
        if(x[-1].find("\t0")>=0):
            y.append(x)
            print(x)
    return y

#def values(l):
#    for 

with open("CH3g1.txt") as f:
    content = f.readlines()
del content[17:23]

content = [line.rstrip() for line in content]


stack_gs = build_tree(content)

stack_gs = ast(stack_gs)
print(stack_gs)

#print [len(line) for line in stack_gs]
#df_np = [(map(int, line.split())) for line in content]
##df_np = [line + [0] for line in df_np if len(line) < 3]
#df_np = [line + [0] if len(line) < 3 else line for line in df_np]
#lst_ge = []
#for lines in df_np:
#    lst = [abs(number) for number in lines]
#    lst_ge.append(lst)
#    print(lst)
#print('bla')


#df_np = np.vstack(df_np)
#df_np = np.abs(df_np)


