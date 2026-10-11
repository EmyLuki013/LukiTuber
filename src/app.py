import pygame
from pygame.locals import *

from logger import log
from avatars_manager import AvatarsManager
from settings import global_settings
from renderer import Renderer

class App: 
    def __init__(self, width=800, height=600):
        self.width = width
        self.height = height
        self.avatars_manager = AvatarsManager()
        self.settings = global_settings
        self.renderer = Renderer()
        
        pygame.init()
        
        pygame.display.set_mode((self.width, self.height))
        pygame.display.set_caption("LukiTuber")
        log.info("LukiTuber Inicializado")

        self.settings.load_settings()
        self.avatars_manager.load_avatars()

        selected_avatar = self.avatars_manager.get_avatar(self.settings.selected_avatar)
        if selected_avatar:
            selected_avatar.layers_manager.load_layers()
            log.info(f"Layers do avatar '{selected_avatar.name}' carregados")
            self.renderer.set_avatar(selected_avatar)
        else:
            log.error("Não foi possivel carregar o avatar selecionado")

        self.screen = pygame.display.get_surface()
        
    def handle_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                log.info("Programa encerrado")
                return False
        
        return True
    
    def render_frame(self):
        self.renderer.render(self.screen)
        pygame.display.flip()
    
    def run(self):
        clock = pygame.time.Clock()
        running = True
        
        while running:
            running = self.handle_events()
            self.render_frame()
            clock.tick(60)
        
        pygame.quit()
