# read the log file
# from llvmlite import binding
# import numba
# from numba import jit
import os, re, random, ipaddress
import numpy as np
import pandas as pd
import geoip2.database as gipd
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

# count the number of lines in the file, the size of the file and approximate size of a line in bytes
def file_info(file):
	f = open(file)
	lines = 0
	line_size = 0
	size = os.stat(file).st_size
	for l in f:
		lines += 1
	line_size = size / lines

	return size, lines, line_size

# the information about this sampling can be found on https://en.wikipedia.org/wiki/Reservoir_sampling
# in our case S(n) - input file with n lines (we assume n is unknown)
# R(k) - output file called "test_filename.ext" with k lines (k is given in the parameters)
# returns teh name of the file
def reservoir_algo(input, sample_size):
	f = open(input)
	outF = 'test_' + input
	o = open(outF, 'w')
	# get a single random line:
	total_size_b = os.stat(input).st_size
	for i in range(0, sample_size):
		rand_line = random.randint(0, total_size_b)
		f.seek(rand_line)
		f.readline()
		r = f.readline()
		o.write(str(r))
	return outF

# we parse only a string, so let's use string as input parameter
def parse(s):
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
	return new_line

# split the file into chunks, create DataFrame for each chunk, process separately, save results into globals, clear all
def split_file(file, split_faktor):
	pass

if __name__ == '__main__':
	# global results:
	false_addresses = 0 # the number of non-valid ipadresses in the log file 
	ip_by_country = {} # {'country':int}
	ipv4_total = 0 # total number of the ipv4
	ipv6_total = 0 # total number of the ipv6
	# count appearance for an ip from a country = {'country_name':0}
	countries = {}

	# test splitting
	s, l, ls = file_info('test.txt')
	print(s, l, ls)
	f = open('test.txt')
	# split file into chunks, save to df and process, save results to the global variables
	# split into 11 chunks and then combine it all together
	# Currently only last df is given back => no processing yet
	for j in range(0, l, 10):
		d = {'address':[], 'time':[], 'request':[], 'size':[], 'refer':[], 'agent':[]}
		for i in range(0 + j,10 + j):
			s = f.readline()
			res = parse(s)
			d['address'].append(res[0])
			d['time'].append(res[1])
			d['request'].append(res[2])
			d['size'].append(res[3])
			d['refer'].append(res[4])
			d['agent'].append(res[5])
	df = pd.DataFrame(d)
	# validate the address, isAddress, islocal, isPrivate
	# if ipv6 or ipv4 -> True, else False
	df['valid_ip'] = True
	# create reader object to determine ips origin
	r = gipd.Reader('tmp/GeoLite2-Country.mmdb')

	for i in range(0, len(df)):
		try:
			if ipaddress.ip_address(df['address'][i]):
				# create new column with fasle or true
				df['valid_ip'][i] = True
				# count ipv4 and ipv6
				if type(ipaddress.ip_address(df['address'][i])) == ipaddress.IPv4Address:
					ipv4_total += 1
				else:
					ipv6_total += 1
				# count appereance of each ip of the country country = {'country_name':0}
				res = r.country(df['address'][i])
				if res.country.name not in countries.keys():
					countries[str(res.country.name)] = 1
				else:
					countries[str(res.country.name)] += 1

		except ValueError:
			print('here we see a problem!')
			df['valid_ip'][i] = False	
			# count false ip 
			false_addresses += 1

	print(df)

	print('false_addresses:', false_addresses)
	print('ipv6_total:', ipv6_total)
	print('ipv4_total:', ipv4_total)
	print('countries:', countries)