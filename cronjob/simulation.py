import os
import sys
import mysql.connector
import random
import datetime
import time
import os
from dotenv import load_dotenv

load_dotenv()

database = mysql.connector.connect(
  host=os.getenv('MYSQL_IP'), # VPN IP
  user=os.getenv('MYSQL_USER'),
  password=os.getenv('MYSQL_PASS'),
  database=os.getenv('MYSQL_DATABASE_NAME')
)
cursor = database.cursor()

il_array = ["Adana", "Adıyaman", "Afyon", "Ağrı", "Amasya", "Ankara", "Antalya", "Artvin", "Aydın", "Balıkesir", "Bilecik", "Bingöl", "Bitlis", "Bolu", "Burdur", "Bursa",
 "Çanakkale", "Çankırı", "Çorum", "Denizli", "Diyarbakır", "Edirne", "Elazığ", "Erzincan", "Erzurum", "Eskişehir", "Gaziantep", "Giresun", "Gümüşhane", "Hakkari", "Hatay",
 "Isparta", "İçel (Mersin)", "İstanbul", "İzmir", "Kars", "Kastamonu", "Kayseri", "Kırklareli", "Kırşehir", "Kocaeli", "Konya", "Kütahya", "Malatya", "Manisa", "K.maraş",
 "Mardin", "Muğla", "Muş", "Nevşehir", "Niğde", "Ordu", "Rize", "Sakarya", "Samsun", "Siirt", "Sinop", "Sivas", "Tekirdağ", "Tokat", "Trabzon", "Tunceli", "Şanlıurfa", "Uşak",
 "Van", "Yozgat", "Zonguldak", "Aksaray", "Bayburt", "Karaman", "Kırıkkale", "Batman", "Şırnak", "Bartın", "Ardahan", "Iğdır", "Yalova", "Karabük", "Kilis", "Osmaniye", "Düzce"]
tarih = datetime.datetime.now()
tarih = tarih.strftime("%Y-%d-%m %X")
deger = input("N Yapmak Istiyorsunuz:\n 1) 10 Adet Makine Ekle\n 2) Simulasyonu Baslat\n 3) Tum Makinelerin Degerlerini Sifirla\n 4) Tum Makineleri Sil\n: ")
if deger == "1":
	count = 0
	ip_count = 19
	while count < 9:
		il_random  = random.randint(0,80)
		device_name = ("device"+str(count))
		makine_ip = ("100.96.1."+str(ip_count + 1))
		sqlMakineEkle = ("""INSERT INTO `makineler`(`makine_ip`, `ssh_username`, `ssh_password`, `il`, `ilce`, `mahalle`, `cadde`, `son_bakim`, `eklenme_tarih`, `ekleyen_id`,
			`gorev_kilit`,`ssh_id_rsa`) VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)""")
		makineValues = (makine_ip, device_name, "not_set", il_array[il_random], "Ilce", "Mahalle", "Sokak/Cadde", tarih, tarih, 1, 0, "not_set")
		cursor.execute(sqlMakineEkle, makineValues)
		sqlUseData = ("INSERT INTO `use_data`(`makine_adi`, `makine_ip`, `cam`, `metal`, `kagit`, `plastik`, `tanimlanamayan`) VALUES (%s,%s,%s,%s,%s,%s,%s)")
		valueUseData = (device_name, makine_ip, "0","0","0","0","0")
		cursor.execute(sqlUseData, valueUseData)
		database.commit()
		ip_count += 1
		count += 1
elif deger == "2":
	os.system("clear")
	while True:
		id_makine = 1
		while id_makine < 10:
			sqlSelect = "SELECT * FROM `use_data` WHERE `id` = %s"
			cursor.execute(sqlSelect, (id_makine,))
			rows = cursor.fetchall()
			for row in rows:
				cam = row[3]
				metal = row[4]
				kagit = row[5]
				plastik = row[6]
				tanimlanamayan = row[7]
			sec = random.randint(0,4)
			if sec == 0:
				sqlUpdate = "UPDATE `use_data` SET cam=%s WHERE `id` = %s"
				if cam >= 30:
					cam = 30
				else:
					cam += 1
				updateValue = (cam, id_makine)
			elif sec == 1:
				sqlUpdate = "UPDATE `use_data` SET metal=%s WHERE `id` = %s"
				if metal >= 30:
					metal = 30
				else:
					metal += 1
				updateValue = (metal, id_makine)
			elif sec == 2:
				sqlUpdate = "UPDATE `use_data` SET kagit=%s WHERE `id` = %s"
				if kagit >= 30:
					kagit = 30
				else:
					kagit += 1
				updateValue = (kagit, id_makine)
			elif sec == 3:
				sqlUpdate = "UPDATE `use_data` SET plastik=%s WHERE `id` = %s"
				if plastik >= 30:
					plastik = 30
				else:
					plastik += 1
				updateValue = (plastik, id_makine)
			elif sec == 4:
				sqlUpdate = "UPDATE `use_data` SET tanimlanamayan=%s WHERE `id` = %s"
				if tanimlanamayan >= 30:
					tanimlanamayan = 30
				else:
					tanimlanamayan += 1
				updateValue = (tanimlanamayan, id_makine)
			print((cam,metal,kagit,plastik,tanimlanamayan))
			cursor.execute(sqlUpdate, updateValue)
			database.commit()
			id_makine += 1
			time.sleep(1)
elif deger == "3":
	msCount = 1
	while msCount < 10:
		sifirlaSql = ("UPDATE `use_data` SET `cam`=0,`metal`=0,`kagit`=0,`plastik`=0,`tanimlanamayan`=0 WHERE `id` = '{}'".format(msCount))
		cursor.execute(sifirlaSql)
		database.commit()
		msCount += 1
elif deger == "4":
	msCount = 1
	while msCount < 10:
		cursor.execute("DELETE FROM `makineler` WHERE `id` = %s", (msCount,))
		cursor.execute("DELETE FROM `use_data` WHERE `id` = %s", (msCount,))
		database.commit()
		msCount += 1
	cursor.execute("ALTER TABLE `makineler` AUTO_INCREMENT = 0")
	cursor.execute("ALTER TABLE `use_data` AUTO_INCREMENT = 0")
	database.commit()
else:
	print("Hatalı girdi yaptınız.")