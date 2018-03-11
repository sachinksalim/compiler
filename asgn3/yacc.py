import ply.yacc as yacc

from lex import tokens

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

def p_factor_expr(p):
    'factor : LeftParen expression RightParen'
    p[0] = p[2]

# Error rule for syntax errors
def p_error(p):
    print("Syntax error in input!")

# Build the parser
parser = yacc.yacc()

while True:
   try:
       s = input('calc > ')
   except EOFError:
       break
   if not s: continue
   result = parser.parse(s)
   print(result)
