import pygame
from logger import log

class Layer:
    def __init__(self, name: str, path: str):
        self.name = name
        self.path = path
        self.x_offset = 0
        self.y_offset = 0
        self.texture = None
        self.scaled_texture = None
        self.scale = 1.0

    def load_texture(self):
        try:
            self.texture = pygame.image.load(self.path).convert_alpha()
            self.scaled_texture = self.texture
            log.debug(f"Textura carregada: '{self.path}' {self.texture.get_size()}")
        except (pygame.error, FileNotFoundError) as e:
            log.error(f"Falha ao carregar textura '{self.path}': {e}")
            self.texture = None
            self.scaled_texture = None

    def apply_scale(self, scale: float):
        if self.texture is None:
            return
        self.scale = scale
        w = max(1, int(self.texture.get_width()  * scale))
        h = max(1, int(self.texture.get_height() * scale))
        self.scaled_texture = pygame.transform.smoothscale(self.texture, (w, h))

    def get_original_size(self):
        if self.texture is None:
            return (0, 0)
        return self.texture.get_size()

    def draw(self, surface, anchor_x, anchor_y):
        if self.scaled_texture is None:
            return

        sw, sh = self.scaled_texture.get_size()
        pos = (
            anchor_x - sw // 2 + self.x_offset,
            anchor_y - sh // 2 + self.y_offset,
        )
        surface.blit(self.scaled_texture, pos)

    def set_offset(self, x: int, y: int):
        self.x_offset = x
        self.y_offset = y

    def get_obj(self):
        return {
            "name": self.name,
            "path": self.path,
            "x_offset": self.x_offset,
            "y_offset": self.y_offset,
        }