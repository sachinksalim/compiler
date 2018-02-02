#!/usr/bin/python

def main():
    fp = open("test.txt")
    tac = fp.read() # three-address code

    tac = tac.split('\n')
    for i in range(len(tac)):
        tac[i] = tac[i].split(", ")
    print(tac)
    fp.close()

if __name__ == '__main__':
	main()
