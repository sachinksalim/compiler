from collections import Counter
from lex import *

js_code = open("test.js")
data = js_code.read()
js_code.close()

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

for token, lexeme in tokenDict.items():
    lexeme.sort()
    if token in ['Identifier', 'Number']:
    	print("{0:^16} {1:^16}".format(token, len(lexeme)))
    	grouped = Counter(lexeme)
    	for key, count in grouped.items():
    		temp_key = str(key) + " (" + str(count) + ")"
    		print("{0:^76}".format(temp_key))
    		temp_key = ""
    else:
    	print("{0:^16} {1:^16} {2:^8}".format(token, len(lexeme), lexeme[0]))
