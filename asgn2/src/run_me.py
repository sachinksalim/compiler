#!/usr/bin/python

from tables import *

#
# some definitions

# Operators
arith_ops = ['+', '-', '*', '/', '%']
rel_ops = ['lt', 'leq', 'gt', 'geq', 'eq', 'neq']
logic_ops = ['!', '&&', '||']
operators = arith_ops + rel_ops + logic_ops + ['=']

keywords = ['ifgoto', 'goto', 'ret', 'call', 'print', 'label', 'function', 'exit']

lang = operators + keywords

# Variables
basic_blocks = [] # The list of blocks


def form_blocks(tac):
    basic_blocks = []
    block_leaders = set() # block_leaders stores the line numbers of the block leaders
    block_leaders.add(1)  # since the first line is always a leader
    for line in tac:
        if line[1] == 'call':
            block_leaders.add(int(line[0])+1)
        if line[1] == 'ifgoto':
            block_leaders.add(int(line[5])) # since target of a jump is also a leader
            block_leaders.add(int(line[0])+1) 
        elif line[1] == 'label':
            block_leaders.add(int(line[0]))   
        elif line[1] == 'ret':
            block_leaders.add(int(line[0]))
    block_leaders = list(sorted(block_leaders))
    print(block_leaders)

    new_block = []
    for line in tac:
        new_block.append(line)
        if (int(line[0])+1) in block_leaders:
            basic_blocks.append(new_block)
            new_block = []
    for block in basic_blocks:    
        print (block)
    return basic_blocks

def process(block):
    return

if __name__ == '__main__':
    with open("test.txt") as fp:
        tac = fp.read() # three-address code
    tac = tac.split('\n')

    for i in range(len(tac)):
        tac[i] = tac[i].split(", ")    
    
    basic_blocks = form_blocks(tac)

    for line in tac:
        for word in line:
            if word not in (lang + var_list) and line[1] not in ['label', 'call']:
                try:
                    int(word)
                except:
                    var_list.append(word)
    print(var_list)

    print ('.section .text')
    print ('.global _start')
    print ('_start:')

    inst_no = 1
    for block in basic_blocks:
        if block[0][1] != 'label':
            print ('L' + str(inst_no) + ':')
        process(block)
        inst_no += 1
