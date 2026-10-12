import sys
import os
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
            selected_avatar.bootstrap_states()
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

            if event.type == pygame.KEYDOWN:
                mods = pygame.key.get_mods()
                ctrl = mods & pygame.KMOD_CTRL

                if ctrl and event.key == pygame.K_r:
                    log.info("Reiniciando LukiTuber...")
                    self._save_state()
                    pygame.quit()
                    os.execv(sys.executable, [sys.executable] + sys.argv)

                elif event.key in (pygame.K_EQUALS, pygame.K_PLUS, pygame.K_KP_PLUS):
                    self.renderer.zoom_in()
                elif event.key in (pygame.K_MINUS, pygame.K_KP_MINUS):
                    self.renderer.zoom_out()
                elif event.key == pygame.K_0:
                    self.renderer.reset_zoom()
                
            if event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:
                    self.renderer.start_drag(event.pos)

            elif event.type == pygame.MOUSEBUTTONUP:
                if event.button == 1:
                    self.renderer.end_drag()

            elif event.type == pygame.MOUSEMOTION:
                if self.renderer.is_dragging:
                    if event.buttons[0]:
                        self.renderer.update_drag(event.pos)
                    else:
                        self.renderer.end_drag()

            elif event.type == pygame.MOUSEWHEEL:
                mods = pygame.key.get_mods()
                if mods & pygame.KMOD_CTRL:
                    if event.y > 0:
                        self.renderer.zoom_in()
                    elif event.y < 0:
                        self.renderer.zoom_out()

        return True

    def _save_state(self):
        try:
            self.avatars_manager.save_avatars()
            log.info("Estado dos avatares salvo")
        except Exception as e:
            log.exception(f"Falha ao salvar avatares: {e}")

    def render_frame(self):
        self.screen.fill((0, 255, 0))
        self.renderer.render(self.screen)
        pygame.display.flip()

    def run(self):
        clock = pygame.time.Clock()
        running = True

        while running:
            running = self.handle_events()
            self.render_frame()
            clock.tick(60)

        self._save_state()
        pygame.quit()