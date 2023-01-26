#!/bin/bash
pkill python3
python3 /tmp/001.py --modelpath ssd-mobilenet.onnx --version $1
