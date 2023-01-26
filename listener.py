import time
import serial
import os
import sys
import cv2
import random
from PIL import Image

def gstreamer_pipeline(
    capture_width=1280,
    capture_height=720,
    display_width=1280,
    display_height=720,
    framerate=60,
    flip_method=1,
):
    return (
        "nvarguscamerasrc ! "
        "video/x-raw(memory:NVMM), "
        "width=(int)%d, height=(int)%d, "
        "format=(string)NV12, framerate=(fraction)%d/1 ! "
        "nvvidconv flip-method=%d ! "
        "video/x-raw, width=(int)%d, height=(int)%d, format=(string)BGRx ! "
        "videoconvert ! "
        "video/x-raw, format=(string)BGR ! appsink"
        % (
            capture_width,
            capture_height,
            framerate,
            flip_method,
            display_width,
            display_height,
        )
    )


def camera():
    time.sleep(2)
    print(gstreamer_pipeline(flip_method=0))
    cap = cv2.VideoCapture(gstreamer_pipeline(flip_method=0), cv2.CAP_GSTREAMER)
    ret_val, img = cap.read()
    cv2.imwrite(img_name, img)
    im = Image.open(img_name)
    im_resized = im.resize([1333, 800], Image.ANTIALIAS)
    im_resized.save(img_name)

serConnection = serial.Serial('/dev/ttyUSB0', 9600)
time.sleep(3)
print("Dinleme Moduna Alindi")
"""
gelen = serConnection.readline()
sonStr = gelen.decode()
sonStr = sonStr.rstrip()
print(sonStr)
"""
while True:
	gelen = serConnection.readline()
	sonStr = gelen.decode()
	sonStr = sonStr.rstrip()
	if sonStr == "2":
		randInt = random.randint(0,100000)
		img_name = ("/home/aktifcopculer/Desktop/img/"+str(randInt) + ".jpg")
		img_oname = ("/home/aktifcopculer/Desktop/img/"+str(randInt) + "_output.jpg")
		image_fname = (str(randInt) + ".jpg")
		image_oname = (str(randInt) + "_output.jpg")
		camera()
		command = ('sudo /usr/bin/python3 /home/aktifcopculer/Desktop/detector.py --model="ondort.onnx" --labels="labels_Son.txt" --input-blob=input_0 --output-cvg=scores --output-bbox=boxes ' + img_name + ' ' + img_oname)
		os.system(command)
	time.sleep(0.25)
