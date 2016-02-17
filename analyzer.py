# read the log file
# from llvmlite import binding
# from numba import jit
import os, re, random
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

# the information about this sampling can be found on https://en.wikipedia.org/wiki/Reservoir_sampling
# in our case S(n) - input file with n lines (we assume n is unknown)
# R(k) - output file called "test_filename.ext" with k lines (k is given in the parameters)
# returns teh name of the file
def reservoir_algo(input, sample_size):
	f = open(input)
	# outF = 'test_' + input
	# get a single random line:
	total_size_b = os.stat(input).st_size
	rand_line = random.randint(0, total_size_b)
	f.seek(rand_line)
	f.readline()
	return f.readline()


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
		# here can also happen, that no agent ingo is provided, in this case we need to distinguish between "-" and "-" 
		r = s.split('"')
		reference = '"' + str(r[1]) + '"'
		new_line.append(reference)
		# here we need a check, that something is still left for agent, if not -> agent = '"-"'
		# if there were no agent info provided, than s looks like this: '# # # # # #', it contains 6 signs '#'
		s = s.replace(reference, '#')
		# agent info is provided
		if s.count('#') < 6:
			# get agent normally
			r = s.split('"')
			agent = '"' + str(r[1]) + '"'
			new_line.append(agent)
			s = s.replace(agent, '#')
		else:
			agent = '"-"' 
			new_line.append(agent)
		# create immense dictionary for data.frame
		# df_dict = {'address':[], 'time':[], 'request':[], 'size_bytes':[], 'reference':[], 'agent':[]}
		df_dict['address'].append(new_line[0])
		df_dict['time'].append(new_line[1])
		df_dict['request'].append(new_line[2])
		df_dict['size_bytes'].append(new_line[3])
		df_dict['reference'].append(new_line[4])
		df_dict['agent'].append(new_line[5])
		df = pd.DataFrame(df_dict)

		# test function, to know where we got the parse error
		print(len(df['address']))
	return df

if __name__ == '__main__':
	# df = convert_file('test.txt') 
	# print(len(df['address']))
	r = reservoir_algo('access.txt', 10)
	print(r)

