import ply.lex as lex
tokens = ['Plus','Minus','Times','Divide','Assign', 
	'OpenBracket', 'CloseBracket', 'OpenParen','CloseParen','OpenBrace','CloseBrace',
	'Identifier','Type','Return','IntConst','SemiColon']

t_Plus    = r'\+'
t_Minus   = r'-'
t_Times   = r'\*'
t_Divide  = r'/'
t_OpenParen  = r'\('
t_CloseParen  = r'\)'
t_Assign = r'='

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
