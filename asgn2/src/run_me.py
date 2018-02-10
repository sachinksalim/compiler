#!/usr/bin/python

from tables import *

#
# some definitions
DEBUG = True

# Operators
arith_ops = ['+', '-', '*', '/', '%']
rel_ops = ['lt', 'leq', 'gt', 'geq', 'eq', 'neq']
logic_ops = ['!', '&&', '||']
operators = arith_ops + rel_ops + logic_ops + ['=']

non_vars = ['label', 'call']
keywords = ['ifgoto', 'goto', 'ret', 'print', 'function', 'exit'] + non_vars

lang = operators + keywords

# Variables
basic_blocks = [] # The list of blocks


def form_blocks(inst_list):
    basic_blocks = []
    block_leaders = set() # block_leaders stores the line numbers of the block leaders
    block_leaders.add(1)  # since the first line is always a leader
    for line in inst_list:
        if line[1] == 'call':
            block_leaders.add(int(line[0])+1) # next line
        elif line[1] == 'goto':
            block_leaders.add(int(line[-1])) # target of a jump 
        elif line[1] == 'ifgoto':
            block_leaders.add(int(line[-1])) # target of a jump
            block_leaders.add(int(line[0])+1) # next line
        elif line[1] == 'label':
            block_leaders.add(int(line[0])) # current line
        
    block_leaders = list(sorted(block_leaders))
    debug_print("\nBLOCK LEADERS")
    debug_print(block_leaders)

    # Split the Instruction list into basic blocks
    for i in range(len(block_leaders) - 1):
        basic_blocks.append(inst_list[block_leaders[i]-1: block_leaders[i+1]-1])
    basic_blocks.append(inst_list[block_leaders[-1]-1:])  # append the last block
    debug_print("\nBLOCKS")
    for block in basic_blocks:    
        debug_print (block)
    return basic_blocks

def content(block):
    block_var_set = set() # Set of all the variables in the block
    block_var_list_by_line = []  # List of the lists of the variables in each line of the block
    for line in block:
        block_var_list_by_line.append([])
        if line[1] in non_vars:
            continue
        for word in line:
            if word not in lang:
                try:
                    int(word)
                except:
                    block_var_list_by_line[-1].append(word)
                    block_var_set.add(word)
    # print("List:", block_var_list_by_line)       
    return (block_var_set, block_var_list_by_line)

def print_asm(line, symbol_table, line_var_list):
    op = line[1]
    # print ("op: ", op)
    for var in line_var_list:
        var_idx = line_var_list.index(var)
        (in_reg, reg) = get_reg(var, symbol_table)
        if len(line_var_list) > 1:
            if not in_reg:
                print ("\tmovl "+var+", %"+reg)
        line_var_list[var_idx] = '%'+reg

    if op=='=':
        t = line[-1]
        try:
            int(t)
        except:
            t = line_var_list[-1]
        else:
            t = '$'+t            
        print ("\tmovl "+t+", "+ line_var_list[0])

    elif op=='+':
         print ("\taddl "+line_var_list[1]+", "+line_var_list[0]) # need to be updated

def process(block):
    (block_var_set, block_var_list_by_line) = content(block)
    
    for var in block_var_set:
        if var not in addr_desc:
            addr_desc[var] = {'loc': 'mem', 'reg_val': None}

    symbol_table_list = []
    symbol_table = {}
    for var in block_var_set:
        symbol_table[var] = {'state': 'dead', 'prev_use': None, 'next_use': None}

    if not symbol_table: # if symbol table is empty
        for line in block:
            symbol_table_list.append({})
        # symbol_table_list = {}*len(block)
        for i in range(len(block)):
            print_asm(block[i], symbol_table_list[i], block_var_list_by_line[i])
    else:
        for line in reversed(block):
            idx = block.index(line)
            if not block_var_list_by_line[idx]: # if no variable in the current line
                symbol_table_list.insert(0, {})
                continue
            print('....', block_var_list_by_line[idx])
            dest = block_var_list_by_line[idx][0]
            if dest[0] == '$':
                symbol_table[dest]['state'] = 'dead'
            for i in range(1, len(block_var_list_by_line[idx])):
                src = block_var_list_by_line[idx][i]
                if src[0] == '$':
                    if symbol_table[src]['state'] == 'dead':
                        symbol_table[src]['state'] = 'live'
                        symbol_table[src]['prev_use'] = idx
                    symbol_table[src]['next_use'] = idx
            symbol_table_list.insert(0, symbol_table)

    # print('\n\n')
    # print('Block')
    # for i in block:
    #     print('\n',i)
    # print('\nSymbol')
    # for i in symbol_table_list:
    #     print(i)
    # print('\nVar List')
    # for i in block_var_list_by_line:
    #     print(i)
    # print('\n\n')
    debug_print('\n__________________')
    print('\nCURRENT BLOCK')
    print(block)
    for i in range(len(block)):
        print_asm(block[i], symbol_table_list[i], block_var_list_by_line[i])
    debug_print('\nSYMBOL TABLE')
    debug_print(symbol_table)
    debug_print('\nADDRESS DESCRIPTOR')
    debug_print(addr_desc)
    debug_print('\nREGISTER DESCRIPTOR')
    for desc in reg_desc:
        if reg_desc[desc]['content']:
            debug_print((desc, reg_desc[desc]))

def debug_print(s):
    if DEBUG:
        print(s)

if __name__ == '__main__':
    with open("test.txt") as fp:
        inst_list = fp.read().split('\n') # three-address code

    debug_print("INSTRUCTIONS")
    for line in inst_list:
        debug_print(line)
    for i in range(len(inst_list)):
        inst_list[i] = inst_list[i].split(", ")    
    
    basic_blocks = form_blocks(inst_list)

    for line in inst_list:
        for word in line:
            if word not in lang and line[1] not in non_vars:
                try:
                    int(word)
                except:
                    var_set.add(word)
    debug_print("\nALL VARIABLES")
    debug_print(var_set)

    print ('\n\t.section .text')
    print ('\t.global _start')
    print ('_start:')

    inst_no = 1
    for block in basic_blocks:
        # if block[0][1] != 'label':
        #     print ('L' + str(inst_no) + ':', end="")
        process(block)
        inst_no += 1
