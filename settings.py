import json


def load_settings(filename="settings.json"):
    """Загружает настройки приложения"""
    try:
        with open(filename, "r") as f:
            return json.load(f)
    except FileNotFoundError:
        print(f"Error:File {filename} not found.")


settings = load_settings()

show_fps = settings.get("show_fps", True)
draw_hand_skeleton = settings.get("draw_hand_skeleton", False)
draw_bounding_box = settings.get("draw_bounding_box", True)
draw_danger_zone = settings.get("draw_danger_zone", True)
camera_path = settings.get("camera_path", 0)
