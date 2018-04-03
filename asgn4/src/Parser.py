#!/usr/bin/env python3

import ply.yacc as yacc
from lex import tokens
import sys

DEBUG = True

tmp_count = 0
tmp_base = 'tmp'
scope_count = 0
scope_base = 'scope'
code_list = []

ST = {}
ST['scopes'] = []
ST['addr_desc'] = {}

def debug(*args, **kwargs): # Debug
    if DEBUG:
        print(*args, **kwargs)

# Auxiliary functions

def add_entry(id_name): #, id_type):
    var_entry = dict()
    var_entry['name'] = id_name
    # var_entry['type'] = id_type
    # var_entry['offset'] = id_offset

    ST['addr_desc'][id_name] = var_entry
    ST['scopes'][-1]['__variables__'].append(id_name)

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
    ST[scope_name] = {}
    ST[scope_name]['__name__'] = scope_name
    ST[scope_name]['__level__'] = len(ST['scopes'])
    ST[scope_name]['__variables__'] = []
    ST[scope_name]['__functions__'] = []
    ST['scopes'].append(ST[scope_name])

def removeScope():
    ST['scopes'].pop()

def gen(code):
    code_list.append(code)
    return code

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
    ''' start : block
                | statements'''

def p_statements(p):   # it is used as statement*
    ''' statements : statement statements 
                   | empty'''

def p_statement(p):
    ''' statement : SemiColon
                  | assignmentStatement SemiColon
                  | reassignmentStatement SemiColon'''

def p_block(p):
    ''' block : LeftBrace beginBlock statements RightBrace'''
    removeScope()

def p_beginBlock(p):
    ''' beginBlock : empty'''
    addScope()

def p_assignmentStatement(p):
    ''' assignmentStatement : var assignmentList 
                          | assignmentList '''

def p_assignmentList(p):
    ''' assignmentList : variableAssignment Comma assignmentList 
                                | variableAssignment'''

def p_variableAssignment(p):
    ''' variableAssignment : Identifier Assign singleExpression'''
    debug('p_variableAssignment')
    add_entry(p[1])
    p[0] = {}
    p[0]['code'] = p[3]['code'] + gen("=, " + p[1] + ", " + p[3]['addr'])

def p_factor(p):
    ''' singleExpression : factor'''
    debug('p_factor')
    p[0] = p[1]

def p_factor_Identifier(p):
    ''' factor : Identifier'''
    debug('p_factor_Identifier')
    p[0] = {}
    p[0]['addr'] = p[1]
    p[0]['code'] = ''

def p_factor_literal(p):
    ''' factor : literal'''
    debug('p_factor_literal')
    p[0] = {}
    p[0]['addr'] = str(p[1])
    p[0]['code'] = ''

def p_factor_paranthesis(p):
    ''' factor : LeftParen singleExpression RightParen'''
    debug('p_factor_paranthesis')
    p[0] = {}
    p[0]['addr'] = p[2]['addr']
    p[0]['code'] = p[2]['code']

def p_expression_binary_arith(p):
    ''' singleExpression : singleExpression Plus singleExpression
                         | singleExpression Minus singleExpression
                         | singleExpression Times singleExpression
                         | singleExpression Divide singleExpression
                         | singleExpression Mod singleExpression '''
    debug('p_expression_binary_arith')
    p[0] = {}
    p[0]['addr'] = newTemp()
    p[0]['code'] = p[1]['code'] + p[3]['code']
    p[0]['code'] += gen("=, " + p[0]['addr'] + ", " + p[1]['addr'])
    p[0]['code'] += gen(p[2] + ", " + p[0]['addr'] + ", " + p[3]['addr'])

def p_expression_unary_arith(p):
    ''' singleExpression : Incr singleExpression
                    | Decr singleExpression
                    | Plus singleExpression
                    | Minus singleExpression'''
    debug('p_expression_unary_arith')
    p[0] = {}
    p[0]['addr'] = newTemp()
    p[0]['code'] = p[2]['code']
    if p[1] == '+':
        p[0]['code'] += gen("=, " + p[0]['addr'] + ", " + p[2]['addr'])
    elif p[1] == '-':
        p[0]['code'] += gen("=, " + p[0]['addr'] + ", " + p[2]['addr'])
        p[0]['code'] += gen("*, " + p[0]['addr'] + ", " + "-1")
    elif p[1] == '++':
        p[0]['code'] += gen("+, " + p[2]['addr'] + ", " + "1")
        p[0]['code'] += gen("=, " + p[0]['addr'] + ", " + p[2]['addr'])
    elif p[1] == '--':
        p[0]['code'] += gen("-, " + p[2]['addr'] + ", " + "1")
        p[0]['code'] += gen("=, " + p[0]['addr'] + ", " + p[2]['addr'])

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
    p[0]['code'] = p[3]['code'] + gen("+, " + p[1] + ", " + p[3]['addr'])

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
        print("Syntax error at '%s'" % p.value)
    else:
        print("Syntax error at EOF")

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
    fpw = open('tac.ir','w')
    parser = yacc.yacc(debug=True, optimize=False)
    # result = parser.parse(data, debug=2)
    result = parser.parse(data)
    debug()
    for scope in ST['scopes']:
        debug(scope)
    debug()
    for code in code_list:
        print(code)
