#!/usr/bin/env python3

import ply.yacc as yacc
from lex import tokens
import sys

DEBUG = True

tmp_count = 0
tmp_base = '__tmp'
scope_count = 0
scope_base = '__scope'
code_list = []

SymTab = {}
SymTab['scopes'] = []
SymTab['addr_desc'] = {}

def debug(*args, **kwargs): # Debug
    if DEBUG:
        print(*args, **kwargs)

def eprint(*args, **kwargs): # Print Errors
    print(*args, file=sys.stderr, **kwargs)

# Auxiliary functions

def add_entry(id_name): #, id_type):
    var_entry = dict()
    var_entry['name'] = id_name
    SymTab['addr_desc'][id_name] = var_entry
    SymTab['scopes'][-1]['__variables__'].add(id_name)

def newTemp():
    global tmp_count
    tmp_name = tmp_base + str(tmp_count)
    tmp_count += 1
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
    debug(SymTab['scopes'][-1])
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

def gen(code):
    code_list.append(code)

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
    ''' start : statements'''
    gen("exit")

def p_statements(p):   # it is used as statement*
    ''' statements : statement statements 
                  | empty'''

def p_statement(p):
    ''' statement : singleStatement SemiColon                  
                  | blockStatement'''

def p_singleStatement(p):
    ''' singleStatement : assignmentStatement
                  | reassignmentStatement
                  | functionCall
                  | returnStatement
                  | empty'''

def p_blockStatement(p):
    ''' blockStatement : functionDefinition'''
    pass
    # if else, while, etc. comes here


def p_block(p):
    ''' block : LeftBrace beginBlock statements RightBrace'''
    debug('p_block')
    removeScope()

def p_beginBlock(p):
    ''' beginBlock : empty'''
    addScope()

def p_assignmentStatement(p):
    ''' assignmentStatement : var assignmentList 
                          | assignmentList '''
    if len(p) == 3:
        p[0] = p[2]
        for var in p[0]:
            if inCurScope(var):
                raise RuntimeError("(In code) name '" + var + "' is defined previously")
            add_entry(var)
    else:
        p[0] = p[1]
        for var in p[0]:
            add_entry(var)

def p_assignmentList(p):
    ''' assignmentList : variableAssignment Comma assignmentList 
                                | variableAssignment'''
    if len(p) == 2:
        p[0] = [p[1]]
    else:
        p[0] = [p[1]] + p[3]

def p_variableAssignment(p):
    ''' variableAssignment : Identifier Assign singleExpression'''
    debug('p_variableAssignment')
    p[0] = p[1]
    gen("=, " + p[1] + ", " + p[3]['addr'])

def p_factor(p):
    ''' singleExpression : factor'''
    debug('p_factor')
    p[0] = p[1]

def p_factor_Identifier(p):
    ''' factor : Identifier'''
    debug('p_factor_Identifier')
    if p[-1] and inAllScope(p[1]) == -1:
        raise NameError("(In code) name '" + p[1] + "' is not defined")
    p[0] = {}
    p[0]['addr'] = p[1]


def p_factor_literal(p):
    ''' factor : literal'''
    debug('p_factor_literal')
    p[0] = {}
    p[0]['addr'] = str(p[1])

def p_factor_paranthesis(p):
    ''' factor : LeftParen singleExpression RightParen'''
    debug('p_factor_paranthesis')
    p[0] = {}
    p[0]['addr'] = p[2]['addr']

def p_expression_binary_arith(p):
    ''' singleExpression : singleExpression Plus singleExpression
                         | singleExpression Minus singleExpression
                         | singleExpression Times singleExpression
                         | singleExpression Divide singleExpression
                         | singleExpression Mod singleExpression '''
    debug('p_expression_binary_arith')
    p[0] = {}
    p[0]['addr'] = newTemp()
    gen("=, " + p[0]['addr'] + ", " + p[1]['addr'])
    gen(p[2] + ", " + p[0]['addr'] + ", " + p[3]['addr'])

def p_expression_unary_arith(p):
    ''' singleExpression : Incr singleExpression
                    | Decr singleExpression
                    | Plus singleExpression
                    | Minus singleExpression'''
    debug('p_expression_unary_arith')
    p[0] = {}
    p[0]['addr'] = newTemp()
    if p[1] == '+':
        gen("=, " + p[0]['addr'] + ", " + p[2]['addr'])
    elif p[1] == '-':
        gen("=, " + p[0]['addr'] + ", " + p[2]['addr'])
        gen("*, " + p[0]['addr'] + ", " + "-1")
    elif p[1] == '++':
        gen("+, " + p[2]['addr'] + ", " + "1")
        gen("=, " + p[0]['addr'] + ", " + p[2]['addr'])
    elif p[1] == '--':
        gen("-, " + p[2]['addr'] + ", " + "1")
        gen("=, " + p[0]['addr'] + ", " + p[2]['addr'])

def p_reassignmentStatement(p):
    ''' reassignmentStatement : Identifier PlusEq singleExpression
                           | Identifier MinusEq singleExpression
                           | Identifier MulEq singleExpression
                           | Identifier DivEq singleExpression
                           | Identifier ModEq singleExpression
                           '''
    debug('p_reassignmentStatement')
    add_entry(p[1])
    p[0] = {}
    gen("+, " + p[1] + ", " + p[3]['addr'])


###FUNCTION BLOCK

def p_functionDefinition(p):
    ''' functionDefinition : function Identifier funcDecMarker LeftParen functionParameterList RightParen block'''

def p_funcDecMarker(p):
    '''funcDecMarker : empty'''
    gen('function, '+ p[-1])

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
    debug(p[0])

def p_functionCall(p):
    ''' functionCall : Identifier LeftParen functionParameterList RightParen '''
    gen('call, '+ p[1])

def p_returnStatement(p):
    ''' returnStatement : return
                        | return IdentifierName'''
    if len(p) == 2:
        gen("ret")
    else:
        gen("ret, " + p[2])



def p_identifierName(p):
    ''' IdentifierName : Identifier
                       | arrayLiteral
                       | objectLiteral'''
    p[0] = p[1]

def p_arrayLiteral(p):
    '''arrayLiteral : '''
    #TODO
    pass

def p_objectLiteral(p):
    '''objectLiteral : '''
    #TODO
    pass



def p_DecimalLiteral(p):
    ''' literal : Number'''
    debug('p_DecimalLiteral')
    p[0] = p[1]

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

    with open('tac.ir','w') as fin:
        for code in code_list:
            fin.write(code)
            fin.write('\n')

    debug()
    for code in code_list:
        print(code)

    removeScope()
