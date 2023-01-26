#!/usr/bin/python3

# Bilgilendirme: Bu kod parçasını güncellerken Python dilini öğrenme aşamasındaydım.
# Eğer incelerseniz göreceğiniz dilin rezalet bir şekilde kullanılmasından dolayı 
# tüm Python geliştiricilerinden özür dilerim :)
# Bu kod parçasına baktığımda sadece güzel anılar hatırlıyorum.
# Bana bu anıları yaşatan kardeşlerime buradan gizli bir şekilde teşekkür ederim.
# Uzun seneler boyunca burada kalması dileğiyle...

import jetson.inference
import jetson.utils
import argparse
import sys
import os
import mysql.connector
import sqlite3
import time
import random
import datetime
import getpass
import netifaces
import serial
from dotenv import load_dotenv

load_dotenv()

interface = 'lo'

netifaces.ifaddresses(interface)
makine_ip = netifaces.ifaddresses(interface)[netifaces.AF_INET][0]['addr']
makine_username = getpass.getuser()
print("Detector yuklendi")
try:
    database = sqlite3.connect('data.db')
    cursor = database.cursor()
    print("SQLite baglantisi basarili!")
    cursor.execute("SELECT * FROM use_data")
    row = cursor.fetchall()
    for i in row:
        camDeger = i[0]
        camD1 = i[0]
        metalDeger = i[1]
        metalD1 = i[1]
        kagitDeger = i[2]
        kagitD1 = i[2]
        plastikDeger = i[3]
        plastikD1 = i[3]
        tanimlanamayanDeger = i[4]
        tanimlanamayanD1 = i[4]
    database.commit()
except sqlite3.Error as error:
    print("SQLite baglanma sirasinda bir hata olustu! Yetkili servise yonlendirildi!")
    file = open("/tmp/aktif_copculer_log.txt","w")
    file.write(str(error))
    file.close()
    mysql = mysql.connector.connect(
			host=os.getenv('MYSQL_IP'), # VPN IP
			user=os.getenv('MYSQL_USER'),
			password=os.getenv('MYSQL_PASS'),
			database=os.getenv('MYSQL_DATABASE_NAME')
    )
    sql = ("UPDATE `use_data` SET `ozel_bakim` = '1' WHERE `makine_ip` = %s and `makine_adi` = %s")
    valuesIP = (makine_ip, makine_username)
    cursorIP = mysql.cursor()
    cursorIP.execute(sql, valuesIP)
    mysql.commit()
    mysql.close()
    sys.exit()


parser = argparse.ArgumentParser(description="Locate objects in a live camera stream using an object detection DNN.", 
                                 formatter_class=argparse.RawTextHelpFormatter, epilog=jetson.inference.detectNet.Usage() +
                                 jetson.utils.videoSource.Usage() + jetson.utils.videoOutput.Usage() + jetson.utils.logUsage())

parser.add_argument("input_URI", type=str, default="", nargs='?', help="URI of the input stream")
parser.add_argument("output_URI", type=str, default="", nargs='?', help="URI of the output stream")
parser.add_argument("--network", type=str, default="ssd-mobilenet-v2", help="pre-trained model to load (see below for options)")
parser.add_argument("--overlay", type=str, default="box,labels,conf", help="detection overlay flags (e.g. --overlay=box,labels,conf,none)")
parser.add_argument("--threshold", type=float, default=0.5, help="minimum detection threshold to use") 

is_headless = ["--headless"] if sys.argv[0].find('console.py') != -1 else [""]

try:
	opt = parser.parse_known_args()[0]
except:
	print("")
	parser.print_help()
	sys.exit(0)
net = jetson.inference.detectNet(opt.network, sys.argv, opt.threshold)
input = jetson.utils.videoSource(opt.input_URI, argv=sys.argv)
output = jetson.utils.videoOutput(opt.output_URI, argv=sys.argv+is_headless)

camArray = ["1"]
plastikArray = ["2","3","4","8","9"]
metalArray = ["5"]
kagitArray = ["6","7","10","11"]

ser = serial.Serial("/dev/ttyUSB0", 9600)
while True:
	img = input.Capture()
	detections = net.Detect(img, overlay=opt.overlay)
	if len(detections) == 0:
		tanimlanamayanDeger += 1
		sqlQuery = ("UPDATE use_data SET tanimlanamayan = {} WHERE 1".format(tanimlanamayanDeger))
		ser.write(str.encode("3"))
		print("# ------------- #")
		print('tanimlanamadi')
		print("# ------------- #")
		cursor.execute(sqlQuery)
		database.commit()
		database.close()
	for detection in detections:
		detectedID = (detection.ClassID)
		detectedID = str(detectedID)
		print("DETECTED: " + detectedID)
		if detectedID in camArray:
			camDeger += 1
			sqlQuery = ("UPDATE use_data SET cam = {} WHERE 1".format(camDeger))
			ser.write(str.encode("4"))
			print("# ------------- #")
			print('cam')
			print("# ------------- #")
			cursor.execute(sqlQuery)
			database.commit()
			database.close()
		elif detectedID in metalArray:
			metalDeger += 1
			sqlQuery = ("UPDATE use_data SET metal = {} WHERE 1".format(metalDeger))
			ser.write(str.encode("6"))
			print("# ------------- #")
			print('metal')
			print("# ------------- #")
			cursor.execute(sqlQuery)
			database.commit()
			database.close()
		elif detectedID in kagitArray:
			kagitDeger += 1
			sqlQuery = ("UPDATE use_data SET kagit = {} WHERE 1".format(kagitDeger))
			ser.write(str.encode("2"))
			print("# ------------- #")
			print('kagit')
			print("# ------------- #")
			cursor.execute(sqlQuery)
			database.commit()
			database.close()
		elif detectedID in plastikArray:
			plastikDeger += 1
			sqlQuery = ("UPDATE use_data SET plastik = {} WHERE 1".format(plastikDeger))
			ser.write(str.encode("5"))
			print("# ------------- #")
			print('plastik')
			print("# ------------- #")
			cursor.execute(sqlQuery)
			database.commit()
			database.close()
		else:
			tanimlanamayanDeger += 1
			sqlQuery = ("UPDATE use_data SET tanimlanamayan = {} WHERE 1".format(tanimlanamayanDeger))
			ser.write(str.encode("6"))
			print("# ------------- #")
			print('tanimlanamadi')
			print("# ------------- #")
			cursor.execute(sqlQuery)
			database.commit()
			database.close()

	output.Render(img)
	ser.write(str.encode("1"))
	# output.SetStatus("{:s} | Network {:.0f} FPS".format(opt.network, net.GetNetworkFPS()))
	net.PrintProfilerTimes()
	if not input.IsStreaming() or not output.IsStreaming():
		break
sys.exit()                                             
