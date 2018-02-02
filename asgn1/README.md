# Compiler Assignment 1
## Lexer for Javascript using PLY

A lexer for Javascript using the parsing tool PLY (Python Lex-Yacc). It outputs a summary of the tokens in the program.


### How to run

Inside the "asgn1" directory, there are two folders named "src" and "test". 

The sample test files ( javascript files ) are inside the "test" directory.  
( test1.js  test2.js  test3.js  test4.js  test5.js)

Whereas "src" contains the source code for the lexer implemented in python. The "src" again contains two .py files namely "lex.py" and "run_me.py". The "lex.py" file basically contains the code for the regular expressions and matching the patterns. The "run_me.py" is linked to "lex.py". The output which we are supposed to generate is handled by the "run_me.py" file.

The "asgn1" folder also contains a Makefile. 
By running the shell command "make" , a folder "bin" is created and inside it an executable named "lexer" along with it.

So to finally run the test cases, you need to type for example " bin/lexer test/test1.js " to run the sample test case-1.

Also the bin folder which was created by "make" can be cleaned using the command "make clean".

```
cd asgn1
make
bin/lexer test/test1.js
```

## Authors

* **Sachin K Salim (14575)** - *CSE, IIT Kanpur*
* **Sughosh P (14441)** - *CSE, IIT Kanpur*
* **Shivam Yadav (14655)** - *CSE, IIT Kanpur*
