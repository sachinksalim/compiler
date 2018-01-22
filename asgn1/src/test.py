from lex import *

data = "2+6*85+1="

# Give the lexer some input
lexer.input(data)

tokenDict = {}

# Tokenize
print("{0:^16} {1:^16} {2:^8}".format("Token", "Occurrences", "Lexemes"))
print("{0:^16} {1:^16} {2:^8}".format("-----", "-----------", "-------"))
for tok in lexer:
    if tok.type in tokenDict:
        tokenDict[tok.type].append(tok.value)
    else:
        tokenDict.update({tok.type: [tok.value]})
    #print("{0:^16} {1:^16} {2:^8}".format(tok.type, tok.lexpos, tok.value))

#print(tokenDict)

for token, lexeme in tokenDict.items():
    print("{0:^16} {1:^16} {2:^8}".format(token, len(lexeme), lexeme[0]))
    for lex in lexeme[1:]:
        print("{0:^75}".format(lex))
