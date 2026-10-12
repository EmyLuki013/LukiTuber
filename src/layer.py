import pygame
from logger import log

PLACEHOLDER_SIZE = (200, 200)

def _make_placeholder(name: str, size=PLACEHOLDER_SIZE) -> pygame.Surface:
    h = abs(hash(name)) % 360
    color = pygame.Color(0)
    color.hsva = (h, 80, 90, 100)

    surface = pygame.Surface(size, pygame.SRCALPHA)
    surface.fill((color.r, color.g, color.b, 255))

    pygame.draw.rect(surface, (0, 0, 0, 255), surface.get_rect(), width=3)

    try:
        font = pygame.font.SysFont("consolas", 14, bold=True)
        text = font.render(name, True, (0, 0, 0))
        text_rect = text.get_rect(center=(size[0] // 2, size[1] // 2))
        surface.blit(text, text_rect)
    except Exception:
        pass

    return surface


class Layer:
    def __init__(self, name: str, path: str):
        self.name = name
        self.path = path
        self.x_offset = 0
        self.y_offset = 0
        self.texture = None
        self.scaled_texture = None 
        self.scale = 1.0
        self.is_placeholder = False

    def load_texture(self):
        try:
            self.texture = pygame.image.load(self.path).convert_alpha()
            self.scaled_texture = self.texture
            self.is_placeholder = False
            log.debug(f"Textura carregada: '{self.path}' {self.texture.get_size()}")
        except (pygame.error, FileNotFoundError) as e:
            log.warning(f"Falha ao carregar textura '{self.path}': {e}. Usando placeholder.")
            self.texture = _make_placeholder(self.name)
            self.scaled_texture = self.texture
            self.is_placeholder = True

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