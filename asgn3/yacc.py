import ply.yacc as yacc

from lex import tokens

import sys

def p_program(p):
    'start : statements'

def p_statements(p):
    '''statements   : statement statements 
                    | statement'''

def p_statement(p):
    '''statement    : block 
                    | SemiColon
                    | variableStatement 
                    | expressionStatement
                    | ifStatement
                    | iterationStatement
                    | continueStatement
                    | breakStatement
                    | returnStatement
                    | withStatement
                    | switchStatement
                    | printStatement'''
                    # functionDeclaration is needed to look because it contains many deleted rules

def p_block(p):
    'block  : LeftBrace statements RightBrace'

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

def p_ifStatement(p):
    ''' ifStatement : if LeftParen expressionSequence RightParen statement
                    | if LeftParen expressionSequence RightParen statement else statement'''

def p_iterationStatement(p):
    ''' iterationStatement  : do statement while LeftParen expressionSequence RightParen SemiColon
                            | while LeftParen expressionSequence RightParen statement
                            | for LeftParen singleExpression in expressionSequence RightParen statement
                            | for LeftParen var variableDeclaration in expressionSequence RightParen statement'''
                         # doubt here   
                         #   | for LeftParen expressionSequence? SemiColon expressionsequence? SemiColon expressionsequence? RightParen statement
                         #   | for LeftParen var variabledeclarationlist SemiColon expressionsequence? SemiColon expressionsequence? RightParen statement

def p_continueStatement(p):
    '''continueStatement : continue Identifier SemiColon
                         | continue SemiColon'''

def p_breakStatement(p):
    '''breakStatement : break Identifier SemiColon
                      | break SemiColon'''

def p_returnStatement(p):
    '''returnStatement : return expressionSequence SemiColon
                       | return SemiColon'''

def p_withstatement(p):
    '''withStatement : with LeftParen expressionSequence RightParen statement'''

def p_switchStatement(p):
    '''switchStatement : switch LeftParen expressionSequence RightParen caseBlock'''

def p_caseBlock(p):
    ''' caseBlock : LeftBrace caseClauses defaultClause caseClauses RightBrace
                  | LeftBrace caseClauses defaultClause RightBrace
                  | LeftBrace caseClauses RightBrace
                  | LeftBrace defaultClause caseClauses RightBrace
                  | LeftBrace defaultClause RightBrace
                  | LeftBrace RightBrace'''

def p_caseClauses(p):
    ''' caseClauses : caseClause caseClauses 
                    | caseClause'''

def p_caseClause(p):
    ''' caseClause : case expressionSequence Colon statements 
                   | case expressionSequence Colon'''

def p_defaultClause(p): # default is be added to keywords in lex.py
    '''defaultClause : default Colon statements
                     | default Colon'''

##############################################################
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
