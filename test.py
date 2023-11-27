# from yolov5.utils import dataloaders
from utils.dataloaders import LoadStreams
import sys
import cv2
from models.common import DetectMultiBackend
import numpy as np


sys.stdout.reconfigure(encoding='utf-8')
sys.stdin.reconfigure(encoding='utf-8')

dataset = LoadStreams('output.mp4')
for path, img, im0s, vid_cap, idk in dataset:
    print(path, img, im0s, idk)
    print('done')
    cv2.imshow('img', (img))
    cv2.imshow('im0s', im0s)
    cv2.imshow('vid_cap', vid_cap)
    cv2.WaitKey(0)
    break
print()
