#!/usr/bin/python

# some imports

#
# some definitions
# block_leaders stores the line numbers of the block leaders
temp_block_leaders = []
block_leaders = []
basic_blocks = []
#op = ['=',]

def main():
	fp = open("test.txt")
	tac = fp.read() # three-address code
	tac = tac.split('\n')
	num_lines_tac  = len(tac)
	for i in range(len(tac)):
		tac[i] = tac[i].split(", ")
	#print(tac)
###############################################################
#					Block leaders
################################################################
# for call=goto, ifgoto, label, ret#
## according to wikipedia, definition of a leader:
# 	1)The first instruction is a leader.
#	2)The target of a conditional or an unconditional goto/jump instruction is a leader.
#	3)The instruction that immediately follows a conditional goto/jump instruction is a leader.
	temp_block_leaders.append(1)	# since, the first line is always a leader
	temp = 1;
	for i in range(num_lines_tac):
#		if tac[i][1] == 'call':
#			print tac[i][0]
#			block_leaders.append(int(tac[i][0])+1)
		if tac[i][1] == 'ifgoto':
			#print tac[i][0]
			temp_block_leaders.append(int(tac[i][5])) # since target of a jump is also a leader
			temp_block_leaders.append(int(tac[i][0])+1) 
		elif tac[i][1] == 'label':
			#print tac[i][0]
			temp_block_leaders.append(int(tac[i][0]))	
		if tac[i][1] == 'ret':
			#print tac[i][0]
			temp_block_leaders.append(int(tac[i][0]))
	temp_block_leaders.sort()
	# lets remove duplicates
	for i in temp_block_leaders:
		if i not in block_leaders:
			block_leaders.append(i)
	print block_leaders
############################################################
# lets now build the basic blocks
### lets just put a special character '$' just before a block leader

	for i in range(num_lines_tac):
		basic_blocks.append(tac[i])
	#print basic_blocks
	temp=0
	for i in block_leaders:
		basic_blocks.insert( i+temp-1, "$")
		temp = temp+1
	print basic_blocks
# we have finished seperating the basic blocks by '$'
################################################################

	fp.close()

if __name__ == '__main__':
	main()

# block leaders are (1,5,7,8,10)
