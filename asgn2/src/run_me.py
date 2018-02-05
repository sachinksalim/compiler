#!/usr/bin/python

from tables import *

#
# some definitions

# Operators
arith_ops = ['+', '-', '*', '/', '%']
rel_ops = ['<', '<=', '>', '>=', '==', '!=']
logic_ops = ['!', '&&', '||']

keywords = ['ifgoto', 'goto', 'return', 'call', 'print', 'label', '=', 'function', 'exit']

def main():
    with open("test.txt") as fp:
        tac = fp.read() # three-address code
    tac = tac.split('\n')

    for i in range(len(tac)):
        tac[i] = tac[i].split(", ")
    # print(tac)
###############################################################
#                   Block leaders
################################################################
# for call=goto, ifgoto, label, ret#
## according to wikipedia, definition of a leader:
#   1)The first instruction is a leader.
#   2)The target of a conditional or an unconditional goto/jump instruction is a leader.
#   3)The instruction that immediately follows a conditional goto/jump instruction is a leader.
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
############################################################
# lets now build the basic blocks
### lets just put a special character '$' just before a block leader
    basic_blocks = []
    for line in tac:
        if int(line[0]) in block_leaders:
            basic_blocks.append('$')
        basic_blocks.append(line)
    print (basic_blocks)
# we have finished seperating the basic blocks by '$'
################################################################

if __name__ == '__main__':
    main()
