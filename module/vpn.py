import subprocess
import os

def connect():
	subprocess.Popen(['osascript',os.getcwd() + '/module/vpn/connect.applescript'])

def disconnect():
	x = subprocess.Popen(['osascript',os.getcwd() + '/module/vpn/disconnect.applescript'])

def checkConnection(ip):
	import time
	from geoip import geolite2 as geoip
	time.sleep(3)
	result = subprocess.check_output('curl ifconfig.me', shell=True)
	country = geoip.lookup(result).country
	if ip != result or country != "KR":
		print "VPN is working!(%s)" %(country)
		return 1
	else:
		print "VPN is not working"
		return 0