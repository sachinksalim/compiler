import ply.yacc as yacc
from lex import tokens
import sys

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
        arithmeticExpression : singleExpression Plus singleExpression
                      | singleExpression Minus singleExpression
                      | singleExpression Times singleExpression
                      | singleExpression Divide singleExpression
                      | singleExpression Mod singleExpression
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
                         | arithmeticExpression
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
