# Register Descriptor
# Stores the variable identifier currently in each register.
# Initially all the registers are empty
reg_desc = {}

# Tuple of all the registers in X86
reg_list = ('eax', 'ebx', 'ecx', 'edx', 'esi', 'edi')
var_set = set() # Set of all variables

for reg in reg_list:
    reg_desc[reg] = {'state': 'empty', 'content': None}

# Address Descriptor
# Keep track of location where current value of the name can be found at runtime
# The location might be a register, stack, memory address or a set of those
addr_desc = {} 

def find_farthest_use(symbol_table):
    farthest_use = {'idx': -1, 'var': '', 'reg': 0}
    for reg in reg_list:
        var = reg_desc[reg]['content']
        if var not in symbol_table or symbol_table[var]['state'] == 'dead':
            farthest_use['reg'] = reg
            farthest_use['var'] = var
        else:
            farthest_use['idx'] = max(farthest_use['idx'],symbol_table[var]['next_use'])
    return farthest_use

def get_reg(var, symbol_table):
    if addr_desc[var]['loc'] == 'reg': # If var is in register
        return (True, addr_desc[var]['reg_val']) # Return register of var

    for reg in reg_list:
        if reg_desc[reg]['state'] == 'empty':
            reg_desc[reg]['state'] = 'loaded'
            reg_desc[reg]['content'] = var
            addr_desc[var]['loc'] = 'reg'
            addr_desc[var]['reg_val'] = reg
            return (False, reg) # Return empty register of var


    farthest_use = find_farthest_use(symbol_table)
    # print ('FARTHEST USE', farthest_use)
    reg = farthest_use['reg']

    print ("\tmovl %" + str(reg) + ", " + str(farthest_use['var']))
    addr_desc[farthest_use['var']]['loc'] = 'mem'
    addr_desc[farthest_use['var']]['reg_val'] = None
    addr_desc[var]['loc'] = 'reg'
    addr_desc[var]['reg_val'] = reg
    reg_desc[reg]['state'] = 'loaded'
    reg_desc[reg]['content'] = var
    return (False, reg)

def movex86(src, dest, flag = 'R2R'):
    if flag == 'R2R':
        print ("\tmovl %"+src+', %'+dest)
        if reg_desc[dest]['state'] == 'loaded':
            addr_desc[reg_desc[dest]['content']]['reg_val'] = None
        reg_desc[dest]['state'] = 'loaded'
        reg_desc[dest]['content'] = reg_desc[src]['content']
        reg_desc[src]['state'] = 'empty'
        reg_desc[src]['content'] = None
        addr_desc[reg_desc[dest]['content']]['reg_val'] = dest

    elif flag == 'R2M':
        print ("\tmovl %"+src+', '+dest)
        reg_desc[src]['state'] = 'empty'
        reg_desc[src]['content'] = None
        addr_desc[dest]['loc'] = 'mem'
        addr_desc[dest]['reg_val'] = None

    elif flag == 'M2R':
        print ("\tmovl "+src+', %'+dest)
        if reg_desc[dest]['state'] == 'loaded':
            addr_desc[reg_desc[dest]['content']]['reg_val'] = None
        reg_desc[dest]['state'] = 'loaded'
        reg_desc[dest]['content'] = src
        addr_desc[src]['loc'] = 'reg'
        addr_desc[src]['reg_val'] = dest

    else:
        print('Invalid Flag!')

def free_all_registers():
    for reg in reg_list:
        if reg_desc[reg]['state'] == 'loaded':
            var = reg_desc[reg]['content']
            movex86(reg, var, 'R2M')
