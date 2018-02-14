The folder asgn2 contains two folders 'src' and 'test' and two files 'Makefile' and 'README; (which you are going through right now :p)'

The folder 'src' further contains these files:
1)run_me.py   2)tables.py 

*run_me.py imports tables.py.
 Tables.py contains the ('get_reg', 'movex86', 'free_reg') functions.

The folder 'test' contains 5 testfiles namely:
( test1.ir, test2.ir, test3.ir, test4.ir, test5.ir )

**The makefile can be used to do the following:
	1) make
	2) make clean
  
  The command 'make' creates the folder 'bin' inside 'asgn2' and inside it an executable named  'codegen'
  The command 'make clean' just removes the created 'bin' and its contents

  **Now to convert the 3 Address code into assembly code, let's say for the testcase 'test1.ir', we need to do the following:
  1) cd asgn2
  2) make
  3) bin/codegen test/test1.ir

  This prints the required assembly code to the terminal output
  To run the assembly code generated, do the following:
  1) cd asgn2
  2) make
  3) bin/codegen test/test1.ir > codegen.s
  4) as --32 codegen.s -o codegen.o
  5) ld -m elf_i386 codegen.o -o key -lc -dynamic-linker /lib/ld-linux.so.2
  6) ./key
