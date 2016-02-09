# read the log file
# from llvmlite import binding
# from numba import jit
import os, re
# from multiprocessing import Process
# @jit
def make_readable(file):
	inF = file
	outF = os.path.splitext(inF)[0] + '.txt'
	with open(inF, 'rb') as i:
		with open(outF, 'wb') as j:
			j.write(i.read())
	os.remove(inF)

def convert_file(file):
	# open file for r\w
	f = open(file, 'rb')
	n = os.path.splitext(file)[0] + '_list' + '.txt'
	res = open(n, 'wb')

	# all used regex
	re_ipv6 = r"(([0-9a-fA-F]{1,4}:){7,7}[0-9a-fA-F]{1,4}|([0-9a-fA-F]{1,4}:){1,7}:|([0-9a-fA-F]{1,4}:){1,6}:[0-9a-fA-F]{1,4}|([0-9a-fA-F]{1,4}:){1,5}(:[0-9a-fA-F]{1,4}){1,2}|([0-9a-fA-F]{1,4}:){1,4}(:[0-9a-fA-F]{1,4}){1,3}|([0-9a-fA-F]{1,4}:){1,3}(:[0-9a-fA-F]{1,4}){1,4}|([0-9a-fA-F]{1,4}:){1,2}(:[0-9a-fA-F]{1,4}){1,5}|[0-9a-fA-F]{1,4}:((:[0-9a-fA-F]{1,4}){1,6})|:((:[0-9a-fA-F]{1,4}){1,7}|:)|fe80:(:[0-9a-fA-F]{0,4}){0,4}%[0-9a-zA-Z]{1,}|::(ffff(:0{1,4}){0,1}:){0,1}((25[0-5]|(2[0-4]|1{0,1}[0-9]){0,1}[0-9])\.){3,3}(25[0-5]|(2[0-4]|1{0,1}[0-9]){0,1}[0-9])|([0-9a-fA-F]{1,4}:){1,4}:((25[0-5]|(2[0-4]|1{0,1}[0-9]){0,1}[0-9])\.){3,3}(25[0-5]|(2[0-4]|1{0,1}[0-9]){0,1}[0-9]))"
	re_ipv4 = r"((25[0-5]|(2[0-4]|1{0,1}[0-9]){0,1}[0-9])\.){3,3}(25[0-5]|(2[0-4]|1{0,1}[0-9]){0,1}[0-9])"
	re_time = r"(\[([0-2][0-9]|3[0-1])\/([JjFfMmAaSsOoNnDd][AaEePpUuCcOo][NnBbRrIiNnLlGgPpTtVvCc])\/([1-2][0-9]{3}):([0-1][0-9]|2[0-4]):([0-5][0-9]):([0-5][0-9]) \+[0-9]{4}\])"
	re_request = r"(\"([PHGphg][EOUAeoua][TSAtsa]|[PHGphg][EOUAeoua][TSAtsa][TDHtdh]).{1,80}(HTTP\/1\.1)\")"
	re_digits = r"([0-9]{1,3} [0-9]{1,9})" 
	re_redirect = r"(\"(\-|http:\/\/[^\"]{0,30})\")"
	re_agent = r"(\"[^ -GgHh]{1,300}\")"

	for s in f:
	# for l in res:
		new_line = []
		# get rid of delimiter
		delimiter = re.search("( - - )", s).group(0)
		s = s.replace(delimiter, " ")

		# search for all patterns
		call_time = re.search(re_time, s).group(0)
		ipv6 = re.search(re_ipv6, s).group(0)
		ipv4 = re.search(re_ipv4, s).group(0)
		request_method = re.search(re_request, s).group(0)
		package_size = re.search(re_digits, s).group(0) # in bytes
		internal_rediret = re.search(re_redirect, s).group(0)

		# add patterns to the list
		if ipv6:
			categories = [ipv6, call_time, request_method, package_size, internal_rediret]
		elif ipv4:
			categories = [ipv4, call_time, request_method, package_size, internal_rediret]
		else:
			categories = ["Unknown Address", call_time, request_method, package_size, internal_rediret]
		agent = s
		for i in categories:
			agent = agent.replace(i,'')
		# for some reason the place will be replaced with space and not an empty string
		# this is why we use this weird hack to get proper formatting
		agent = agent[len(categories):-2]
		# put everything into new_line
		for c in categories:
			if c in s:
				new_line.append(c)
		new_line.append(agent)
		res.write(new_line)

	f.close()
	res.close()
	

if __name__ == '__main__':
	file = 'access.txt'
	f = open(file)
	n = os.path.splitext(file)[0] + '_list' + '.txt'
	res = open(n, 'w')

	# all used regex
	re_ipv6 = r"(([0-9a-fA-F]{1,4}:){7,7}[0-9a-fA-F]{1,4}|([0-9a-fA-F]{1,4}:){1,7}:|([0-9a-fA-F]{1,4}:){1,6}:[0-9a-fA-F]{1,4}|([0-9a-fA-F]{1,4}:){1,5}(:[0-9a-fA-F]{1,4}){1,2}|([0-9a-fA-F]{1,4}:){1,4}(:[0-9a-fA-F]{1,4}){1,3}|([0-9a-fA-F]{1,4}:){1,3}(:[0-9a-fA-F]{1,4}){1,4}|([0-9a-fA-F]{1,4}:){1,2}(:[0-9a-fA-F]{1,4}){1,5}|[0-9a-fA-F]{1,4}:((:[0-9a-fA-F]{1,4}){1,6})|:((:[0-9a-fA-F]{1,4}){1,7}|:)|fe80:(:[0-9a-fA-F]{0,4}){0,4}%[0-9a-zA-Z]{1,}|::(ffff(:0{1,4}){0,1}:){0,1}((25[0-5]|(2[0-4]|1{0,1}[0-9]){0,1}[0-9])\.){3,3}(25[0-5]|(2[0-4]|1{0,1}[0-9]){0,1}[0-9])|([0-9a-fA-F]{1,4}:){1,4}:((25[0-5]|(2[0-4]|1{0,1}[0-9]){0,1}[0-9])\.){3,3}(25[0-5]|(2[0-4]|1{0,1}[0-9]){0,1}[0-9]))"
	re_ipv4 = r"((25[0-5]|(2[0-4]|1{0,1}[0-9]){0,1}[0-9])\.){3,3}(25[0-5]|(2[0-4]|1{0,1}[0-9]){0,1}[0-9])"
	re_time = r"(\[([0-2][0-9]|3[0-1])\/([JjFfMmAaSsOoNnDd][AaEePpUuCcOo][NnBbRrIiNnLlGgPpTtVvCc])\/([1-2][0-9]{3}):([0-1][0-9]|2[0-4]):([0-5][0-9]):([0-5][0-9]) \+[0-9]{4}\])"
	re_request = r"(\"([PHGphg][EOUAeoua][TSAtsa]|[PHGphg][EOUAeoua][TSAtsa][TDHtdh]).{1,80}(HTTP\/1\.1)\")"
	re_size = r"([0-9]{1,3} [0-9]{1,9})" 
	re_redirect = r"(\"(\-|http:\/\/[^\"]{0,30})\")"
	re_agent = r"(\"[^ -GgHh]{1,300}\")"
	# ToDo: bind real values with their regex via dict
	regex_list = [re_ipv6, re_ipv4, re_time, re_redirect, re_request, re_size]

	for s in f:
	# for l in res:
		new_line = []
		# get rid of delimiter
		delimiter = re.search("( - - )", s).group(0)
		s = s.replace(delimiter, " ")

		# search for all patterns
		for reg in regex_list:
			if re.search(reg, s) != None:
				call_time = re.search(re_time, s).group(0)
				request_method = re.search(re_request, s).group(0)
				package_size = re.search(re_digits, s).group(0) # in bytes
				internal_rediret = re.search(re_redirect, s).group(0)
				if 
				ipv6 = re.search(re_ipv6, s).group(0)
				ipv4 = re.search(re_ipv4, s).group(0)

		# add patterns to the list
		if ipv6 != None:
			categories = [ipv6, call_time, request_method, package_size, internal_rediret]
		elif ipv4 != None:
			categories = [ipv4, call_time, request_method, package_size, internal_rediret]
		else:
			categories = ["Unknown Address", call_time, request_method, package_size, internal_rediret]
		agent = s
		for i in categories:
			agent = agent.replace(i,'')
		# for some reason the place will be replaced with space and not an empty string
		# this is why we use this weird hack to get proper formatting
		agent = agent[len(categories):-2]
		# put everything into new_line
		for c in categories:
			if c in s:
				new_line.append(c)
		new_line.append(agent)
		res.write(str(new_line))
