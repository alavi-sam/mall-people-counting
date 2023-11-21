import cv2
import json
from utils.dataloaders import IMG_FORMATS, VID_FORMATS


def click_event(event, x, y, **kwargs):
    if event == cv2.EVENT_LBUTTONDOWN:
        return x, y


def get_coordinates(source_path):
    source_format = source_path.split('.')[-1]
    if source_format in VID_FORMATS:
        cap = cv2.VideoCapture(source_path)
        if not cap.isOpened():
            raise ValueError('Corrupted video!')
        else:
            _, frame = cap.read()
            cap.release()
    elif source_format in IMG_FORMATS:
        frame = cv2.imread(source_path)
    else:
        raise ValueError('WRONG FORMAT INPUT!')

    zone_dict = dict()
    esc_keyword = None
    while esc_keyword != 'end':
        zone_name = input('zone name:  ')
        zone_dict[zone_name] = list()
        cv2.namedWindow(f'annotate {zone_name}')
        for _ in range(4):
            x, y = cv2.setMouseCallback(f'annotate {zone_name}', click_event)
            zone_dict[zone_name].append((x, y))
        final_frame = frame.copy()
        for idx in range(len(zone_dict[zone_name])):
            try:
                final_frame = cv2.line(final_frame,
                                       zone_dict[zone_name][idx],
                                       zone_dict[zone_name][idx+1], color=(0, 255, 0))



get_coordinates('output.mp4')


