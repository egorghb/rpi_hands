import numpy as np
import cv2
from shapely.geometry import Polygon


class HandsTracker:
    def __init__(self, padding=10, danger_bbox=None):
        self.padding = padding
        self.danger_bbox_np = np.array(danger_bbox, dtype=np.int32)
        self.danger_bbox_pg = Polygon(danger_bbox)

    def get_bbox(self, image, hands):
        """Возвращает координаты прямоугольника, ограничивающего ладонь"""
        h, w, _ = image.shape
        for hand_landmarks in hands:
            keypoints = np.array([[lm.x * w, lm.y * h] for lm in hand_landmarks.landmark])
            bbox = cv2.boundingRect(keypoints.astype(int))
            x1, y1 = bbox[0] - self.padding, bbox[1] - self.padding
            x2, y2 = bbox[0] + bbox[2] + self.padding, bbox[1] + bbox[3] + self.padding
            yield [x1, y1, x2, y2]

    def is_intersect(self, bbox):
        """Проверка пересечения ладони с опасной зоной"""
        x1, y1, x2, y2 = bbox
        hand_polygon = Polygon([(x1, y1), (x1, y2), (x2, y1), (x2, y2)])
        if hand_polygon.intersects(self.danger_bbox_pg):
            print('---------------------------------')
            print(hand_polygon)
            print(self.danger_bbox_pg)
            print('---------------------------------')
            return True

    def draw_danger_zone(self, image):
        """Отрисовка опасной зоны"""
        return cv2.polylines(image, [self.danger_bbox_np], True, (0, 0, 255), 1)

    def draw_bbox(self, image, bbox):
        """Отрисовка ограничивающего прямоугольника ладони"""
        x1, y1, x2, y2 = bbox
        return cv2.rectangle(image, (x1, y1), (x2, y2), (255, 0, 255), 2)
