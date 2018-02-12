#!/usr/bin/python

from tables import *
import copy
import sys

DEBUG = False

# Operators
arith_ops = ['+', '-', '*', '/', '%']
rel_ops = ['lt', 'leq', 'gt', 'geq', 'eq', 'neq']
logic_ops = ['!', '&&', '||']
operators = arith_ops + rel_ops + logic_ops + ['=']

non_vars = ['label', 'call']
keywords = ['ifgoto', 'goto', 'ret', 'print', 'exit'] + non_vars

label_ids = set()

lang = operators + keywords

# Variables
basic_blocks = [] # The list of blocks

print_exit = '\nend_label:\n\
    movl $1, %eax\n\
    movl $0, %ebx\n\
    int $0x80'

def form_blocks(inst_list):
    basic_blocks = []
    block_leaders = set() # block_leaders stores the line numbers of the block leaders
    block_leaders.add(1)  # since the first line is always a leader
    for line in inst_list:
        if line[1] in ['call', 'ifgoto']:
            label_ids.add(line[-1])
            block_leaders.add(int(line[0])+1) # next line
        elif line[1] == 'label':
            block_leaders.add(int(line[0])) # current line
            label_ids.add(line[-1])
    
    # print(lang)   
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
    bad_ops = ['/', '%', 'ret', 'call', 'print', 'exit']

    line_reg_list = []
    debug_print(line)
    if op not in bad_ops:
        for var in line_var_list:
            (in_reg, reg) = get_reg(var, symbol_table)
            if len(line_var_list) > 1:
                if not in_reg:
                    print ("\tmovl "+var+", %"+reg)
            line_reg_list.append('%'+reg)


        if op == '=':
            t = line[-1]
            try:
                int(t)
            except:
                t = line_reg_list[-1]
            else:
                t = '$'+t            
            print ("\tmovl "+t+", "+ line_reg_list[0])

        elif op == 'label':
            print ( "\n" + line[2]+":")
        elif op == '!':     # logical not operation
            print ("\tnotl "+line_reg_list[0])
        elif op == '+':
             print ("\taddl "+line_reg_list[1]+", "+line_reg_list[0])
        elif op == '-':
            print ("\tsubl "+line_reg_list[1]+", "+line_reg_list[0])
        elif op == '*':
            print ("\timul "+line_reg_list[1]+", "+line_reg_list[0])
        elif op == 'goto':
            print ("\tjmp "+ line[2])
        elif op == '&&':    # 'and' operator    
            print ("\tandl "+line_reg_list[1]+", "+line_reg_list[0])
        elif op == '||':    # 'or' operator    
            print ("\torl "+line_reg_list[1]+", "+line_reg_list[0])
        elif op == 'ifgoto':
            print ("\tcmp "+line_reg_list[1]+", "+line_reg_list[0])
            if line[2] == 'lt':
                print ("\tjl ", end = "")
            elif line[2] == 'leq':
                print ("\tjle ", end = "")
            elif line[2] == 'gt':
                print ("\tjg ", end = "")
            elif line[2] == 'geq':
                print ("\tjge ", end = "")
            elif line[2] == 'eq':
                print ("\tje ", end = "")
            elif line[2] == 'neq':
                print ("\tjne ", end = "")
            else:
                print ("No other rel operators!\n")
            print(line[5])
        else:
            print ('Invaid operator: '+op+'\n')
        return
    # ''' elif op == 'call':
    #     free_reg()
    #     print ("\tcall "+line[2])
    #     if len(line_reg_list)!=0:
    #         print ("movl %eax, "+line_reg_list[0])
    # '''
    elif op == 'exit':
        print(print_exit)
    elif op == 'call':
        print ("\tcall "+line[2])
    elif op == 'ret':
        if line_var_list:
            var = line_var_list[0]
            if reg_desc[var]['loc'] != 'reg' or reg_desc[var]['reg_val'] != 'eax':
                movex86('eax', reg_desc['eax']['content'], 'R2M')
                if reg_desc[var]['loc'] == 'mem':
                    movex86(var, 'eax', 'M2R')
                else:
                    movex86(reg_desc[var]['reg_val'], 'eax', 'R2R')
        print ("\tret")
    elif op == 'print':
            var = line_var_list[0] # var stores the var whose value is to be printed
            var_reg = addr_desc[var]['reg_val'] # var_reg : its corresponding register
            # for print we would need to do
            # movl $4, %eax
            # movl $1, %ebx
            # and move the contents of the register to be printed to ecx
            # so lets just free all the registers
            temp_print = []
            for reg in reg_list:
                if reg_desc[reg]['state'] == 'loaded':
                    src = reg
                    dest = reg_desc[reg]['content']
                    print ("\tmovl %"+src+', '+dest)
                    temp_print.append((src,dest))
                    reg_desc[src]['state'] = 'empty'
                    reg_desc[src]['content'] = None
                    addr_desc[dest]['loc'] = 'mem'
                    addr_desc[dest]['reg_val'] = None
            # lets push the value of the variable onto the stack
            print ('\tpushl '+var)
            print ('\tcall __printInt')
            print ('\tpopl ' +var)

            for x in temp_print:
                src = x[1]
                dest_reg = x[0]
                print ("\tmovl "+src+', %'+dest_reg)
                reg_desc[dest_reg]['state'] = 'loaded'
                reg_desc[dest_reg]['content'] = src
                addr_desc[src]['loc'] = 'reg'
                addr_desc[src]['reg_val'] = dest_reg


    elif op in ['/', '%']:
        dividend = line_var_list[0]
        divisor = line_var_list[1]
        if addr_desc[dividend]['loc'] == 'mem':
            if reg_desc['eax']['state'] != 'empty':
                movex86('eax', reg_desc['eax']['content'], 'R2M')
            movex86(dividend, 'eax', 'M2R')
        else:
            if addr_desc[dividend]['reg_val'] != 'eax':
                if reg_desc['eax']['state'] != 'empty':
                    movex86('eax', reg_desc['eax']['content'], 'R2M')
                movex86(addr_desc[dividend]['reg_val'], 'eax', 'R2R')

        if reg_desc['edx']['state'] == 'loaded':
           movex86('edx', reg_desc['edx']['content'], 'R2M')
        print ("\tmovl $0, %edx")
        (in_reg, reg) = get_reg(divisor, symbol_table)
        if not in_reg:
            print ("\tmovl "+divisor+", %"+reg)
        line_reg_list.append('%'+reg)
        print ("\tdivl "+line_reg_list[0])

        if op == '/':
            reg_desc['edx']['state'] = 'empty'
            reg_desc['edx']['content'] = None
            reg_desc['eax']['state'] = 'loaded'
            reg_desc['eax']['content'] = dividend
            addr_desc[dividend]['loc'] = 'reg'
            addr_desc[dividend]['reg_val'] = 'eax'
        else:
            reg_desc['eax']['state'] = 'empty'
            reg_desc['eax']['content'] = None
            reg_desc['edx']['state'] = 'loaded'
            reg_desc['edx']['content'] = dividend
            addr_desc[dividend]['loc'] = 'reg'
            addr_desc[dividend]['reg_val'] = 'edx'


def process(block):
    (block_var_set, block_var_list_by_line) = content(block)
    
    for var in block_var_set:
        if var not in addr_desc:
            addr_desc[var] = {'loc': 'mem', 'reg_val': None}

    symbol_table_list = []
    symbol_table = {}
    for var in block_var_set:
        symbol_table[var] = {'state': 'dead', 'next_use': None}

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
            dest = block_var_list_by_line[idx][0]
            symbol_table[dest]['state'] = 'dead'
            start_idx = 0
            if line[1] == '=':
                start_idx = 1
            for i in range(start_idx, len(block_var_list_by_line[idx])):
                src = block_var_list_by_line[idx][i]
                symbol_table[src]['state'] = 'live'
                symbol_table[src]['next_use'] = idx
            symbol_table_list.insert(0, copy.deepcopy(symbol_table)) # inserts a copy of symbol table to the list

    debug_print('\n____________________________________', 1) 
    if symbol_table:
        for i in range(len(block)):
            debug_print('\t.............', 1)
            print_asm(block[i], symbol_table_list[i], block_var_list_by_line[i])

    debug_print('\nCURRENT BLOCK', 1)
    debug_print(block, 1)
    debug_print('\nSYMBOL TABLE LIST', 1)
    for symbol_table in symbol_table_list:
        debug_print(symbol_table, 1)
    debug_print('\nADDRESS DESCRIPTOR', 1)
    debug_print(addr_desc, 1)
    debug_print('\nREGISTER DESCRIPTOR', 1)
    for desc in reg_desc:
        if reg_desc[desc]['content']:
            debug_print((desc, reg_desc[desc]), 1)

def debug_print(s, level = 0):
    if DEBUG:
        if level > 0:
            print(s)

if __name__ == '__main__':
    ir_filename = sys.argv[1]
    with open(ir_filename) as fp:
        inst_list = fp.read().split('\n') # three-address code

    debug_print("INSTRUCTIONS")
    for line in inst_list:
        debug_print(line)
    for i in range(len(inst_list)):
        inst_list[i] = inst_list[i].split(", ")
        inst_list[i].insert(0, str(i+1)) # add line number
    
    basic_blocks = form_blocks(inst_list)

    lang += list(label_ids)

    for line in inst_list:
        for word in line:
            if word not in lang and line[1] not in non_vars:
                try:
                    int(word)
                except:
                    var_set.add(word)
    debug_print("\nALL VARIABLES")
    debug_print(var_set)

    print ('\t.section .text\n')
    print ('\t.global _start\n')
    print ('_start:')

    inst_no = 1
    for block in basic_blocks:
        # if block[0][1] != 'label':
        #     print ('L' + str(inst_no) + ':', end="")
        process(block)
        inst_no += 1
    
    print_int = '\n__printInt:\n\
    movl 4(%esp), %ecx\n\
    cmpl $0, %ecx\n\
    jge __positive\n\
    notl %ecx\n\
    inc %ecx\n\
    movl %ecx, %edi\n\
    movl $45, %eax\n\
    pushl   %eax\n\
    movl $4, %eax\n\
    movl $1, %ebx\n\
    movl %esp, %ecx\n\
    movl $1, %edx\n\
    int $0x80\n\
    popl %eax\n\
    movl %edi, %ecx\n\n\
__positive:\n\
    movl %ecx, %eax\n\
    movl %esp, %esi\n\n\
__iterate:\n\
    cdq\n\
    movl $10, %ebx\n\
    idivl %ebx\n\
    pushl %edx\n\
    cmpl $0, %eax\n\
    jne __iterate\n\
    jmp __printNum\n\
    \n\
__printNum:\n\
    popl %edx\n\
    addl $48, %edx\n\
    pushl %edx\n\
    movl $4, %eax\n\
    movl $1, %ebx\n\
    movl %esp, %ecx\n\
    movl $1, %edx\n\
    int $0x80\n\
    popl %edx\n\
    cmp %esp, %esi\n\
    jne __printNum\n\
    movl $4, %eax\n\
    movl $1, %ebx\n\
    movl $new, %ecx\n\
    movl $1, %edx\n\
    int $0x80\n\
    ret  \n\n'

    print(print_int)
    print ('\t.section .data')
    for word in var_set:
        print (word+":\t.long 0")
    print ('new:')
    print ('\t.ascii "\\n"')
