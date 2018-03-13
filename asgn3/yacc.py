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

# start or program
def p_program(p):
    '''start : statements'''

def p_statements(p):
    '''statements : statement statements
                  | statement'''
def p_statement(p):
    '''statement : block
                 | SemiColon
                 | variablestatement
                 | expressionstatement
                 | ifstatement
                 | iterationstatement
                 | continuestatement
                 | breakstatement
                 | returnstatement
                 | withstatement
                 | switchstatement
                 | funcitondeclaration'''

def p_block(p):
    'block: LeftBrace statements RightBrace'

def p_variablestatement(p):
    'variablestatement : var variabledeclarationlist SemiColon'

def p_variabledeclarationlist(p):
    '''variabledeclarationlist : variabledeclaration
                               | variabledeclaration Comma variabledeclarationlist'''
def p_variabledeclaration(p):
    '''variabledeclaration : Identifier 
                           | Identifier Equal singleexpression
                           | arrayliteral
                           | arrayliteral Equal singleexpression
                           | objectliteral
                           | objectliteral Equal singleexpression'''

def p_expressionstatement(p):
    'expressionstatement : expressionsequence SemiColon'

def p_ifstatement(p):
    ''' ifstatement : if LeftParen expressionsequence RightParen statement
                    | if LeftParen expressionsequence RightParen statement else statement'''

def p_iterationstatement(p):
    ''' expressionsequence? : expressionsequence 
                            | 
        iterationstatement  : do statement while LeftParen expressionsequence RightParen SemiColon
                            | while LeftParen expressionsequence RightParen statement
                            | for LeftParen expressionsequence? SemiColon expressionsequence? SemiColon expressionsequence? RightParen statement
                            | for LeftParen var variabledeclarationlist SemiColon expressionsequence? SemiColon expressionsequence? RightParen statement
                            | for LeftParen singleexpression in expressionsequence RightParen statement
                            | for LeftParen var variabledeclaration in expressionsequence RightParen statement'''

def p_continuestatement(p):
    '''continuestatement : continue Identifier SemiColon
                         | continue SemiCOlon'''

def p_breakstatement(p):
    '''breakstatement : break Identifier SemiColon
                      | break SemiColon'''
def p_returnstatement(p):
    '''returnstatement : return SemiColon
                       | return expressionsequence SemiColon'''
def p_withstatement(p):
    '''withstatement : with LeftParen expressionsequence RightParen statement'''
def p_switchstatement(p):
    '''switchstatement : switch LeftParen expressionsequence RightParen caseblock'''
def p_caseblock(p):
    ''' caseclauses? : caseclauses 
                     |
        defaultclause_caseclauses?? : defaultclause caseclauses?
                                   | 
        caseblock : LeftBrace caseclauses? defaultclause_caseclauses?? RightBrace'''
def p_caseclauses(p):
    ''' caseclauses: caseclause caseclauses | caseclause'''
def p_caseclause(p):
    ''' caseclause : case expressionsequence Colon statement* 
        statement* : statement statement* 
                   | '''

#############################
def p_defaultclause(p): # default must be added to keywords
    '''defaultclause : default Colon statement*
       statement* : statement statement* 
                   | '''
################################
# formalparameterlist is in deleted ones, so we should mostly remove it from below

def p_functiondeclaration(p):
    '''functiondeclaration : function Identifier LeftParen formalparameterlist? RightParen LeftBrace functionbody RightBrace
       formalparameterlist? : formalparameterlist 
                            | '''
################################

def p_functionbody(p):
    '''functionbody : sourceelements
                    | '''
def p_arrayliteral(p):
    '''arrayliteral : LeftBracket comma* elementlist? comma* RightBracket
       elementlist? : elementlist
                    |   
       comma* : Comma comma* 
              | '''

def p_elementlist(p):
    '''elementlist : singleexpression comma_singleexpression*
       comma_singleexpression* : Comma singleexpression comma_singleexpression*
                               | '''
def p_arguments(p):
    ''' comma_singleexpression* : Comma singleexpression comma_singleexpression*
                               | 
        arguments : LeftParen singleexpression comma_singleexpression* Rightparen
                  | LeftParen Rightparen '''
def p_expressionsequence(p):
    '''comma_singleexpression* : Comma singleexpression comma_singleexpression*
                               | 
       expressionsequence : singleexpression comma_singleexpression*'''
def p_singleexpression(p):
    ##############
    ######### doubt in singleexpression first production involving function 
    ##############
    ''' Identifer? : Identifer 
                   | 
        arguments? : arguments
                   | 
        formalparameterlist? : formalparameterlist 
                            | 
        incr_decr_plus : Incr
                       | Decr
                       | Plus
                       | Minus
                       | BinNot
                       | Not
        p_m_t_d_m : Plus
                  | Minus
                  | Times
                  | Divide
                  | Mod
        shift_l_r_ur : Lshift
                     | Rshift
                     | Urshift
        grt_less : LT
                 | GT
                 | LTE
                 | GTE
        diffequals : Equal
                   | NotEqual
                   | StrEqual
                   | StrNotEqual
        binoperators : BinAnd
                     | BinXor
                     | BinOr
                     | And
                     | Or
        assignmentoperator : IntoEq
                           | DivEq
                           | ModEq
                           | PlusEq
                           | MinusEq
                           | LshiftEq
                           | RshiftEq
                           | UrshiftEq
                           | AndEq
                           | XorEq
                           | OrEq
        singleexpression : function Identifier? LeftParen formalparameterlist? RightParen LeftBrace functionbody RightBrace
                         | singleexpression LeftBracket expressionsequence RightBracket
                         | singleexpression Dot identifiername
                         | singleexpression arguments
                         | eval LeftParen program  RightParen
                         | new singleexpression arguments?
                         | singleexpression Incr
                         | singleexpression Decr
                         | delete singleexpression
                         | void singleexpression
                         | Typeof singleexpression
                         | incr_decr_plus singleexpression
                         | singleexpression p_m_t_d_m singleexpression
                         | singleexpression shift_l_r_ur singleexpression
                         | singleexpression grt_less singleexpression
                         | singleexpression in singleexpression
                         | singleexpression diffequals singleexpression
                         | singleexpression binoperators singleexpression
                         | singleexpression CondOp singleexpression Colon singleexpression
                         | singleexpression Assign singleexpression
                         | singleexpression assignmentoperator singleexpression
                         | this
                         | undefined
                         | Identifier
                         | literal
                         | arrayliteral
                         | objectliteral
                         | LeftParen expressionsequence RightParen '''
def p_literal(p):
    '''literal : nullliteral
               | booleanliteral
               | stringliteral
               | templatestringliteral
               | decimalliteral'''
def object_literal(p):
    ''' comma? : Comma
               | 
        comma_propertyassignment* : Comma propertyassignment comma_propertyassignment*
                                  | 


        objectliteral : LeftBrace propertyassignment comma_propertyassignment* comma? RightBrace
                      | LeftBrace comma? RightBrace'''
def p_propertyassignment(p):
    '''propertyassignment : propertyname Colon singleexpression
                          | propertyname Equal singleexpression
                          | LeftBracket singleexpression RightBracket Colon singleexpression
                          | Identifier'''
def p_propertyname(p):
    '''propertyname : identifiername
                    | stringliteral
                    | decimalliteral'''
def p_identifiername(p):
    ''' identifiername : Identifier
                       | reservedword'''
def p_reservedword(p):
    '''reservedword : keyword
                    | nullliteral
                    | booleanliteral'''
#######      
### identifier already deined in lex.py###
#######

def p_stringliteral(p):
    'stringliteral : string'
##############
### someone complete templatestringliteral ###
##############
def p_booleanliteral(p):
    '''booleanliteral : true
                      | false'''
def p_nullliteral(p):
    '''nullliteral : null'''
def p_decimalliteral(p):
    ''' decimalliteral : number'''

#######  Assignment ################# 

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
