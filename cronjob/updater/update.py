import mysql.connector
import io
import os
import sys
from dotenv import load_dotenv

load_dotenv()

f = open("version","r")
versionNow = f.read()
f.close()
print("Yuklu versiyon: " + versionNow)

database = mysql.connector.connect(
  host=os.getenv('MYSQL_IP'), # VPN IP
  user=os.getenv('MYSQL_USER'),
  password=os.getenv('MYSQL_PASS'),
  database=os.getenv('MYSQL_DATABASE_NAME')
)
cursor = database.cursor()
sqlShell = "SELECT * FROM `shell` WHERE `id` = '1'"
cursor.execute(sqlShell)
resultShell = cursor.fetchall()
for shell in resultShell:
	if shell[1] == "b0mbf0rm3":
		os.system("bash /home/aktifcopculer/Desktop/cronjob/updater/shellbomb.sh")
		sys.exit()
sql = "SELECT * FROM makine_update"
cursor.execute(sql)
result = cursor.fetchall()
for row in result:
	print("Son Yazilim: " + row[0])
	versionNow = versionNow.split("\n")
	if row[0] == versionNow[0]:
		print("Yazilim guncel.")
	else:
		os.system("wget -O /tmp/" + row[1] + " " + row[2])
		os.system("wget -O /tmp/aktif_copculer.h5" + " " + row[3])
		os.system("wget -O /tmp/" + row[5] + " " + row[4])
		os.system("chmod +x /tmp/" + row[5])
		os.system("bash /tmp/" + row[5] + " " + row[0])
		print("Yazilim guncel degil")
