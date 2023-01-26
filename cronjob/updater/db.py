import sqlite3
import mysql.connector
import datetime
import getpass
import netifaces
import os
from dotenv import load_dotenv

load_dotenv()

try:
    database = sqlite3.connect(os.getenv('DATABASE_PATH'))
    cursor = database.cursor()
    print("SQLite baglantisi basarili!")
    cursor.execute("SELECT * FROM use_data")
    row = cursor.fetchall()
    for i in row:
        camDeger = i[0]
        metalDeger = i[1]
        kagitDeger = i[2]
        plastikDeger = i[3]
        tanimlanamayanDeger = i[4]
    print(camDeger, metalDeger, kagitDeger, plastikDeger, tanimlanamayanDeger)
    database.commit()

except sqlite3.Error as error:
    print("SQLite baglanma sirasinda bir hata olustu! - ", error)

database.close()

database = mysql.connector.connect(
  host=os.getenv('MYSQL_IP'), # VPN IP
  user=os.getenv('MYSQL_USER'),
  password=os.getenv('MYSQL_PASS'),
  database=os.getenv('MYSQL_DATABASE_NAME')
)
interface = "tun0"
netifaces.ifaddresses(interface)
makine_ip = netifaces.ifaddresses(interface)[netifaces.AF_INET][0]['addr']
makine_username = getpass.getuser()
cursor = database.cursor()

sql = ("UPDATE `use_data` SET `cam`=%s,`metal`=%s,`kagit`=%s,`plastik`=%s,`tanimlanamayan`=%s WHERE `makine_adi` = %s and `makine_ip` = %s")
values = (camDeger, metalDeger, kagitDeger, plastikDeger, tanimlanamayanDeger, makine_username, makine_ip)
cursor.execute(sql, values)
database.commit()
