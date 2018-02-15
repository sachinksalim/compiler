The folder asgn2 contains two folders 'src' and 'test' and two files 'Makefile' and 'README'

The folder 'src' further contains:
```
1) run_me.py
2) tables.py
3) print_int.s
```
run_me.py imports tables.py.
 Tables.py contains the ('get_reg', 'movex86') functions.
 print_int.s contains the x86 code to print an integer.

The folder 'test' contains 5 testfiles namely:
( test1.ir, test2.ir, test3.ir, test4.ir, test5.ir )

The makefile can be used to do the following:
```
1) make
2) make clean
```
  
The command 'make' creates the folder 'bin' inside 'asgn2' and inside it an executable named 'codegen'.
The command 'make clean' removes the created 'bin' and its contents.

To convert the 3 Address code into assembly code, say for the testcase 'test1.ir', we need to do the following:
```
  cd asgn2
  make
  bin/codegen test/test1.ir
```
Above commands prints the required assembly code to the terminal output.

To execute the assembly code generated, do the following:
```
  cd asgn2
  make -f Execute
  bin/codegen test/test1.ir
```
