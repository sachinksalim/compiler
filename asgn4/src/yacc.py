import ply.yacc as yacc
from lex import tokens
import sys
from ast import literal_eval

temp_count = 0
temp_base = 'tmp'

ST = {}
ST['addressDescriptor'] = {}
ST['main'] = {}
ST['main']['__name__'] = 'main'
ST['main']['__level__'] = 0
ST['main']['__variables__'] = [] 
ST['main']['__functions__'] = []

ST['scopes'] = [ST['main']]


def str_to_type(s):
    try:
        k=literal_eval(s)
        return type(k)
    except:
        return type(s)

def newTemp():
    global temp_count, temp_base
    new_place = temp_base+str(temp_count)
    temp_count += 1
    ST['addressDescriptor'][new_place] = {'scope': ST['scopes'][len(ST['scopes'])-1], 'variable': ''}   
    return new_place

## note that - string_rs => string*
##             string_rp => string+
##             string_rq => string?

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


def p_program(p):
    ''' start : statements'''

def p_empty(p):
    ''' empty :'''
    pass

def p_statements(p):   # it is used as statement*
    ''' statements : statement statements 
                   | empty'''

def p_statement(p):
    ''' statement : block 
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
                  | functionDeclaration'''

def p_block(p):
    ''' block : LeftBrace statements RightBrace'''

def p_variableStatement(p):
    ''' variableStatement : var variableDeclarationList SemiColon
                          | variableDeclarationList SemiColon'''

def p_variableDeclarationList(p):
    ''' variableDeclarationList : variableDeclaration Comma variableDeclarationList 
                                | variableDeclaration'''

def p_variableDeclaration(p):
    ''' variableDeclaration : Identifier_tmp 
                            | Identifier_tmp Assign singleExpression
        Identifier_tmp : Identifier
                       | arrayLiteral
                       | objectLiteral'''

def p_expressionStatement(p):
    ''' expressionStatement : expressionSequence SemiColon'''

def p_ifStatement(p):
    ''' ifStatement : if LeftParen expressionSequence RightParen statement
                    | if LeftParen expressionSequence RightParen statement else statement'''

def p_iterationStatement(p):
    ''' iterationStatement  : do statement while LeftParen expressionSequence RightParen SemiColon
                            | while LeftParen expressionSequence RightParen statement
                            | for LeftParen expressionSequence_rq SemiColon expressionSequence_rq SemiColon expressionSequence_rq RightParen statement
                            | for LeftParen var variableDeclarationList SemiColon expressionSequence_rq SemiColon expressionSequence_rq RightParen statement
                            | for LeftParen singleExpression in expressionSequence RightParen statement
                            | for LeftParen var variableDeclaration in expressionSequence RightParen statement
                            
        expressionSequence_rq : expressionSequence
                               | empty'''

def p_continueStatement(p):
    ''' continueStatement : continue Identifier SemiColon
                          | continue SemiColon'''

def p_breakStatement(p):
    ''' breakStatement : break Identifier SemiColon
                       | break SemiColon'''

def p_returnStatement(p):
    ''' returnStatement : return expressionSequence SemiColon
                        | return SemiColon'''

def p_withstatement(p):
    ''' withStatement : with LeftParen expressionSequence RightParen statement'''

def p_switchStatement(p):
    ''' switchStatement : switch LeftParen expressionSequence RightParen caseBlock'''

def p_caseBlock(p):
    ''' caseBlock       : LeftBrace caseClauses_rq defaultClause_caseClauses_rq RightBrace
        caseClauses_rq : caseClauses
                        | empty
        defaultClause_caseClauses_rq : defaultClause caseClauses_rq
                        | empty'''
                

def p_caseClauses(p):
    ''' caseClauses : caseClause caseClauses 
                    | caseClause'''

def p_caseClause(p):
    ''' caseClause : case expressionSequence Colon statements'''

def p_defaultClause(p):
    ''' defaultClause : default Colon statements'''

def p_functionDeclaration(p):
    ''' functionDeclaration : function Identifier LeftParen formalParameterList_rq RightParen LeftBrace statements RightBrace
        formalParameterList_rq : formalParameterList
                               | empty'''

def p_formalParameterList(p):
    ''' formalParameterList : varDC Comma formalParameterList
                            | varDC
        varDC : Identifier
              | Identifier Assign Number
              | Identifier Assign String'''

def p_arrayLiteral(p):
    ''' arrayLiteral : LeftBracket comma_rs elementList_rq comma_rs RightBracket
        elementList_rq : elementList
                        | empty
        comma_rs : Comma comma_rs 
                | empty'''    

# some doubts in ','+ in grammar of assignment 0 for elementList and arguments
def p_elementList(p):
    ''' elementList : singleExpression comma_rp_singleExpression_rs
        comma_rp_singleExpression_rs : comma_rp singleExpression comma_rp_singleExpression_rs
                                    | empty
        comma_rp : Comma comma_rp
                 | Comma '''

def p_arguments(p):
    ''' arguments : LeftParen expressionSequence RightParen
                  | LeftParen RightParen'''

def p_expressionSequence(p):    
    ''' expressionSequence : singleExpression Comma expressionSequence 
                           | singleExpression'''

def p_singleExpression(p):
        ''' arguments_rq : arguments
                      | empty
        unaryExpression : Incr singleExpression
                        | Decr singleExpression
                        | Plus singleExpression
                        | Minus singleExpression
                        | BinNot singleExpression
                        | Not singleExpression
        arithmeticExpression : singleExpression Plus singleExpression
                             | singleExpression Minus singleExpression
                             | singleExpression Times singleExpression
                             | singleExpression Divide singleExpression
                             | singleExpression Mod singleExpression
        shiftExpression : singleExpression Lshift singleExpression
                        | singleExpression Rshift singleExpression
                        | singleExpression Urshift singleExpression
        logicalExpression : singleExpression LT singleExpression
                          | singleExpression GT singleExpression
                          | singleExpression LTE singleExpression
                          | singleExpression GTE singleExpression
        logicalExpression : singleExpression Equal singleExpression
                          | singleExpression NotEqual singleExpression
                          | singleExpression StrEqual singleExpression
                          | singleExpression StrNotEqual singleExpression
        binaryExpression : singleExpression BinAnd singleExpression
                         | singleExpression BinXor singleExpression
                         | singleExpression BinOr singleExpression
                         | singleExpression And singleExpression
                         | singleExpression Or singleExpression
        
        singleExpression : LeftParen expressionSequence RightParen
                         | singleExpression LeftBracket expressionSequence RightBracket
                         | singleExpression Dot Identifier
                         | singleExpression arguments
                         | new singleExpression arguments_rq
                         | singleExpression Incr
                         | singleExpression Decr
                         | delete singleExpression
                         | void singleExpression
                         | unaryExpression
                         | arithmeticExpression
                         | shiftExpression
                         | logicalExpression
                         | singleExpression in singleExpression
                         | binaryExpression
                         | singleExpression CondOp singleExpression Colon singleExpression
                         | singleExpression Assign singleExpression
                         | reassignmentExpression
                         | this
                         | undefined
                         | arrayLiteral
                         | objectLiteral'''

def p_expression_literal(p):
    ''' singleExpression : Identifier'''
    # print('\n\n\n\nHaay\n\n\n\n')
    # p[0] = {}
    # p[0]['type'] = p[1]['type']
    # p[0]['place'] = newTemp()
    # print("**, " + p[0]['place'] + ", " + str(p[1]['val']))

def p_expression_literal(p):
    ''' singleExpression : literal'''
    p[0] = {}
    p[0]['type'] = p[1]['type']
    p[0]['val'] = p[1]['val']
    # p[0]['place'] = newTemp()
    # print("**, " + p[0]['place'] + ", " + str(p[1]['val']))
        

def p_reassignmentExpression(p):
    ''' reassignmentExpression : Identifier MulEq singleExpression
                           | Identifier DivEq singleExpression
                           | Identifier ModEq singleExpression
                           | Identifier PlusEq singleExpression
                           | Identifier MinusEq singleExpression
                           | Identifier LshiftEq singleExpression
                           | Identifier RshiftEq singleExpression
                           | Identifier UrshiftEq singleExpression
                           | Identifier AndEq singleExpression
                           | Identifier XorEq singleExpression
                           | Identifier OrEq singleExpression'''
    
    # p[0] = dict()
    print(p[2][:-1] + ", " + p[1] + ", " + str(p[3]['val']))

    # for elem in p:
    #     print(elem)


def p_literal(p):
    '''literal : NullLiteral
               | BooleanLiteral
               | StringLiteral
               | DecimalLiteral'''
    p[0] = {}
    typ = str_to_type(p[1])
    if typ == int:
        p[0]['type'] = 'int'
        p[0]['val'] = int(p[1])
    elif typ == str:
        p[0]['type'] = 'str'
        p[0]['val'] = p[1]
    elif typ == bool:
        p[0]['type'] = 'bool'
        p[0]['val'] = bool(p[1])
               
def p_objectLiteral(p):
    ''' objectLiteral : LeftBrace propertyAssignment comma_propertyAssignment_rs comma_rq RightBrace
                      | LeftBrace comma_rq RightBrace
        comma_propertyAssignment_rs : Comma propertyAssignment comma_propertyAssignment_rs
                                   | empty
        comma_rq : Comma
                  | empty'''

def p_propertyAssignment(p):
    '''propertyAssignment : singleExpression Colon singleExpression
                          | singleExpression Equal singleExpression
                          | LeftBracket singleExpression RightBracket Colon singleExpression
                          | Identifier'''

# def p_propertyName(p):
#     '''propertyName : identifierName
#                     | StringLiteral
#                     | DecimalLiteral'''

# def p_identifierName(p): # Identifier already defined in lex.py#
#     ''' identifierName : Identifier
#                        | reservedWord'''

# def p_reservedWord(p):
#     '''reservedWord : NullLiteral
#                     | BooleanLiteral'''
#                     #| keywords'''  # how to include keywords of lex.py

def p_StringLiteral(p): # String defined in lex.py
    ''' StringLiteral : String'''

def p_BooleanLiteral(p):
    ''' BooleanLiteral : true
                       | false'''

def p_NullLiteral(p):
    ''' NullLiteral : null'''

def p_DecimalLiteral(p): # Number defined in lex.py
    ''' DecimalLiteral : Number'''
    p[0] = p[1]

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
    # parser = yacc.yacc(debug=True, optimize=False)
    # result = parser.parse(data, debug=2)
    parser = yacc.yacc(debug=True, optimize=False)
    result = parser.parse(data)
