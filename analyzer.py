import os, re, random, ipaddress, cProfile, re
import numpy as np
import pandas as pd
import geoip2
import geoip2.database as gipd
from multiprocessing import Pool


# some helper functions
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

def get_statistics(file_name):
	f = open(file_name)
	# create reader object to determine ips origin
	r = gipd.Reader('tmp/GeoLite2-Country.mmdb')
	# global results:
	false_addresses = 0 # the number of non-valid ipadresses in the log file 
	ip_by_country = {'undefined':0} # {'country':int}
	ipv4_total = 0 # total number of the ipv4
	ipv6_total = 0 # total number of the ipv6

	for line in f:
		res = parse(line)
		# validate the address, isAddress, islocal, isPrivate
		try:
			if ipaddress.ip_address(res[0]):
				if type(ipaddress.ip_address(res[0])) == ipaddress.IPv4Address:
					ipv4_total += 1
				else:
					ipv6_total += 1
				# count appereance of each ip of the country country = {'country_name':0}
				try:
					if r.country(res[0]):
						origin = r.country(res[0])
						if origin.country.name not in ip_by_country.keys():
							ip_by_country[str(origin.country.name)] = 1
						else:
							ip_by_country[str(origin.country.name)] += 1
				except geoip2.errors.AddressNotFoundError:
					ip_by_country['undefined'] += 1
		except ValueError:
			false_addresses += 1
	return false_addresses, ipv4_total, ipv6_total, ip_by_country

if __name__ == '__main__':
	# test = reservoir_algo('access.txt', 50000) 
	# errors, ipv4, ipv6, geo = get_statistics('test_access.txt')
	# print(errors, ipv4, ipv6, geo)
	# print(geo['undefined'])

	cProfile.run('re.compile(get_statistics("test_access.txt"))')