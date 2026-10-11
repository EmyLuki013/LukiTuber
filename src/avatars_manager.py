import json
import os

from logger import log
from avatar import Avatar

AVATARS_FILE = "avatars/avatars.json"

class AvatarsManager:
    def __init__(self):
        self.avatars = []

    def create_avatar(self, name: str, dir: str):
        new_avatar = Avatar(name, dir)
        self.avatars.append(new_avatar)
        os.makedirs(dir, exist_ok=True)

    def save_avatars(self):
        avatars_obj = []
        for avatar in self.avatars:
            avatar_obj = avatar.get_obj()
            avatars_obj.append(avatar_obj)

        with open(AVATARS_FILE, 'w', encoding='utf-8') as f:
            log.info(f"Arquivo {AVATARS_FILE} Salvo")
            json.dump(avatars_obj, f, indent=2)

    def load_avatars(self):
        os.makedirs(os.path.dirname(AVATARS_FILE), exist_ok=True)
        
        if not os.path.exists(AVATARS_FILE):
            log.warning(f"Arquivo {AVATARS_FILE} não encontrado. Criando novo arquivo...")
            log.info("Criando Default Avatar...")
            self.create_avatar("Default", "avatars/default") 

            log.info(f"Criando arquivo {AVATARS_FILE}...")
            self.save_avatars()

        with open(AVATARS_FILE, 'r') as file:
            log.info(f"Abrindo arquivo {AVATARS_FILE}...")
            content = file.read()
            avatars_json = json.loads(content)

            log.info("Carregando Avatars...")
            for avatar in avatars_json:
                self.create_avatar(avatar["name"], avatar["dir"])
                log.info(f"Avatar '{avatar["name"]}' Carregado.")