import json
import os

from logger import log

SETTINGS_FILE = "settings.json"

class Settings:
    def __init__(self):
        self.selected_avatar = None
        self.selected_microphone = None

        self.mic_threshold_open = 0.02
        self.mic_threshold_big  = 0.08
        self.mic_threshold_close = 0.01
        self.mic_smoothing = 0.4

    def load_settings(self):
        if not os.path.exists(SETTINGS_FILE):
            log.warning(...)
            self.save_settings()

        with open(SETTINGS_FILE, 'r', encoding="utf-8") as f:
            content = f.read()
            data = json.loads(content)

            self.selected_avatar     = data.get("selected_avatar", None)
            self.selected_microphone = data.get("selected_microphone", None)
            self.mic_threshold_open  = data.get("mic_threshold_open", 0.02)
            self.mic_threshold_big   = data.get("mic_threshold_big", 0.08)
            self.mic_threshold_close = data.get("mic_threshold_close", 0.01)
            self.mic_smoothing       = data.get("mic_smoothing", 0.4)

    def save_settings(self):
        obj = {
            "selected_avatar": self.selected_avatar,
            "selected_microphone": self.selected_microphone,
            "mic_threshold_open": self.mic_threshold_open,
            "mic_threshold_big": self.mic_threshold_big,
            "mic_threshold_close": self.mic_threshold_close,
            "mic_smoothing": self.mic_smoothing,
        }
        with open(SETTINGS_FILE, 'w', encoding='utf-8') as f:
            json.dump(obj, f, indent=2, ensure_ascii=False)

    def lipsync_config(self):
        return {
            "threshold_open": self.mic_threshold_open,
            "threshold_big": self.mic_threshold_big,
            "threshold_close": self.mic_threshold_close,
            "smoothing": self.mic_smoothing,
        }

global_settings = Settings()