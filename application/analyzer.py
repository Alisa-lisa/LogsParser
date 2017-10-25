import os
import random
import ipaddress
import lzma
import zipfile
import tarfile
import GeoIP as gi


def extract_file(args):
	inF = args['filename']
	tup = os.path.splitext(inF)
	ext = tup[1]
	outF = tup[0]
	print(os.getcwd())
	if ext == '.xz':
		with lzma.open(inF, 'rb') as i:
			with open(outF, 'wb') as o:
				o.write(i.read())
	elif ext == '.zip':
		name = os.path.splitext(inF)[0]
		with zipfile.ZipFile(inF, 'r') as z:
			with open(outF, 'wb') as i:
				i.write(z.read(name))
	elif ext == '.tar':
		with tarfile.open(inF, mode='r|*') as i:
			i.extractall(path='uploads')
	elif ext == '.gz':
		with tarfile.open(inF, mode='r|*') as i:
			i.extractall(path='uploads')	


def make_readable(file):
	inF = file
	outF = os.path.splitext(inF)[0] + '.txt'
	with open(inF, 'rb') as i:
		with open(outF, 'wb') as j:
			j.write(i.read())
	os.remove(inF)
	return str(outF)


def file_info(file):
	f = open(file)
	lines = 0
	size = os.stat(file).st_size
	for line in f:
		lines += 1
	line_size = size / lines
	f.close()
	return size, lines, line_size


# the information about this sampling can be found on https://en.wikipedia.org/wiki/Reservoir_sampling
# in our case S(n) - input file with n lines (we assume n is unknown)
# R(k) - output file called "test_filename.ext" with k lines (k is given in the parameters)
# returns teh name of the file
def reservoir_algo(input_file, sample_size):
	f = open(input_file)
	outF = 'test_' + input_file
	o = open(outF, 'w')
	# get a single random line:
	total_size_b = os.stat(input_file).st_size
	for i in range(0, sample_size):
		rand_line = random.randint(0, total_size_b)
		f.seek(rand_line)
		f.readline()
		r = f.readline()
		o.write(str(r))
	return outF


def parse(s):
	new_line = []
	r = s.split(' ')
	address = r[0]
	new_line.append(address)
	return new_line


def get_statistics(file_name):
	f = open(file_name)
	ip4 = gi.open('tmp/GeoIP.dat', gi.GEOIP_STANDARD)
	ip6 = gi.open("tmp/GeoIPv6.dat", gi.GEOIP_STANDARD)
	false_addresses = 0 # the number of non-valid ipadresses in the log file
	ip_by_country = {'undefined':0} # {'country':int}
	ipv4_total = 0 # total number of the ipv4
	ipv6_total = 0 # total number of the ipv6

	for line in f:
		res = parse(line)
		try:
			if ipaddress.ip_address(res[0]):
				if type(ipaddress.ip_address(res[0])) == ipaddress.IPv4Address:
					ipv4_total += 1
				else:
					ipv6_total += 1
				if ip4.country_name_by_addr(res[0]):
					origin = ip4.country_name_by_addr(res[0])
					if origin not in ip_by_country.keys():
						ip_by_country[origin] = 1
					else:
						ip_by_country[origin] += 1
				elif ip6.country_name_by_addr_v6(res[0]):
					origin = ip6.country_name_by_addr_v6(res[0])
					if origin not in ip_by_country.keys():
						ip_by_country[origin] = 1
					else:
						ip_by_country[origin] += 1
				else:
					ip_by_country['undefined'] += 1	
		except ValueError:
			false_addresses += 1
	return false_addresses, ipv4_total, ipv6_total, ip_by_country
