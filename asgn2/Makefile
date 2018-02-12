SHELL := /bin/bash
default:
	mkdir bin
	touch bin/codegen
	chmod +x bin/codegen
	echo "#! /usr/bin/env python" >> bin/codegen
	echo "import sys" >> bin/codegen
	echo "import os" >> bin/codegen
	echo "test_file = sys.argv[1]" >> bin/codegen
	echo 'command = "python ./src/run_me.py %s" %(test_file)' >> bin/codegen
	echo "os.system(command)" >> bin/codegen
clean:
	rm -r bin
