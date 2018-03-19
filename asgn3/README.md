Usage:
```
make
bin/parser test/test.js
firefox test.html
```
The directory asgn3 contains the folders "src" and "test", a Makefile and a Readme

The "src" folder further contains the files lex.py, yacc.py, process_log.py and parser
"lex.py" is the lexer and when given a string of characters produces valid tokens
"yacc.py" contains the grammar which ensures the correct syntax of the given code
The "test" folder contains 5 different test cases.

Command "make" when in the directory "/asgn3" creates the folder "bin" and creates the executable "parser" in it.

The executalbe "parser" has the following lines:
```#!/bin/bash
python3 ./src/yacc.py $1 2> bin/debug.log
python3 ./src/process_log.py
```

After the suitable files are created, to run a test case from the "test" folder, use the command "bin/parser test/test.js" to create a html file "test.html" in the "/asgn3" directory. 
Then using the command "firefox right-derivation.html" we can open this in the Mozilla browser.

"make clean" removes the /bin directory and its contents along with the html file.

