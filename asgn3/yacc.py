import ply.yacc as yacc

from lex import tokens

import sys

def p_program(p):
    'start : statements'

def p_statements(p):
    '''statements : statement statements 
    | statement'''

def p_statement(p):
    '''statement : variableStatement 
    | expressionStatement
    | printStatement
    | SemiColon'''

def p_variableStatement(p):
    '''variableStatement : var variableDeclarationList SemiColon
    | variableDeclarationList SemiColon'''

def p_variableDeclarationList(p):
    '''variableDeclarationList : variableDeclaration Comma variableDeclarationList 
    | variableDeclaration'''

def p_variableDeclaration(p):
    '''variableDeclaration : Identifier 
    | Identifier Assign singleExpression'''

def p_expressionStatement(p):
    'expressionStatement : expressionSequence SemiColon'

def p_expressionSequence(p):
    '''expressionSequence : singleExpression Comma expressionSequence 
    | singleExpression'''

def p_singleExpression(p):
    'singleExpression : expression'

def p_printStatement(p):
    'printStatement : console Dot log LeftParen factor RightParen'

def p_expression_plus(p):
    'expression : expression Plus term'
    p[0] = p[1] + p[3]

def p_expression_minus(p):
    'expression : expression Minus term'
    p[0] = p[1] - p[3]

def p_expression_term(p):
    'expression : term'
    p[0] = p[1]

def p_term_times(p):
    'term : term Times factor'
    p[0] = p[1] * p[3]

def p_term_div(p):
    'term : term Divide factor'
    p[0] = p[1] / p[3]

def p_term_factor(p):
    'term : factor'
    p[0] = p[1]

def p_factor_num(p):
    'factor : Number'
    p[0] = p[1]

def p_factor_id(p):
    'factor : Identifier'
    p[0] = p[1]

def p_factor_expr(p):
    'factor : LeftParen expression RightParen'
    p[0] = p[2]

def p_expression_name(p):
    "expression : Identifier"
    try:
        p[0] = names[p[1]]
    except LookupError:
        print("Undefined name '%s'" % p[1])
        p[0] = 0

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
        sys.exit()
    filename = sys.argv[1]
    data = read_data(filename)
    parser = yacc.yacc(debug=True, optimize=False)
    result = parser.parse(data, debug=2)
