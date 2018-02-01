SHELL := /bin/bash
default:
	mkdir bin
	touch bin/lexer
	chmod +x bin/lexer
	echo "#! /usr/bin/env python" >> bin/lexer
	echo "import sys" >> bin/lexer
	echo "import os" >> bin/lexer
	echo "js_file_name = sys.argv[1]" >> bin/lexer
	echo 'command = "python ./src/run_me.py %s" %(js_file_name)' >> bin/lexer
	echo "os.system(command)" >> bin/lexer
clean:
	rm -r bin
