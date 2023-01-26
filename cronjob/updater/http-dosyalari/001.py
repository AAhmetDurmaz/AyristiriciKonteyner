import os
import argparse
import sys

parser = argparse.ArgumentParser(description="Firmware Updated")
parser.add_argument('-mp', '--modelpath', type=str, required=True, help='Model dosya adi')
parser.add_argument('-v', '--version', type=str, required=True ,help='Version numarası')
args = parser.parse_args()

os.system("mv /home/aktifcopculer/Desktop/ssd-mobilenet.onnx /home/aktifcopculer/Desktop/ssd-mobilenet.onnx-Eski")
os.system("mv /tmp/" + args.modelpath + " /home/aktifcopculer/")
os.system("echo " + str(args.version) + " > /home/aktifcopculer/Desktop/retinanet/updater/version")
os.system("python3 /home/aktifcopculer/Desktop/detector.py --modelname " + args.modelpath)
sys.exit()
