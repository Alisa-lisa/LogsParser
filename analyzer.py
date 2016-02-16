# read the log file
# from llvmlite import binding
# from numba import jit
import os, re
import numpy as np
import pandas as pd
# from multiprocessing import Process
# @jit
def make_readable(file):
	inF = file
	outF = os.path.splitext(inF)[0] + '.txt'
	with open(inF, 'rb') as i:
		with open(outF, 'wb') as j:
			j.write(i.read())
	os.remove(inF)
	return str(outF)

def convert_file(file):
	# open file for r\w
	f = open(file, 'r')

	df_dict = {'address':[], 'time':[], 'request':[], 'size_bytes':[], 'reference':[], 'agent':[]}
	df = None

	for s in f:
		new_line = []
		# clean s from delimeters
		if re.search("( - - )", s) != None:
			delimiter = re.search("( - - )", s).group(0)
			s = s.replace(delimiter, " ")

		# recognize address
		r = s.split(' ')
		address = r[0]
		new_line.append(address)
		s = s.replace(r[0], '#') 
		# get time via regex, cause simple
		re_time = r"(\[[0-9].*[0-9]\])"
		time = re.search(re_time, s).group(0)
		new_line.append(time)
		s = s.replace(time, '#')
		# get request
		r = s.split('"')
		request = '"' + str(r[1]) + '"'
		new_line.append(request)
		s = s.replace(request, '#')
		# get size via regex, cause ez
		re_size = r"([0-9]{1,3} [0-9]{1,9})" 
		size = re.search(re_size, s).group(0)
		new_line.append(size)
		s = s.replace(size, '#')
		# get reference, here if suddenly stays # - means, that it was refered from own ipv4/6 (can not really happen) 
		r = s.split('"')
		reference = '"' + str(r[1]) + '"'
		new_line.append(reference)
		s = s.replace(reference, '#')
		# get agent
		r = s.split('"')
		agent = '"' + str(r[0]) + '"'
		new_line.append(agent)
		s = s.replace(agent, '#')
		# create immense dictionary for data.frame
		# df_dict = {'address':[], 'time':[], 'request':[], 'size_bytes':[], 'reference':[], 'agent':[]}
		df_dict['address'].append(new_line[0])
		df_dict['time'].append(new_line[1])
		df_dict['request'].append(new_line[2])
		df_dict['size_bytes'].append(new_line[3])
		df_dict['reference'].append(new_line[4])
		df_dict['agent'].append(new_line[5])

		df = pd.DataFrame(df_dict)
	return df

if __name__ == '__main__':
	# df = convert_file('access.txt') 
	# print(df.head(5))
	
