#!/usr/bin/python

# some imports

#
# some definitions

def main():
    fp = open("test.txt")
    tac = fp.read() # three-address code
    tac = tac.split('\n')
    num_lines_tac  = len(tac)
    for i in range(len(tac)):
        tac[i] = tac[i].split(", ")
    print(tac)
## start segregating the basic blocks  ##
## first find the block leaders ##
# for call=goto, ifgoto, label, ret#
## according to wikipedia, definition of a leader:
#   1)The first instruction is a leader.
#   2)The target of a conditional or an unconditional goto/jump instruction is a leader.
#   3)The instruction that immediately follows a conditional goto/jump instruction is a leader.
    block_leaders = set() # block_leaders stores the line numbers of the block leaders
    block_leaders.add(1)  # sinc ethe first line is always a leader
    for line in tac:
#       if tac[i][1] == 'call':
#           print tac[i][0]
#           block_leaders.add(int(tac[i][0])+1)
        if line[1] == 'ifgoto':
            block_leaders.add(int(line[5])) # since target of a jump is also a leader
            block_leaders.add(int(line[0])+1) 
        elif line[1] == 'label':
            block_leaders.add(int(line[0]))   
        elif line[1] == 'ret':
            block_leaders.add(int(line[0]))
    sorted(block_leaders)
    print(block_leaders)
    fp.close()

if __name__ == '__main__':
    main()
