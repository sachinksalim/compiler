import ply.lex as lex

keywords = ('break','case','console','continue','delete','do', 'else','eval','for','function','if','in','log','new','return','switch', 'this','typeof','undefined','var','void','while','with')

tokens = ('Dot', 'Comma', 'SemiColon', 'Colon', 'Plus', 'Minus', 'Times', 'Expo', 'Divide', 'Mod', 'BinAnd', 'BinOr', 'BinXor', 'BinNot', 'CondOp', 'Not', 'LeftParen', 'RightParen', 'LeftBrace', 'RightBrace', 'LeftBracket', 'RightBracket', 'Assign', 'Equal', 'NotEqual', 'StrEqual', 'StrNotEqual', 'LT', 'GT', 'LTE', 'GTE', 'Or', 'And', 'Incr', 'Decr', 'Lshift', 'Rshift', 'Urshift', 'PlusEq', 'MinusEq', 'IntoEq', 'DivEq', 'LshiftEq', 'RshiftEq', 'UrshiftEq', 'AndEq', 'ModEq', 'XorEq', 'OrEq',

    'Identifier', 'Number', 'String') + keywords

# define operators
t_Dot           = r'\.'
t_Comma         = r','
t_SemiColon     = r';'
t_Colon         = r':'
t_Plus          = r'\+'             
t_Minus         = r'-'              
t_Times         = r'\*'             
t_Expo          = r'\*\*'
t_Divide        = r'/'              
t_Mod           = r'%'              
t_BinAnd        = r'&'              
t_BinOr         = r'\|'             
t_BinXor        = r'\^'             
t_BinNot        = r'~'              
t_CondOp        = r'\?'
t_Not           = r'!'              
t_LeftParen     = r'\('             
t_RightParen    = r'\)'             
t_LeftBrace     = r'{'              
t_RightBrace    = r'}'              
t_LeftBracket   = r'\['
t_RightBracket  = r'\]'
t_Assign        = r'='
t_Equal         = r'=='
t_NotEqual      = r'!='
t_StrEqual      = r'==='
t_StrNotEqual   = r'!=='
t_LT            = r'<'              
t_GT            = r'>'              
t_LTE           = r'<='
t_GTE           = r'>='
t_Or            = r'\|\|'           
t_And           = r'&&'             
t_Incr          = r'\+\+'           
t_Decr          = r'--'             
t_Lshift        = r'<<'             
t_Rshift        = r'>>'             
t_Urshift       = r'>>>'            
t_PlusEq        = r'\+='
t_MinusEq       = r'-='
t_IntoEq        = r'\*='
t_DivEq         = r'/='
t_LshiftEq      = r'<<='
t_RshiftEq      = r'>>='
t_UrshiftEq     = r'>>>='
t_AndEq         = r'&='
t_ModEq         = r'%='
t_XorEq         = r'\^='
t_OrEq          = r'\|='

def t_Identifier(t):                         
    r'[a-zA-Z_][a-zA-Z_0-9]*'
    if t.value in keywords:
    	t.type = t.value
    return t

number = r"""
(?:
    (?:0|[1-9][0-9]*)\.[0-9]*  # floating point
    (?:[eE][+-]?[0-9]+)?       # optional exponent part
    |
    \.[0-9]+                   # floating point starting with dot
    (?:[eE][+-]?[0-9]+)?       # optional exponent part
    |
    (?:0|[1-9][0-9]*)          # integer
    (?:[eE][+-]?[0-9]+)?       # optional exponent part
)
"""
@lex.TOKEN(number)
def t_Number(t):
    #t.value = int(t.value)
    return t

# To track line numbers
def t_NewLine(t):
    r'\n+'
    t.lexer.lineno += len(t.value)

string = r"""
(?:
    # single quoted string
    (?:'                               # opening single quote
        (?: [^'\\\n\r]                 # no \, line terminators or '
            | \\[a-zA-Z!-\/:-@\[-`{-~] # or escaped characters
            | \\x[0-9a-fA-F]{2}        # or hex_escape_sequence
            | \\u[0-9a-fA-F]{4}        # or unicode_escape_sequence
        )*?                            # zero or many times
        (?: \\\n                       # multiline ?
          (?:
            [^'\\\n\r]                 # no \, line terminators or '
            | \\[a-zA-Z!-\/:-@\[-`{-~] # or escaped characters
            | \\x[0-9a-fA-F]{2}        # or hex_escape_sequence
            | \\u[0-9a-fA-F]{4}        # or unicode_escape_sequence
          )*?                          # zero or many times
        )*
    ')                                 # closing single quote
    |
    # double quoted string
    (?:"                               # opening double quote
        (?: [^"\\\n\r]                 # no \, line terminators or "
            | \\[a-zA-Z!-\/:-@\[-`{-~] # or escaped characters
            | \\x[0-9a-fA-F]{2}        # or hex_escape_sequence
            | \\u[0-9a-fA-F]{4}        # or unicode_escape_sequence
        )*?                            # zero or many times
        (?: \\\n                       # multiline ?
          (?:
            [^"\\\n\r]                 # no \, line terminators or "
            | \\[a-zA-Z!-\/:-@\[-`{-~] # or escaped characters
            | \\x[0-9a-fA-F]{2}        # or hex_escape_sequence
            | \\u[0-9a-fA-F]{4}        # or unicode_escape_sequence
          )*?                          # zero or many times
        )*
    ")                                 # closing double quote    
)
"""  # "

@lex.TOKEN(string)
def t_String(t):
    t.value = t.value.replace('\\\n', '')
    return t

# Ignored characters (spaces and tabs)
t_ignore  = ' \t'

# Ignore comments
t_ignore_LineComment = r'//[^\r\n]*'
t_ignore_BlockComment = r'\/\*[^*]*\*\/'

# Error handling
def t_error(t):
    print("Illegal character '%s'" % t.value[0])
    t.lexer.skip(1)

# Build the lexer
lexer = lex.lex()
