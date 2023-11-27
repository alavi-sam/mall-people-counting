import cv2
import json
import numpy as np
from utils.dataloaders import IMG_FORMATS, VID_FORMATS


class GetCoordinates:
    def __init__(self, source_input):
        self.frame = None
        self.annotate_frame = None
        self.source_input = source_input
        self.zone_dict = dict()

    def read_source(self):
        if self.source_input.split('.')[-1] in VID_FORMATS:
            print('found video')
            cap = cv2.VideoCapture(self.source_input)
            if not cap.isOpened():
                raise ValueError('Video is corrupted!')
            _, frame = cap.read()
            self.frame = frame
            cap.release()
            return frame

        elif self.source_input.split('.')[-1] in IMG_FORMATS:
            frame = cv2.imread(self.source_input)
            self.frame = frame
            return frame
        else:
            raise ValueError('You must input a video or image source. Wrong format!')

    def click_event(self, event, x, y, flags, param):
        if event == cv2.EVENT_LBUTTONDOWN:
            if param not in self.zone_dict:
                self.zone_dict[param] = list()
            self.zone_dict[param].append((x, y))
            cv2.circle(self.annotate_frame, (x, y), 3, (0, 255, 255), -1)

    def annotate_zone(self, zone_name):
        self.annotate_frame = self.frame.copy()
        cv2.namedWindow(f'zone {zone_name}')
        cv2.setMouseCallback(f'zone {zone_name}', self.click_event, zone_name)
        while True:
            cv2.imshow(f'zone {zone_name}', self.annotate_frame)
            k = cv2.waitKey(1) & 0xFF
            if k == 27:
                break
        cv2.destroyWindow(f'zone {zone_name}')

        self.annotate_frame = self.draw_zone(zone_name)
        cv2.imshow(f'zone drawn for {zone_name}', self.annotate_frame)
        k = cv2.waitKey(0) & 0xFF
        if k in (110, 121):
            cv2.destroyWindow(f'zone drawn for {zone_name}')
        if k == 110:
            self.annotate_frame = self.frame
            self.annotate_zone(zone_name)

    def draw_zone(self, zone_name):
        def is_clockwise(vertices):
            # Calculate the signed area using the Shoelace formula
            area = 0.5 * np.sum(np.cross(vertices, np.roll(vertices, 1, axis=0), axis=1))
            return area < 0

        polygon_vertices = np.array(self.zone_dict[zone_name], dtype=np.float32)
        # Check if the vertices are ordered clockwise
        if is_clockwise(polygon_vertices):
            # Reverse the order of vertices to make them counterclockwise
            polygon_vertices = np.flipud(polygon_vertices)

        self.zone_dict[zone_name] = polygon_vertices.reshape((-1, 1, 2)).astype(np.int32)
        cv2.polylines(self.annotate_frame, [self.zone_dict[zone_name]], color=(0, 255, 0), thickness=3, isClosed=True)
        return self.annotate_frame


get_zone = GetCoordinates('output.mp4')
sample_frame = get_zone.read_source()
get_zone.annotate_zone('ghorfe')




