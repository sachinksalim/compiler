#!/usr/bin/python

import re

def process_derivation():
    for i in range(len(deriv_list)):
        deriv_list[i] = deriv_list[i].split(' ')
        print(deriv_list[i])

    output = []
    output.append(deriv_list[0][0])
    write_html.write('<p>Non-terminal being expanded is shown in <b>BOLD</b>. ')
    write_html.write('Derived expansion is shown in <u>UNDERLINE</u>.</p>')
    new_deriv = (0, 0)
    for deriv in deriv_list:
        for i in range(len(output) - 1, -1, -1):
            if output[i] == deriv[0]:
                break
        print_out = output[:]
        output = output[:i] + deriv[2:] + output[i+1:]
        print_out[i] = '<b>' + print_out[i] + '</b>'
        print_out[new_deriv[0]] = '<u>' + print_out[new_deriv[0]]
        print_out[new_deriv[1]] = print_out[new_deriv[1]] + '</u>'
        write_html.write('<p>')
        write_html.write(" ".join(print_out))
        write_html.write('</p>\n')
        new_deriv = (i, i + len(deriv[2:]) - 1)


if __name__ == '__main__':
    read_log = open("debug.log")
    write_html = open("test.html", 'w')
    text = read_log.read()    

    pattern = r"Action : Reduce rule \[(.*?)\]"
    deriv_list = re.findall(pattern, text)
    deriv_list.reverse()

    process_derivation()
    
    read_log.close()
    write_html.close()
