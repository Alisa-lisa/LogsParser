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

def convert_file(file):
	# open file for r\w
	f = open(file, 'r')
	n = os.path.splitext(file)[0] + '_list' + '.txt'
	res = open(n, 'w')

	# all used regex

	# ToDo use python ip + validation, Date parser
	re_ipv6 = r"(([0-9a-fA-F]{1,4}:){7,7}[0-9a-fA-F]{1,4}|([0-9a-fA-F]{1,4}:){1,7}:|([0-9a-fA-F]{1,4}:){1,6}:[0-9a-fA-F]{1,4}|([0-9a-fA-F]{1,4}:){1,5}(:[0-9a-fA-F]{1,4}){1,2}|([0-9a-fA-F]{1,4}:){1,4}(:[0-9a-fA-F]{1,4}){1,3}|([0-9a-fA-F]{1,4}:){1,3}(:[0-9a-fA-F]{1,4}){1,4}|([0-9a-fA-F]{1,4}:){1,2}(:[0-9a-fA-F]{1,4}){1,5}|[0-9a-fA-F]{1,4}:((:[0-9a-fA-F]{1,4}){1,6})|:((:[0-9a-fA-F]{1,4}){1,7}|:)|fe80:(:[0-9a-fA-F]{0,4}){0,4}%[0-9a-zA-Z]{1,}|::(ffff(:0{1,4}){0,1}:){0,1}((25[0-5]|(2[0-4]|1{0,1}[0-9]){0,1}[0-9])\.){3,3}(25[0-5]|(2[0-4]|1{0,1}[0-9]){0,1}[0-9])|([0-9a-fA-F]{1,4}:){1,4}:((25[0-5]|(2[0-4]|1{0,1}[0-9]){0,1}[0-9])\.){3,3}(25[0-5]|(2[0-4]|1{0,1}[0-9]){0,1}[0-9]))"
	re_ipv4 = r"((25[0-5]|(2[0-4]|1{0,1}[0-9]){0,1}[0-9])\.){3,3}(25[0-5]|(2[0-4]|1{0,1}[0-9]){0,1}[0-9])"
	re_time = r"(\[.*\])"  #r"(\[([0-2][0-9]|3[0-1])\/([JjFfMmAaSsOoNnDd][AaEePpUuCcOo][NnBbRrIiNnLlGgPpTtVvCc])\/([1-2][0-9]{3}):([0-1][0-9]|2[0-4]):([0-5][0-9]):([0-5][0-9]) \+[0-9]{4}\])"
	re_request = r"(\"([PHGphg][EOUAeoua][TSAtsa]|[PHGphg][EOUAeoua][TSAtsa][TDHtdh]).{1,80}(HTTP\/1\.1)\")"
	re_size = r"([0-9]{1,3} [0-9]{1,9})" 
	re_redirect = r"(\"(\-|http:\/\/[^\"]{0,30})\")"
	re_agent = r"(\"[^ -GgHh]{1,300}\")"

	regex_list = [re_ipv6, re_ipv4, re_time, re_request, re_size, re_redirect]
	existing_regex = regex_list

	for s in f:
		new_line = []
		# get rid of delimiter
		if re.search("( - - )", s) != None:
			delimiter = re.search("( - - )", s).group(0)
			s = s.replace(delimiter, " ")
		# search for the patterns
		for reg in regex_list:
			if re.search(reg, s) == None:
				existing_regex.remove(reg)
			else:
				pass
		# read out the patterns
		for item in existing_regex:
			new_line.append(re.search(item, s).group(0))
		agent = s
		for i in new_line:
			agent = agent.replace(i,'')
		# for some reason the place will be replaced with space and not an empty string
		# this is why we use this weird hack to get proper formatting
		agent = agent[len(existing_regex):-2]
		new_line.append(agent)
		# new_line.append(re.search(arowgent, s).group(0))
		# print(new_line)
		res.write(str(new_line))
	
	

if __name__ == '__main__':
	# convert_file('access.txt') # 
	# f = open('access_list.txt')
	# print(f.readline())



