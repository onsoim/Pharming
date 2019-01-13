import multiprocessing
import requests
import urllib2	# Downloadfiles
import os
import re

def phase1():
	print "[*] Phase1 (Get cert.html)"
	if not os.path.exists('./Working'):
		os.makedirs(os.path.join('./Working'))
	if not os.path.exists('./Working/cert.html'):
		print "=> working on"
		res = requests.get(url)
		with open(os.path.join('./Working/cert.html'), 'w') as f:
			f.write(res.text)

def phase2():
	print "[*] Phase2 (List victim)"
	if not os.path.exists('./Working/victim.txt'):
		print "=> working on"
		with open('./Working/cert.html', 'r') as fi, open('./Working/victim.txt', 'w') as fo:
			data, count = fi.readline(), 0
			while data:
				regex = re.compile('.zip')
				if regex.search(data) != None:
					count += 1
					time = data.split('right">')[1].split('  ')[0]
					ip = data.split('.zip">')[1].split('</a>')[0]
					fo.write("%s,%s,%s\n" %(count, time, ip))
				data = fi.readline()

def phase3():
	print "[*] Phase3 (Download zip)"
	if not os.path.exists('./Working/Downloads'):
		os.makedirs(os.path.join('./Working/Downloads'))
	import subprocess
	num = subprocess.check_output('ls ./Working/Downloads | wc -l', shell=True)
	if num != file_num:
		print "=> working on"
		# 1. Try to download all files
		# 2. Try to download missed files
		for i in range(2):
			jobs = []
			for j in range(7):
				p = multiprocessing.Process(target=download, args=(j, j * 5268,(j + 1) * 5268 - 1))
				jobs.append(p)
				p.start()
			for k in jobs:
				k.join()

def download(procs,start,end):
	with open('./Working/victim.txt', 'r') as fi:
		lines = fi.readlines()[start:end]
		for data in lines:
			filename = './Working/Downloads/[%05s-%s]%s' %(data.split(',')[0], file_num, data.split(',')[2][:-1])
			if not os.path.exists(filename):
				with open(filename, 'w') as fw:
					full_url = url + data.split(',')[2][:-1]
					fw.write(urllib2.urlopen(url + '/' + data.split(',')[2][:-1]).read())
					print('%d - [%05s/%05s/%05s]' %(procs,start,data.split(',')[0],end))

def phase4():
	print "[*] Phase4 (Unzip cert)"
	print "=> working on"



with open('secret.txt','r') as f:
	url = f.readline()
file_num = 36876
phase1()
phase2()
phase3()
#phase4()

