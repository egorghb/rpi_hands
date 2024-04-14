from modules.hands_recognition import HandsDetector, HandsTracker
import cv2
import settings
import json
from datetime import datetime


def load_coordinates(filename="data/danger_zone_coords.json"):
    """Загружает координаты полигона из файла."""
    try:
        with open(filename, "r") as f:
            points = json.load(f)
        print("Coordinates loaded.")
    except FileNotFoundError:
        print(f"Error: File {filename} not found.")

    return points


def main():
    cap = cv2.VideoCapture(settings.camera_path)
    if not cap.isOpened():
        print("Error: Could not open video capture")
        return

    hands_detector = HandsDetector()
    hands_tracker = HandsTracker(danger_bbox=load_coordinates())

    import time
    fps = 0
    frames_processed = frames_processed_all = 0
    start_time = start_time_avg = time.time()

    while cap.isOpened():
        success, image = cap.read()
        if not success:
            continue

        hands = hands_detector.detect(image)
        if hands:
            for bbox in hands_tracker.get_bbox(image, hands):
                if hands_tracker.is_intersect(bbox):
                    print("warning")
                    cv2.imwrite(f'./logs/{datetime.now()}.jpeg', image)
                if settings.draw_bounding_box:
                    hands_tracker.draw_bbox(image, bbox)
                if settings.draw_hand_skeleton:
                    hands_detector.draw_hands(image, hands)

        if settings.draw_danger_zone:
            hands_tracker.draw_danger_zone(image)

        frames_processed_all += 1
        frames_processed += 1
        if time.time() - start_time >= 1:
            fps = frames_processed / (time.time() - start_time)
            frames_processed = 0.0
            start_time = time.time()

        if settings.show_fps:
            cv2.putText(image, f'FPS: {int(fps)}', (500, 30), cv2.FONT_HERSHEY_PLAIN, 2, (255, 0, 0), 2)

        cv2.flip(image, 1)
        cv2.imshow('Hands', image)
        if cv2.waitKey(1) & 0xFF == ord("q"):
            break

    cap.release()
    cv2.destroyAllWindows()
    hands_detector.release()

    print(f'AVG FPS: {int(frames_processed_all / (time.time() - start_time_avg))}')


if __name__ == '__main__':
    main()
