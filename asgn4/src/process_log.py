#!/usr/bin/python

import re

keywords = ('break','case','console','continue','delete', 'default', 'do', 'else','eval', 'false', 'for','function','if','in','log','new', 'null', 'return','switch', 'this', 'true', 'typeof','undefined','var','void','while','with')

operators = ('Plus', 'Minus', 'Times', 'Expo', 'Divide', 'Mod', 'BinAnd', 'BinOr', 'BinXor', 'BinNot', 'CondOp', 'Not', 'Assign', 'Equal', 'NotEqual', 'StrEqual', 'StrNotEqual', 'LT', 'GT', 'LTE', 'GTE', 'Or', 'And', 'Incr', 'Decr', 'Lshift', 'Rshift', 'Urshift', 'PlusEq', 'MinusEq', 'IntoEq', 'DivEq', 'LshiftEq', 'RshiftEq', 'UrshiftEq', 'AndEq', 'ModEq', 'XorEq', 'OrEq')

tokens = ('Dot', 'Comma', 'SemiColon', 'Colon', 'LeftParen', 'RightParen', 'LeftBrace', 'RightBrace', 'LeftBracket', 'RightBracket', 'Identifier', 'Number', 'String') + keywords + operators

def setcolors(print_out):
    tmp = []
    for out in print_out:
        if out == 'Identifier':
            out = '<font color="#A6E22E">' + out + '</font>'
        elif out in keywords:
            out = '<font color="#F92672">' + out + '</font>'
        elif out in operators:
            out = '<font color="#F92672">' + out + '</font>'
        elif out == 'String':
            out = '<font color="#FD971F">' + out + '</font>'
        elif out == 'Number':
            out = '<font color="#AE81FF">' + out + '</font>'
        tmp.append(out)
    return tmp

def process_derivation():
    for i in range(len(deriv_list)):
        deriv_list[i] = deriv_list[i].split(' ')


    output = []
    output.append(deriv_list[0][0])
    write_html.write('<html>\n<head><title>Rightmost derivation</title><basefont size="7px"></head>\n')
    write_html.write("<body text='white' style='background-color:#272822;'>\n")
    write_html.write('<p>Note: Non-terminal being expanded is shown in <b>BOLD</b>. \n')
    write_html.write('Derived expansion is shown in <u>UNDERLINE</u>.</p>')
    new_deriv = (0, 0)
    for deriv in deriv_list:
        for i in range(len(output) - 1, -1, -1):
            if output[i] == deriv[0]:
                break
        print_out = output[:]
        output = output[:i] + deriv[2:] + output[i+1:]
        print_out[i] = "<b><font size = '5px'>" + print_out[i] + '</font></b>'
        print_out = setcolors(print_out)
        print_out[new_deriv[0]] = '<u>' + print_out[new_deriv[0]]
        print_out[new_deriv[1]] = print_out[new_deriv[1]] + '</u>'
        write_html.write('<p>')
        write_html.write(" ".join(print_out))
        write_html.write('</p>\n')
        new_deriv = (i, i + len(deriv[2:]) - 1)

    print_out = output[:]
    # print_out[new_deriv[0]] = '<u>' + print_out[new_deriv[0]]
    # print_out[new_deriv[1]] = print_out[new_deriv[1]] + '</u>'
    print_out = setcolors(print_out)
    write_html.write('<p>')
    write_html.write(" ".join(print_out))
    write_html.write('</p>\n')
    write_html.write('\n</body>\n</html>')


if __name__ == '__main__':
    read_log = open("./bin/debug.log")
    write_error = open("./bin/error.log", 'w')
    write_html = open("./right-derivation.html", 'w')
    text = read_log.read()

    TEXT = text.split('\n')

    error = []
    for lineno, line in enumerate(TEXT):
        if line == "Traceback (most recent call last):":
            error = TEXT[lineno:]
    error = "\n".join(error)
    write_error.write(error)

    pattern = r"Action : Reduce rule \[(.*?)\]"
    deriv_list = re.findall(pattern, text)
    deriv_list.reverse()

    process_derivation()

    read_log.close()
    write_error.close()
    write_html.close()