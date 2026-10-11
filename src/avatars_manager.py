import json
import os

from logger import log
from avatar import Avatar
from settings import global_settings

AVATARS_FILE = "avatars/avatars.json"

class AvatarsManager:
    def __init__(self):
        self.avatars = []
        self.settings = global_settings

    def select_avatar(self, avatar_name):
        self.settings.selected_avatar = avatar_name
        log.info(f"Avatar '{avatar_name}' selecionado")
        self.settings.save_settings()

    def create_avatar(self, name: str, dir: str, create_dirs=True):
        new_avatar = Avatar(name, dir)
        self.avatars.append(new_avatar)
        
        if create_dirs:
            log.info("Criando diretórios do Avatar...")
            
            body_dir = f"{dir}/body"
            eyes_dir = f"{dir}/eyes"
            mouth_dir = f"{dir}/mouth"
    
            os.makedirs(dir, exist_ok=True)
            os.makedirs(body_dir, exist_ok=True)
            os.makedirs(eyes_dir, exist_ok=True)
            os.makedirs(mouth_dir, exist_ok=True)

    def save_avatars(self):
        avatars_obj = []
        for avatar in self.avatars:
            avatar_obj = avatar.get_obj()
            avatars_obj.append(avatar_obj)

        with open(AVATARS_FILE, 'w', encoding='utf-8') as f:
            log.info(f"Arquivo '{AVATARS_FILE}' Salvo")
            json.dump(avatars_obj, f, indent=2)

    def load_avatars(self):
        os.makedirs(os.path.dirname(AVATARS_FILE), exist_ok=True)
        
        if not os.path.exists(AVATARS_FILE):
            log.warning(f"Arquivo '{AVATARS_FILE}' não encontrado. Criando novo arquivo...")

            log.info("Criando Default Avatar...")
            avatar_name = "Default"
            self.create_avatar(avatar_name, "avatars/default")
            self.select_avatar(avatar_name)

            log.info(f"Criando arquivo '{AVATARS_FILE}'...")
            self.save_avatars()

        with open(AVATARS_FILE, 'r') as file:
            log.info(f"Abrindo arquivo '{AVATARS_FILE}'...")
            content = file.read()
            avatars_json = json.loads(content)

            log.info("Carregando Avatars...")
            for avatar in avatars_json:
                self.create_avatar(avatar["name"], avatar["dir"], False)
                log.info(f"Avatar '{avatar["name"]}' Carregado.")