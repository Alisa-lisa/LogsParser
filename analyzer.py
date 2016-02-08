# read the log file
# from llvmlite import binding
# from numba import jit
import os
import muliprocessing as mp

# @jit
def make_readable(file):
	inF = file
	outF = os.path.join(os.path.splitext(inF)[0], '.txt')
	with open(inF, 'rb') as i:
		with open(outF, 'wb') as j:
			j.write(i.read())