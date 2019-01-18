import multiprocessing
import requests
import urllib2	# Downloadfiles
import os
import io
from geoip import geolite2 as geoip
import json

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
	if not os.path.exists('./Working/result.csv'):
		print "=> working on"
		with open('./Working/cert.html', 'r') as fi, open('./Working/result.csv', 'w') as fo:
			#fo.write('Serial Number,Upload Time,Name,Bank,Account Number,IP,Country\n')
			data, count = fi.readline(), 0
			import re
			while data:
				regex = re.compile('.zip')
				if regex.search(data) != None:
					count += 1
					time = data.split('right">')[1].split('  ')[0]
					ip = data.split('.zip">')[1].split('</a>')[0]
					fo.write("%s,%s,,,,%s\n" %(count, time, ip[:-4]))
				data = fi.readline()

def phase3():
	print "[*] Phase3 (Download zip)"
	if not os.path.exists('./Working/Downloads'):
		os.makedirs(os.path.join('./Working/Downloads'))
	import subprocess
	num = subprocess.check_output('ls ./Working/Downloads | wc -l', shell=True).lstrip()
	if int(num) != file_num:
		print "=> working on"
		jobs = []
		for j in range(7):
			p = multiprocessing.Process(target=download, args=(j, j * 5268,(j + 1) * 5268))
			jobs.append(p)
			p.start()
		for k in jobs:
			k.join()

def download(procs,start,end):
	redown = []
	with open('./Working/result.csv', 'r') as fi:
		lines = fi.readlines()[start:end]
		for data in lines:
			num, ip = data.split(',')[0], data.split(',')[5][:-1]
			filename = './Working/Downloads/[%05s-%s]%s.zip' %(num, file_num, ip)
			if not os.path.exists(filename):
				try:
					with open(filename, 'w') as fw:
						full_url = url + ip + '.zip'
						fw.write(urllib2.urlopen(full_url).read())
					# print('%d - [%05s/%05s/%05s]' %(procs,start,num,end))
				except:
					os.remove(filename)
					redown.append(filename)
					print "Error on %sth process - %s" %(procs, filename)
	for file in redown:
		with open(file, 'w') as fw:
			full_url = url + file.split(']')[1]
			fw.write(urllib2.urlopen(full_url).read())
			print('Redownload %s' %(file))

def phase4():
	print "[*] Phase4 (Unzip cert)"
	print "=> working on"
	if not os.path.exists('./Working/Unzip'):
		os.makedirs(os.path.join('./Working/Unzip'))
	files = os.listdir('./Working/Downloads')
	import zipfile
	for file in files:
		if not os.path.exists('./Working/Unzip/' + file[:-4]):
			os.makedirs(os.path.join('./Working/Unzip/' + file[:-4]))
			unzip = zipfile.ZipFile('./Working/Downloads/' + file)
			unzip.extractall('./Working/Unzip/' + file[:-4])

def phase5(): # https://pythonhosted.org/python-geoip/
	print "[*] Phase5 (Extract data)"
	print "=> working on"
	files = os.listdir('./Working/Unzip/')
	with open('./Working/result.csv','r') as fi:
		lines = fi.readlines()
	with io.open('./Working/result.csv','w', encoding='utf8') as fo:
#	with open('./Working/result.csv','w') as fo:
		#fo.write(unicode('Serial Number,Upload Time,Name,Bank,Account Number,IP,Country\n'))
		for i in range(36876):
			csv,file = lines[i],'./Working/Unzip/' + files[i] + '/signCert.cert'
			with open(file,'r') as fi:
				cert = fi.readline().decode('cp949')
				num, time, name, bank, account, ip = \
				csv.split(',')[0], csv.split(',')[1], cert.split('=')[1].split('(')[0], cert.split('=')[2].split(',')[0], \
				cert.split(')')[1].split(',')[0], csv.split(',')[5][:-1]
				import subprocess
				#try:
					# ipinfo - 1,000 requests per day
					#cn = subprocess.check_output('curl ipinfo.io/' + ip, shell=True).split('country": "')[1].split('"')[0]
				try:
					cn = geoip.lookup(ip).country
				except:
					cn = "None"
				fo.write("%s,%s,%s,%s,%s,%s,%s,\n" %(num, time, unicode(name), bank, account, ip, cn))
'''
import os, sys
print os.getcwd()
sys.path.insert(0, os.getcwd())
'''

from module import vpn

import subprocess
ip = subprocess.check_output('curl ifconfig.me', shell=True)
while not vpn.checkConnection(ip):
	vpn.connect()

with open('parse.json') as f:
	url = json.load(f)['url']

file_num = 36876
phase1()
phase2()
phase3()
phase4()
phase5()
