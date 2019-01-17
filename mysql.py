import pymysql

with open('mysql.config','r') as f:
	config = f.readlines()

conn = pymysql.connect(host=config[0][:-1],user=config[1][:-1],password=config[2][:-1],db=config[3][:-1],charset=config[4][:-1])

curs = conn.cursor()

sql = "select * from db"
curs.execute(sql)

print curs.fetchall()