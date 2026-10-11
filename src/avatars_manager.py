import json
import os
import shutil

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

    def get_avatar(self, name: str):
        for a in self.avatars:
            if a.name == name:
                return a
        return None

    def create_avatar(self, name: str, dir: str, create_dirs=True):
        if self.get_avatar(name):
            log.warning(f"Avatar '{name}' já existe. Ignorando criação.")
            return self.get_avatar(name)

        new_avatar = Avatar(name, dir)
        self.avatars.append(new_avatar)

        if create_dirs:
            log.info("Criando diretórios do Avatar...")
            for sub in ("body", "eyes", "mouth"):
                os.makedirs(os.path.join(dir, sub), exist_ok=True)

        return new_avatar

    def rename_avatar(self, avatar, new_name: str):
        if not new_name or new_name == avatar.name:
            return
        if self.get_avatar(new_name):
            raise ValueError(f"Já existe um avatar chamado '{new_name}'")

        old_name = avatar.name
        avatar.name = new_name
        log.info(f"Avatar '{old_name}' renomeado para '{new_name}'")

        if self.settings.selected_avatar == old_name:
            self.select_avatar(new_name)

    def delete_avatar(self, avatar, delete_files=False):
        if avatar not in self.avatars:
            return

        self.avatars.remove(avatar)
        log.info(f"Avatar '{avatar.name}' removido da lista")

        if delete_files and os.path.isdir(avatar.dir):
            shutil.rmtree(avatar.dir, ignore_errors=True)
            log.info(f"Diretório '{avatar.dir}' apagado")

        if self.settings.selected_avatar == avatar.name:
            self.settings.selected_avatar = None
            self.settings.save_settings()

    def save_avatars(self):
        os.makedirs(os.path.dirname(AVATARS_FILE), exist_ok=True)

        avatars_obj = [a.get_obj() for a in self.avatars]

        with open(AVATARS_FILE, "w", encoding="utf-8") as f:
            json.dump(avatars_obj, f, indent=2, ensure_ascii=False)

        log.info(f"Arquivo '{AVATARS_FILE}' salvo ({len(avatars_obj)} avatars)")

    def load_avatars(self):
        os.makedirs(os.path.dirname(AVATARS_FILE), exist_ok=True)

        if not os.path.exists(AVATARS_FILE):
            log.warning(f"Arquivo '{AVATARS_FILE}' não encontrado. Criando novo...")

            self.avatars = []
            default = self.create_avatar("Default", "avatars/default")
            self.select_avatar(default.name)
            self.save_avatars()

            log.info("Arquivo inicial criado com avatar 'Default'.")
            return

        with open(AVATARS_FILE, "r", encoding="utf-8") as file:
            content = file.read().strip()

        if not content:
            log.warning(f"Arquivo '{AVATARS_FILE}' vazio. Recriando...")
            self.avatars = []
            default = self.create_avatar("Default", "avatars/default")
            self.select_avatar(default.name)
            self.save_avatars()
            return

        try:
            avatars_json = json.loads(content)
        except json.JSONDecodeError as e:
            log.error(f"JSON inválido em '{AVATARS_FILE}': {e}")
            raise

        self.avatars = []

        log.info("Carregando Avatars...")
        for obj in avatars_json:
            self.create_avatar(obj["name"], obj["dir"], create_dirs=False)
            log.info(f"Avatar '{obj['name']}' carregado.")