import ply.yacc as yacc
from lex import tokens
import sys

## note that - string_rs => string*
##             string_rp => string+
##             string_rq => string?


def p_program(p):
    'start : statements'

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
                  | printStatement'''
                  # functionDeclaration is needed to look because it contains many deleted rules

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

## def p_functionDeclaration(p): remaining

## def p_functionBody(p): remaining

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

# doubt in singleExpression first production involving function
def p_singleExpression(p):
    ''' arguments_rq : arguments
                      | empty
        unaryOp : Incr
                | Decr
                | Plus
                | Minus
                | BinNot
                | Not
        binaryOpAirth : Plus
                      | Minus
                      | Times
                      | Divide
                      | Mod
        shiftOp : Lshift
                | Rshift
                | Urshift
        logicalOpComp : LT
                       | GT
                       | LTE
                       | GTE
        logicalOpEqual : Equal
                        | NotEqual
                        | StrEqual
                        | StrNotEqual
        binaryOpBit : BinAnd
                    | BinXor
                    | BinOr
                    | And
                    | Or

        singleExpression : singleExpression LeftBracket expressionSequence RightBracket
                         | singleExpression Dot identifierName
                         | singleExpression arguments
                         
                         | new singleExpression arguments_rq
                         | singleExpression Incr
                         | singleExpression Decr
                         | delete singleExpression
                         | void singleExpression
                         
                         | unaryOp singleExpression
                         | singleExpression binaryOpAirth singleExpression
                         | singleExpression shiftOp singleExpression
                         | singleExpression logicalOpComp singleExpression
                         | singleExpression in singleExpression
                         | singleExpression logicalOpEqual singleExpression
                         | singleExpression binaryOpBit singleExpression
                         | singleExpression CondOp singleExpression Colon singleExpression
                         | singleExpression Assign singleExpression
                         | singleExpression assignmentOperator singleExpression
                         | this
                         | undefined
                         | Identifier
                         | literal
                         | arrayLiteral
                         | objectLiteral
                         | LeftParen expressionSequence RightParen'''
                         #| eval LeftParen program  RightParen
                         #| Typeof singleExpression
                         #| function Identifier? LeftParen formalparameterlist? RightParen LeftBrace functionbody RightBrace

def p_assignmentOperator(p):
    ''' assignmentOperator : IntoEq
                           | DivEq
                           | ModEq
                           | PlusEq
                           | MinusEq
                           | LshiftEq
                           | RshiftEq
                           | UrshiftEq
                           | AndEq
                           | XorEq
                           | OrEq'''

def p_literal(p):
    '''literal : NullLiteral
               | BooleanLiteral
               | StringLiteral
               | DecimalLiteral'''
               #| TemplateStringLiteral
               
def p_objectLiteral(p):
    ''' objectLiteral : LeftBrace propertyAssignment comma_propertyAssignment_rs comma_rq RightBrace
                      | LeftBrace comma_rq RightBrace
        comma_propertyAssignment_rs : Comma propertyAssignment comma_propertyAssignment_rs
                                   | empty
        comma_rq : Comma
                  | empty'''

def p_propertyAssignment(p):
    '''propertyAssignment : propertyName Colon singleExpression
                          | propertyName Equal singleExpression
                          | LeftBracket singleExpression RightBracket Colon singleExpression
                          | Identifier'''

def p_propertyName(p):
    '''propertyName : identifierName
                    | StringLiteral
                    | DecimalLiteral'''

def p_identifierName(p): # Identifier already defined in lex.py#
    ''' identifierName : Identifier
                       | reservedWord'''

def p_reservedWord(p):
    '''reservedWord : NullLiteral
                    | BooleanLiteral'''
                    #| keywords'''  # how to include keywords of lex.py

def p_StringLiteral(p): # String defined in lex.py
    ''' StringLiteral : String'''

## def p_TemplateStringLiteral(p): remaining    

def p_BooleanLiteral(p):
    ''' BooleanLiteral : true
                       | false'''

def p_NullLiteral(p):
    ''' NullLiteral : null'''

def p_DecimalLiteral(p): # Number defined in lex.py
    ''' DecimalLiteral : Number'''

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
