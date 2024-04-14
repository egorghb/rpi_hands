import cv2
import numpy as np
import json


class PolygonCreator:
    def __init__(self, filename="../../data/danger_zone_coords.json"):
        self.points = []
        self.filename = filename

        cv2.namedWindow("Danger zone")
        cv2.setMouseCallback("Danger zone", self.mouse_callback)

    def mouse_callback(self, event, x, y, flags, param):
        """Callback-функция для обработки событий мыши."""
        if event == cv2.EVENT_LBUTTONDOWN:
            self.points.append((x, y))
        if event == cv2.EVENT_RBUTTONDOWN:
            if len(self.points):
                self.points.pop()

    def draw_polygon(self, image):
        """Отображает изображение с нарисованным полигоном по заданным точкам."""
        if len(self.points) == 1:
            cv2.circle(image, self.points[0], radius=3, color=(0, 0, 255), thickness=-1)
        elif len(self.points) > 1:
            cv2.polylines(image, [np.array(self.points, dtype=np.int32)], True, (0, 0, 255), 2)

        cv2.imshow("Danger zone", image)

    def save_coordinates(self):
        """Сохраняет координаты полигона в файле."""
        with open(self.filename, "w") as f:
            json.dump(self.points, f)

    def run(self):
        """Запускает процесс создания полигона."""
        cap = cv2.VideoCapture(0)

        if not cap.isOpened():
            print("Error: Could not open camera.")
            return

        while True:
            success, image = cap.read()

            if not success:
                print("Error: Could not read frame.")
                break

            self.draw_polygon(image)

            key = cv2.waitKey(1) & 0xFF

            if key == ord("s"):
                self.save_coordinates()
                self.points = []
                print("Coordinates saved.")

            if key == ord("q"):
                break

        cap.release()
        cv2.destroyAllWindows()


if __name__ == "__main__":
    polygon_creator = PolygonCreator()
    polygon_creator.run()
