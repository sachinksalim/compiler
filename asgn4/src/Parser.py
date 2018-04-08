#!/usr/bin/env python3
from __future__ import print_function
import ply.yacc as yacc
from lex import tokens
import sys

DEBUG = True

tmp_count = 0
tmp_base = '_tmp_'
scope_count = 0
scope_base = '_scope_'
code_list = []
label_count = 0
label_base = '_label_'


SymTab = {}
SymTab['scopes'] = []
SymTab['addr_desc'] = {}

def debug(*args, **kwargs): # Debug
    if DEBUG:
        print(*args, **kwargs)

def eprint(*args, **kwargs): # Print Errors
    print(*args, file=sys.stderr, **kwargs)

# Auxiliary functions

def first_lexeme(p):
    first = 0
    while True:
        try:
            x = p[first]
            if(not x):
                break
            first -= 1
        except:
            break
    return p[first + 1]

def createLabel():
  global label_count, label_base
  label = label_base + str(label_count)
  label_count = label_count + 1
  return label

def add_entry(id_name, id_scope, id_type):
    if id_name in SymTab['scopes'][id_scope]['__variables__']:
        raise RuntimeError("(In code) name '" + id_name + "' is defined previously")
    var_entry = dict()
    var_entry['addr'] = id_name
    var_entry['type'] = id_type
    var_entry['scope'] = id_scope
    SymTab['addr_desc'][id_name] = var_entry
    SymTab['scopes'][id_scope]['__variables__'].add(id_name)
    gen('init', id_name)

def newTemp():
    global tmp_count
    tmp_name = tmp_base + str(tmp_count)
    tmp_count += 1
    gen('init', tmp_name)
    return tmp_name

def addScope(scope_name = ''):
    global scope_count
    if not scope_name:
        scope_name = scope_base + str(scope_count)
    scope_count += 1
    SymTab[scope_name] = {}
    SymTab[scope_name]['__name__'] = scope_name
    SymTab[scope_name]['__level__'] = len(SymTab['scopes'])
    SymTab[scope_name]['__variables__'] = set()
    SymTab[scope_name]['__functions__'] = set()
    SymTab['scopes'].append(SymTab[scope_name])

def removeScope():
    # debug(SymTab['scopes'][-1])
    SymTab['scopes'].pop()

def inAllScope(_id):
    for scope in reversed(SymTab['scopes']):
        if _id in scope['__variables__']:
            return scope['__level__']
    return -1

def inCurScope(_id):
    scope = SymTab['scopes'][-1]
    if _id in scope['__variables__']:
        return True
    return False

def gen(*code):
    code = [str(x) for x in code]
    code_list.append(code)

def process_code():
    ''' Our Codegen script requires all function definitions to occur after all other statements '''
    tmp1 = []
    tmp2 = []
    idx = 0
    print(len(code_list))
    while idx < len(code_list):
        if code_list[idx][0] == 'function':
            while code_list[idx-1][0] != 'ret':
                tmp2.append(code_list[idx])
                idx += 1                
        tmp1.append(code_list[idx])
        idx += 1
    return tmp1 + tmp2

# Precedence and associativity of operators
precedence = (
    ('left', 'Or'),
    ('left', 'And'),
    ('left', 'BinOr'),
    ('left', 'BinXor'),
    ('left', 'BinAnd'),
    ('left', 'Equal', 'NotEqual', 'StrEqual', 'StrNotEqual'),
    ('left', 'GT', 'GTE', 'LT', 'LTE'),
    ('left', 'Rshift', 'Lshift', 'Urshift'),
    ('left', 'Plus', 'Minus'),
    ('left', 'Times', 'Divide', 'Mod'),
    ('right', 'Not', 'BinNot'),
    ('left', 'Dot')
)

# YACC FUNCTIONS

def p_program(p):
    ''' start : prog_startmarker statements'''
    gen("exit")

def p_prog_startmarker(p):
    ''' prog_startmarker : empty '''
    gen("init", "_zero_")
    gen("=", "_zero_", "0")

def p_statements(p):   # it is used as statement*
    ''' statements : statement statements 
                  | empty'''

def p_statement(p):
    ''' statement : singleStatement SemiColon                  
                  | blockStatement'''
    global tmp_count
    tmp_count = 0

def p_singleStatement(p):
    ''' singleStatement : assignmentStatement
                    | declarationStatement
                  | functionCall
                  | returnStatement
                  | printStatement
                  | breakStatement
                  | singleExpression
                  | empty'''

def p_blockStatement(p):
    ''' blockStatement : functionDefinition
                       | ifStatement
                       | ifelseStatement
                       | whileLoop
                       | forLoop
                       | switchStatement'''
    pass
    # if else, while, etc. comes here


def p_block(p):
    ''' block : LeftBrace beginBlock statements RightBrace'''
    debug('p_block')
    removeScope()

def p_beginBlock(p):
    ''' beginBlock : empty'''
    addScope()

# DECLARATION FUNCTIONS

def p_declarationStatement(p):
    ''' declarationStatement : var declarationList'''
    p[0] = p[2]
    for var in p[0]:
        if inCurScope(var['addr']):
            raise RuntimeError("(In code) name '" + var + "' is defined previously")
        add_entry(var['addr'], len(SymTab['scopes'])-1, var['type'])

def p_declarationList(p):
    ''' declarationList : Identifier Comma declarationList 
                                | Identifier'''
    tmp = {}
    tmp['addr'] = p[1]
    tmp['type'] = 'int'
    p[1] = tmp
    if len(p) == 2:
        p[0] = [p[1]]
    else:
        p[0] = [p[1]] + p[3]

# ASSIGNMENT FUNCTIONS

def p_assignmentStatement(p):
    ''' assignmentStatement : var assignmentList 
                          | assignmentList '''
    if len(p) == 3:
        p[0] = p[2]            
    else:
        p[0] = p[1]

def p_assignmentList(p):
    ''' assignmentList : IdentifierName Assign singleExpression Comma assignmentList 
                                | IdentifierName Assign singleExpression'''
    p[0] = {}   
    p[0]['addr'] = p[1]
    p[0]['type'] = p[3]['type']
    if first_lexeme(p) == 'var':
        add_entry(p[0]['addr'], len(SymTab['scopes'])-1, p[0]['type'])
    gen("=", p[1], p[3]['addr'])
    

def p_factor(p):
    ''' singleExpression : factor'''
    debug('p_factor')
    p[0] = p[1]

def p_factor_Identifier(p):
    ''' factor : Identifier'''
    debug('p_factor_Identifier')
    scope_level = inAllScope(p[1])
    if p[-1] and scope_level == -1:
        raise NameError("(In code) name '" + p[1] + "' is not defined")
    p[0] = {}
    p[0]['addr'] = p[1]
    p[0]['type'] = SymTab['addr_desc'][p[1]]['type']


def p_factor_literal(p):
    ''' factor : literal'''
    debug('p_factor_literal')
    p[0] = {}
    p[0] = p[1]

def p_factor_paranthesis(p):
    ''' factor : LeftParen singleExpression RightParen'''
    debug('p_factor_paranthesis')
    p[0] = {}
    p[0]['addr'] = p[2]['addr']
    p[0]['type'] = p[2]['type']

def p_expression_binary_arith(p):
    ''' singleExpression : singleExpression Plus singleExpression
                         | singleExpression Minus singleExpression
                         | singleExpression Times singleExpression
                         | singleExpression Divide singleExpression
                         | singleExpression Mod singleExpression '''
    debug('p_expression_binary_arith')
    p[0] = {}
    if p[1]['type']=='int' and p[3]['type']=='int':
        p[0]['type'] = 'int'
    else:
        if p[1]['type'] != 'int':
            raise TypeError("(In code) %s has a type %s, Expects int" % (p[1]['addr'],p[1]['type']))
        else:
            raise TypeError("(In code) %s has a type %s, Expects int" % (p[3]['addr'],p[3]['type']))

    p[0]['addr'] = newTemp()
    gen("=", p[0]['addr'], p[1]['addr'])
    gen(p[2], p[0]['addr'], p[3]['addr'])

def p_expression_unary_arith(p):
    ''' singleExpression : Plus singleExpression
                    | Minus singleExpression'''
    debug('p_expression_unary_arith')
    p[0] = {}
    p[0]['addr'] = newTemp()
    p[0]['type'] = p[2]['type']
    if p[1] == '+':
        gen("=", p[0]['addr'], p[2]['addr'])
    elif p[1] == '-':        
        gen("=", p[0]['addr'], p[2]['addr'])
        gen("*", p[0]['addr'], "-1")
    

def p_expression_IncrDecr(p):
    ''' singleExpression : singleExpression Incr
                    | singleExpression Decr
                    | Incr singleExpression
                    | Decr singleExpression'''
    debug('p_IncrDecrStatement')
    p[0] = {}
    if p[-1]:
        p[0]['addr'] = newTemp()
    debug('p[-1]: ', p[-1])
    if p[1] in ['++','--']:    
        gen(p[1][0], p[2]['addr'], "1")
        if p[-1]: 
            p[0]['type'] = p[2]['type']
            gen("=", p[0]['addr'], p[2]['addr'])
    elif p[2] in ['++','--']:
        if p[-1]:
            p[0]['type'] = p[1]['type']
            gen("=", p[0]['addr'], p[1]['addr'])
        gen(p[2][0], p[1]['addr'], "1")

def p_reassignmentStatement(p):
    ''' singleExpression : Identifier PlusEq singleExpression
                           | Identifier MinusEq singleExpression
                           | Identifier MulEq singleExpression
                           | Identifier DivEq singleExpression
                           | Identifier ModEq singleExpression
                           '''
    debug('p_reassignmentStatement')
    # add_entry(p[1]['addr'], p[3]['type'])
    p[0] = {}
    gen(p[2][0], p[1], p[3]['addr'])

# BOOLEAN FUNCTIONS

def p_expression_rel_op(p):
    ''' singleExpression : singleExpression LT singleExpression
                         | singleExpression GT singleExpression
                         | singleExpression LTE singleExpression
                         | singleExpression GTE singleExpression
                         | singleExpression Equal singleExpression
                         | singleExpression NotEqual singleExpression '''
    debug('p_expression_rel_op')
    p[0] = {}
    p[0]['addr'] = newTemp()
    p[0]['type'] = 'bool'
    # symb_dict = {
    # '<': 'lt',
    # '>': 'gt',
    # '<=':'leq',
    # '>=':'geq',
    # '==':'eq',
    # '!=':'neq'
    # }
    gen("=", p[0]['addr'], p[1]['addr'])
    gen(p[2], p[0]['addr'], p[3]['addr'])

def p_expression_logical_op(p):
    ''' singleExpression : singleExpression Or singleExpression
                         | singleExpression And singleExpression '''
    p[0] = {}
    if p[1]['type']=='bool' and p[3]['type']=='bool':
        p[0]['type'] = 'bool'
    else:
        if p[1]['type'] != 'bool':
            raise TypeError("(In code) %s has a type %s, Expects bool" % (p[1]['addr'],p[1]['type']))
        else:
            raise TypeError("(In code) %s has a type %s, Expects bool" % (p[3]['addr'],p[3]['type']))
    p[0]['addr'] = newTemp()
    gen("=", p[0]['addr'], p[1]['addr'])
    gen(p[2], p[0]['addr'], p[3]['addr'])

def p_expression_shift(p):
    '''singleExpression : singleExpression Lshift singleExpression
                  | singleExpression Rshift singleExpression
                  | singleExpression Urshift singleExpression'''

def p_breakStatement(p):
    ''' breakStatement : break'''

### IFStatment
def p_ifStatement(p):
    '''ifStatement : if LeftParen singleExpression RightParen ifblock_marker block'''
    gen("label", p[5][1])
    
def p_ifblock_marker(p):
    '''ifblock_marker : empty'''
    label1 = createLabel()
    label2 = createLabel()
    label3 = createLabel()
    p[0] = [label1, label2, label3]
    gen("ifgoto", "neq", "_zero_", p[-2]['addr'], label1)
    gen("goto", label2)
    gen("label", label1)

###########################################################################

### IFELSEStatement

def p_ifelseStatement(p):
    '''ifelseStatement : if LeftParen singleExpression RightParen ifblock_marker block else elseblock_marker block '''
    gen("label", p[5][2])

def p_elseblock_marker(p):
    '''elseblock_marker : empty'''
    gen("goto", p[-3][2])
    gen("label", p[-3][1])

###########################################################################


## WHILELoop

def p_whileLoop(p):
    ''' whileLoop : while start_marker LeftParen singleExpression RightParen condnchk_marker block blockend_marker'''

def p_blockend_marker(p):
    '''blockend_marker : empty'''
    #gen("reached end of while")
    gen("goto", p[-6][0])
    gen("label", p[-6][1])
    
def p_start_marker(p):
    '''start_marker : empty'''
    start = createLabel()
    end = createLabel()
    p[0] = [start, end]
    gen("label", start)

def p_condnchk_marker(p):
    '''condnchk_marker : empty'''
    gen("ifgoto", "eq", "_zero_", p[-2]['addr'], p[-4][1])

################################################################################################

###FORLoop
def p_forLoop(p):
    '''forLoop : for LeftParen assignmentStatement SemiColon forstart_marker singleExpression forcondnchk_marker SemiColon singleExpression increment_marker RightParen block'''
    gen("goto", p[5][3])
    gen("label", p[5][2])
#    removeScope()

def p_forscope_marker(p):
    '''forscope_marker : empty '''
    addScope()

def p_forstart_marker(p):
    '''forstart_marker : empty'''
    label1 = createLabel()
    label2 = createLabel()
    label3 = createLabel()
    label4 = createLabel()
    p[0] = [label1, label2, label3, label4]
    gen("label", label1)

def p_forcondnchk_marker(p):
    '''forcondnchk_marker : empty'''
    gen("ifgoto", "neq", "_zero_", p[-1]['addr'], p[-2][1])
    gen("goto", p[-2][2])
    gen("label", p[-2][3])

def p_increment_marker(p):
    '''increment_marker : empty'''
    gen("goto", p[-5][0])
    gen("label", p[-5][1])

##################################################################################################


### SwitchStatement
switch_var = None
switch_label = None # at the end of the entire switch case

def p_switchStatement(p):
    '''switchStatement : switch LeftParen singleExpression switch_marker RightParen caseBlock_marker caseBlock caseBlockend_marker'''

def p_switch_marker(p):
    '''switch_marker : empty'''
    global switch_var
    #print( "welcome")
    switch_var = p[-1]['addr']
    #print(switch_var)

def p_caseBlockend_marker(p):
    '''caseBlockend_marker : empty '''
    gen("label", p[-2][0])

def p_caseBlock_marker(p):
    '''caseBlock_marker : empty'''
    global switch_label
    label0 = createLabel()
    switch_label = label0
    p[0] = [label0]

def p_caseBlock(p):
    '''caseBlock : LeftBrace caseClause_rs defaultClause RightBrace

        caseClause_rs : caseClause caseClause_rs
                      | empty '''

def p_caseClause(p):
    '''caseClause : case singleExpression casechk_marker Colon statements caseClauseend_marker'''

def p_casechk_marker(p):
    '''casechk_marker : empty'''
    label1 = createLabel()
    p[0] = [label1]
    #print( switch_var )
    gen("ifgoto", "neq" , switch_var , p[-1]['addr'] , label1 )

def p_caseClauseend_marker(p):
    '''caseClauseend_marker : empty'''
    #print("yooooo")
    #print(p[-7])
    gen( "goto", switch_label )  # this gives the label created in caseBlock_marker, the label at the end of the entire switch block
    gen( "label" , p[-3][0] )

def p_defaultClause(p):
    '''defaultClause : default Colon statements'''

##################################################################################################

###FUNCTION BLOCK

def p_functionDefinition(p):
    ''' functionDefinition : function Identifier funcDecMarker LeftParen functionParameterList RightParen block'''

def p_funcDecMarker(p):
    '''funcDecMarker : empty'''
    gen('function', p[-1])

def p_functionParameterList(p):
    ''' functionParameterList : Identifier Comma functionParameterList
                            | Identifier
                            | empty'''
    debug('p_functionParameterList')
    if p[1]:
        p[0] = [p[1]]
    else:
        p[0] = []
    try:
        p[0] += p[3]
    except:
        pass

def p_functionCall(p):
    ''' functionCall : Identifier LeftParen functionParameterList RightParen '''
    gen('call', p[1])

def p_returnStatement(p):
    ''' returnStatement : return
                        | return singleExpression'''
    if len(p) == 2:
        gen("ret")
    else:
        gen("ret", p[2]['addr'])



def p_identifierName(p):
    ''' IdentifierName : Identifier
                       | arrayLiteral
                       | objectLiteral'''
    p[0] = p[1]

def p_arrayLiteral(p):
    ''' arrayLiteral : Identifier LeftBracket singleExpression RightBracket
    | arrayLiteral LeftBracket singleExpression RightBracket'''
    # Second derivation not implemented (2-D matrices)
    p[0] = {}
    p[0]['array'] = p[1]
    p[0]['addr'] = newTemp()
    p[0]['type'] = 'int' # TODO
    gen('A=', p[0]['addr'], p[0]['array'], p[3]['addr'])
    

def p_objectLiteral(p):
    '''objectLiteral : '''
    #TODO
    pass

# PRINT FUNCTION

def p_printStatement(p):
    '''printStatement : print LeftParen singleExpression RightParen'''
    gen('print', p[3]['type'], p[3]['addr'])


def p_DecimalLiteral(p):
    ''' literal : Number'''
    debug('p_DecimalLiteral')
    p[0] = {}
    p[0]['addr'] = str(p[1])
    p[0]['type'] = 'int'

def p_StringLiteral(p):
    ''' literal : String'''
    debug('p_StringLiteral')
    p[0] = {}
    p[0]['addr'] = p[1]
    if len(p[1]) == 1:
        p[0]['type'] = 'chr'
    else:
        p[0]['type'] = 'str'

def p_BooleanLiteral(p):
    ''' literal : true
                | false'''
    debug('p_BooleanLiteral')
    p[0] = {}
    p[0]['addr'] = p[1]
    p[0]['type'] = 'bool'

def p_empty(p):
    ''' empty :'''
    pass

# Error rule for syntax errors
def p_error(p):
    if p:
        raise SyntaxError("(In code) at '%s'" % p.value)
    else:
        raise SyntaxError("(In code) at EOF")

def read_data(filename):
    fp = open(filename, 'r')
    data = fp.read()
    fp.close()
    return data

if __name__ == '__main__':
    if len(sys.argv) < 2:
        print('Insufficient arguments!')
        print('Format: python yacc.py test.js')
        sys.exit(1)

    addScope('main')

    filename = sys.argv[1]
    data = read_data(filename)
    parser = yacc.yacc(debug=True, optimize=False)
    # result = parser.parse(data, debug=2)
    result = parser.parse(data)

    code_list = process_code()

    with open('tac.ir','w') as fin:
        for code in code_list:
            fin.write(", ".join(code))
            fin.write('\n')
  
    
    debug('\n\nCODE')
    for code in code_list:
        print(code)

    removeScope()
