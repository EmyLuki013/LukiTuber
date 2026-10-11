import json
import os

from logger import log

SETTINGS_FILE = "settings.json"

class Settings:
    def __init__(self):
        self.selected_avatar = None

    def load_settings(self):
        if not os.path.exists(SETTINGS_FILE):
            log.warning(f"Arquivo '{SETTINGS_FILE}' não encontrado. Criando novo arquivo...")
            self.save_settings()

        with open(SETTINGS_FILE, 'r') as file:
            log.info(f"Abrindo arquivo '{SETTINGS_FILE}'...")
            content = file.read()
            settings_json = json.loads(content)
            
            log.info("Carregando Configurações...")
            self.selected_avatar = settings_json["selected_avatar"]  

    def save_settings(self):
        settings_obj = {
            "selected_avatar": self.selected_avatar
        }

        with open(SETTINGS_FILE, 'w', encoding='utf-8') as f:
            log.info(f"Arquivo '{SETTINGS_FILE}' Salvo")
            json.dump(settings_obj, f, indent=2)

global_settings = Settings()