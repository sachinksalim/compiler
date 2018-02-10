# Register Descriptor
# Keep track of what is currently in each register.
# Initially all the registers are empty
reg_desc = {}

# Tuple of all the registers in X86
# reg_list = ('eax', 'ebx', 'ecx', 'edx', 'esi', 'edi', 'ebp', 'esp')
reg_list = ('eax', 'ebx')
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
    print('\n\n\n\n\n..............')
    reg = farthest_use['reg']

    print ("\tmovl %" + str(reg) + ", " + str(farthest_use['var']))
    
    addr_desc[var]['loc'] = 'reg'
    addr_desc[var]['reg_val'] = reg
    reg_desc[reg]['state'] = 'loaded'
    reg_desc[reg]['var'] = var
    return (False, reg)
