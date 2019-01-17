#-*- coding: utf-8 -*-
import json
import pymysql

with open('mysql.json') as f:
	data = json.load(f)

conn = pymysql.connect(host=data["host"],user=data["user"],password=data["password"],db=data["db"],charset=data["charset"])
curs = conn.cursor()

with open('./Working/result.csv','r') as fi:
	lines = fi.readlines()
	for line in lines:
		data = line.split(',')
		sql = """insert into victim (seq,date,name,bank,account,ip,country) 
		values 	(%s,%s,%s,%s,%s,%s,%s);"""
		curs.execute(sql,(data[0],data[1],data[2],data[3],data[4],data[5],data[6]))
conn.commit()
conn.close()