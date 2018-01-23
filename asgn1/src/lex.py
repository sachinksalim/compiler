import ply.lex as lex


keywords = ('break','case','console','continue','delete','do',
	   'else','eval','for','function','if','in','log','new','return','switch',
	   'this','typeof','undefined','var','void','while','with')


tokens = ('Plus','Minus','Times','Divide','Assign', 
	'OpenBracket', 'CloseBracket', 'OpenParen','CloseParen','OpenBrace','CloseBrace',
	'Identifier','Type','IntConst','SemiColon','ID')+keywords



t_Plus    = r'\+'
t_Minus   = r'-'
t_Times   = r'\*'
t_Divide  = r'/'
t_Assign = r'='
t_OpenBracket = r'\[' 
t_CloseBracket = r'\]'
t_OpenParen  = r'\('
t_CloseParen  = r'\)'
t_OpenBrace = r'\{'
t_CloseBrace = r'\}'
t_Identifier = r'[a-zA-Z_][a-zA-Z_0-9]*'
t_SemiColon = r';'

def t_ID(t):                         
    r'[a-zA-Z_][a-zA-Z_]*'
    if t.value in keywords :
	t.type = t.value
    return t


def t_IntConst(t):
    r'\d+'
    t.value = int(t.value)    
    return t

# To track line numbers
def t_NewLine(t):
    r'\n+'
    t.lexer.lineno += len(t.value)

# Ignored characters (spaces and tabs)
t_ignore  = ' \t'

# Error handling
def t_error(t):
    print("Illegal character '%s'" % t.value[0])
    t.lexer.skip(1)

# Build the lexer
lexer = lex.lex()
