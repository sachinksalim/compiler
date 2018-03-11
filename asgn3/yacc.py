import ply.yacc as yacc

from lex import tokens

import sys

# def p_start(p):
#     'start : statements'

# def p_statements(p):
#     '''statements : statement statements 
#     | statement'''

# def p_statement(p):
#     '''statement : variableStatement 
#     | expressionStatement'''

# def p_variableStatement(p):
#     'variableStatement : var variableDeclarationList SemiColon'

# def p_variableDeclarationList(p):
#     '''variableDeclarationList : variableDeclaration Comma variableDeclarationList 
#     | variableDeclaration'''

# def p_variableDeclaration(p):
#     '''variableDeclaration : Identifier 
#     | Identifier Assign singleExpression'''

# def p_expressionStatement(p):
#     'expressionStatement : expressionSequence SemiColon'

# def p_expressionSequence(p):
#     '''expressionSequence : singleExpression Comma expressionSequence 
#     | singleExpression'''

# def p_singleExpression(p):
#     'singleExpression : expression'

# dictionary of names
names = {}

def p_assignment(p):
    'statement : Identifier Assign expression'
    fp_out.write(p_assignment.__doc__ + '\n')
    names[p[1]] = p[3]

def p_statement(p):
    'statement : expression'
    fp_out.write(p_statement.__doc__ + '\n')
    print(p[1])

def p_statement(p):
    'statement : printStatement'
    fp_out.write(p_statement.__doc__ + '\n')

def p_printStatement(p):
    'printStatement : console Dot log LeftParen factor RightParen'
    fp_out.write(p_printStatement.__doc__ + '\n')

def p_expression_plus(p):
    'expression : expression Plus term'
    fp_out.write(p_expression_plus.__doc__ + '\n')
    p[0] = p[1] + p[3]

def p_expression_minus(p):
    'expression : expression Minus term'
    fp_out.write(p_expression_minus.__doc__ + '\n')
    p[0] = p[1] - p[3]

def p_expression_term(p):
    'expression : term'
    fp_out.write(p_expression_term.__doc__ + '\n')
    p[0] = p[1]

def p_term_times(p):
    'term : term Times factor'
    fp_out.write(p_term_times.__doc__ + '\n')
    p[0] = p[1] * p[3]

def p_term_div(p):
    'term : term Divide factor'
    fp_out.write(p_term_div.__doc__ + '\n')
    p[0] = p[1] / p[3]

def p_term_factor(p):
    'term : factor'
    fp_out.write(p_term_factor.__doc__ + '\n')
    p[0] = p[1]

def p_factor_num(p):
    'factor : Number'
    fp_out.write(p_factor_num.__doc__ + '\n')
    p[0] = p[1]

def p_factor_id(p):
    'factor : Identifier'
    fp_out.write(p_factor_id.__doc__ + '\n')
    p[0] = p[1]

def p_factor_expr(p):
    'factor : LeftParen expression RightParen'
    fp_out.write(p_factor_expr.__doc__ + '\n')
    p[0] = p[2]

def p_expression_name(p):
    "expression : Identifier"
    fp_out.write(p_expression_name.__doc__ + '\n')
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
    data = fp.read().split('\n')
    fp.close()
    return data

if __name__ == '__main__':
    if len(sys.argv) < 2:
        print('Insufficient arguments!')
        print('Format: python yacc.py test.js')
        sys.exit()
    filename = sys.argv[1]
    data = read_data(filename)
    out_filename = filename.split('.')[0] + '.html'
    fp_out = open(out_filename, 'w')
    parser = yacc.yacc()
    for statement in data:
        result = parser.parse(statement)
    fp_out.close()

    # Build the parser
    # parser = yacc.yacc()

    # while True:
    #     try:
    #        s = input('calc > ')
    #     except EOFError:
    #        break
    #     if not s: continue
    #     result = parser.parse(s)
