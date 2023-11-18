import cv2
from glob import glob
import os


def capture_frames(*path: str) -> list:
    return glob(os.path.join(*path, '*.jpg'))


