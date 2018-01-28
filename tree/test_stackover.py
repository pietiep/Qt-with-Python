from itertools import takewhile

is_tab = '\t'.__eq__

def build_tree(lines):
    lines = iter(lines)
    stack = []
    for line in lines:
        indent = len(list(takewhile(is_tab, line)))
        stack[indent:] = [line.lstrip()]
        print stack

source = '''ROOT
\tNode1
\t\tNode2
\t\t\tNode3
\t\t\t\tNode4
\tNode5
\tNode6'''

print(source.split('\n'))
build_tree(source.split('\n'))

