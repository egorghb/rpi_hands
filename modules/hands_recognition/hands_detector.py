import cv2
import mediapipe as mp


class HandsDetector:
    def __init__(self, min_detection_confidence=0.5, min_tracking_confidence=0.5, max_num_hands=2):
        self.hands_detector = mp.solutions.hands.Hands(
            model_complexity=0,
            min_detection_confidence=min_detection_confidence,
            min_tracking_confidence=min_tracking_confidence,
            max_num_hands=max_num_hands
        )
        self.mp_drawing = mp.solutions.drawing_utils
        self.mp_drawing_styles = mp.solutions.drawing_styles
        self.mp_hands = mp.solutions.hands

    def detect(self, image):
        """Распознавание рук в кадре"""
        image_rgb = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
        results = self.hands_detector.process(image_rgb)

        return results.multi_hand_landmarks

    def draw_hands(self, image, hands):
        """Отрисовка скелета ладони"""
        for hand_landmarks in hands:
            self.mp_drawing.draw_landmarks(
                image,
                hand_landmarks,
                self.mp_hands.HAND_CONNECTIONS,
                self.mp_drawing_styles.get_default_hand_landmarks_style(),
                self.mp_drawing_styles.get_default_hand_connections_style())

        return image

    def release(self):
        self.hands_detector.close()
