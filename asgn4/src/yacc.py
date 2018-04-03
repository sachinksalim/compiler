import ply.yacc as yacc
from lex import tokens
import sys
from ast import literal_eval

temp_count = 0
temp_base = 'tmp'
label_count = 0
label_base = 'label'

ST = {}
ST['addressDescriptor'] = {}
ST['main'] = {}
ST['main']['__name__'] = 'main'
ST['main']['__level__'] = 0
ST['main']['__variables__'] = [] 
ST['main']['__functions__'] = []

ST['scopes'] = [ST['main']]


# Helping functions
def createLabel():
  global label_count, label_base
  label = label_base + str(label_count)
  label_count = labels_count + 1
  return label
def str_to_type(s):
    try:
        k=literal_eval(s)
        return type(k)
    except:
        return type(s)

def eprint(*args, **kwargs): # Print Errors
    print(*args, file=sys.stderr, **kwargs)


### SYMBOL TABLE FUNCTIONS

def make_table(prevProc):
  if prevProc in SymT:
    eprint(prev + ' function already exists!')
    raise ValueError
  proc_table = dict()
  proc_table['__name__'] = prevProc # Needed?
  proc_table['__level__'] = None #TODO
  proc_table['__vars'] = [] # List of variables
  proc_table['__funcs'] = [] # List of functions

  SymT[prevProc] = proc_table
  return proc_table # Needed?

def add_entry(id_name, id_type, id_offset):
  var_entry = dict()
  var_entry['name'] = id_name
  var_entry['type'] = id_type
  var_entry['offset'] = id_offset

  SymT['addr_desc'][id_name] = var_entry


# def newTemp():
#     global temp_count, temp_base
#     new_place = temp_base+str(temp_count)
#     temp_count += 1
#     ST['addressDescriptor'][new_place] = {'scope': ST['scopes'][len(ST['scopes'])-1], 'variable': ''}   
#     return new_place

## note that - string_rs => string*
##             string_rp => string+
##             string_rq => string?

def addScope():
    #TODO
    pass

def removeScope():
    #TODO
    pass

def in_cur_scope(var):
    '''checks if var exists in current scope'''
    #TODO
    return False

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
    ''' start : block
                | statements'''

def p_statements(p):   # it is used as statement*
    ''' statements : statement statements 
                   | empty'''

def p_statement(p):
    ''' statement : SemiColon
                  | assignmentStatement SemiColon
                  | declarationStatement SemiColon
                  | expressionStatement
                  | ifStatement
                  | ifelseStatement
                  | whileStatement
                  | forStatement
                  | iterationStatement
                  | continueStatement
                  | breakStatement
                  | returnStatement
                  | withStatement
                  | switchStatement
                  | functionDeclaration'''

def p_block(p):
    ''' block : LeftBrace beginBlock statements RightBrace'''
    removeScope()

def p_beginBlock(p):
    ''' beginBlock : '''
    addScope()

def p_declarationStatement(p):
    ''' declarationStatement : var declarationList 
                          | declarationList '''

def p_declarationList(p):
    ''' declarationList : '''
    # TODO










def p_assignmentStatement(p):
    ''' assignmentStatement : var assignmentList 
                          | assignmentList '''
    var_list = p[2]
    for var in var_list:
        if in_cur_scope(var):
            eprint(var + ' already exists in current scope.')
            raise SyntaxError
        add_entry(id_name = var['name'], id_type = var['type'], id_offset = var['offset'])



def p_assignmentList(p):
    ''' assignmentList : variableAssignment Comma assignmentList 
                                | variableAssignment'''

def p_variableAssignment(p):
    ''' variableAssignment : IdentifierName Assign singleExpression '''
    Id = {}
    Id['name'] = p[1]
    Id['type'] = p[3]['type']
    # TODO : place
    p[0] = [Id]

def p_identifierName(p):
    ''' IdentifierName : Identifier
                       | arrayLiteral
                       | objectLiteral'''

def p_expressionStatement(p):
    ''' expressionStatement : expressionSequence SemiColon'''

############## IF BLOCK ###################
## havent implemented createlabels yet##
## also btw, couldnt do any changes for these semantic actions taken fromm the senior's repo
## i believe nothing could be done
def p_ifStatement(p):
    ''' ifStatement : if LeftParen expressionSequence RightParen block'''
    print("label, "+p[-2][1])

############## IF_ElSE BLOCK ###################
def p_ifelseStatement(p):
    ''' ifelseStatement : if LeftParen expressionSequence RightParen ifelseblock_marker statement else elseblock_marker block'''
    print("label, "+p[-5][2])     

def p_ifelseblock_marker(p):
  ''' ifelseblock_marker : empty'''
  label1 = createLabel()
  label2= createLabel()
  label3 = createLabel()
  p[0] = [label1,label2,label3]
  temp = newTemp
  print("=, "+temp+", 1")
  print("ifgoto, eq, "+p[-1]['place']+", "+temp+", "+label1)
  print("goto, "+label2)
  print("label, "+label3)

def p_elseblock_marker(p):
  ''' elseblock_marker : empty'''
  print("goto, "+p[-3][2])
  print("label, "+p[-3][1])

#####################################################################
"""
def p_iterationStatement(p):
    ''' iterationStatement  : do statement while LeftParen expressionSequence RightParen SemiColon
                            | for LeftParen expressionSequence_rq SemiColon expressionSequence_rq SemiColon expressionSequence_rq RightParen statement
                            | for LeftParen var assignmentList SemiColon expressionSequence_rq SemiColon expressionSequence_rq RightParen statement
                            
        expressionSequence_rq : expressionSequence
                               | empty'''


#     in iterationStatement
#                            | for LeftParen singleExpression in expressionSequence RightParen statement
#                            | for LeftParen var variableDeclaration in expressionSequence RightParen statement
"""
####################################################################
######## ForStatement#####################################
#########################################
def p_forStatement(p):
  ''' forStatement  : for LeftParen expressionSequence_rq SemiColon forexp_marker expressionSequence_rq forcheck_marker SemiColon expressionSequence_rq increment_marker RightParen block 
                    | for LeftParen var assignmentList SemiColon forexp_marker expressionSequence_rq forcheck_marker SemiColon expressionSequence_rq increment_marker RightParen block 
                            
      expressionSequence_rq : expressionSequence
                            | empty '''
  print("goto, "+p[-8][3])
  print("label, "+p[-8][2])

def p_forexp_marker(p):
  '''forexp_marker : empty '''
  label1 = createLabel()
  label2 = createLabel()
  label3 = createLabel()
  label4 = createLabel()
  p[0] = [label1, label2, label3, label4]
  print("label, "+label1)

def p_forcheck_marker(p):
  ''' forcheck_marker : empty '''
  tempvar = newTemp()
  print("=, "+tempvar+", 1")
  print("ifgoto, eq, "+p[-1]['place']+", "+tempvar+", "+p[-2][1])
  print("goto, "+p[-2][2])
  print("goto, "+p[-2][2])

def p_increment_marker(p):
  '''increment_marker : empty '''
  print("goto, "+p[-5][0])
  print("label, "+p[-5][1])

####################################


####################################################################
######## WhileStatement#####################################
#########################################

def p_whileStatement(p):
  '''whileStatement : while whileblockbegin_marker LeftParen expressionSequence RightParen exprcheck_marker block '''
  print("goto, "+p[-6][0])
  print("label, "+p[-6][1])

def p_expcheck_marker(p):
  ''' expcheck_marker : empty'''
  tempvar = newTemp()
  print("=, "+tempvar+", 1")
  print("ifgoto, neq, "+p[-2]['place']+", "+tempvar+", "+p[-4][1])

def p_whileblockbegin_marker(p):
  ''' startblock_marker : empty'''
  begin = createLabel()
  end = createLabel()
  p[0] = [begin, end]
  print("label, "+begin)

#############################################
#############################################


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

def p_expression_Identifier(p):
    ''' singleExpression : Identifier'''
    p[0] = {}
    p[0]['type'] = 'id'
    p[0]['val'] = p[1]

def p_expression_literal(p):
    ''' singleExpression : literal'''
    # print('LITERAL HOOOOY')
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
    
    fpw.write(p[2][:-1] + ", " + p[1] + ", " + str(p[3]['val']) + '\n')
    # TODO
    # Restrict arithmetic operator on bool and string


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
    elif typ == bool:
        p[0]['type'] = 'bool'
        p[0]['val'] = bool(p[1])
    else: #if typ == str:
        p[0]['type'] = 'str'
        p[0]['val'] = p[1]
               
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
        sys.exit()
    filename = sys.argv[1]
    data = read_data(filename)
    fpw = open('tac.ir','w')
    parser = yacc.yacc(debug=True, optimize=False)
    # result = parser.parse(data, debug=2)
    result = parser.parse(data)
