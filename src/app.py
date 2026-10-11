import pygame
from pygame.locals import *
from logger import log

class App: 
    def __init__(self, width=800, height=600):
        self.width = width
        self.height = height
        
        pygame.init()
        
        pygame.display.set_mode((self.width, self.height))
        pygame.display.set_caption("Lukituber")
        log.info("LukiTuber Inicializado")
    
    def handle_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                log.info("Programa encerrado")
                return False
        
        return True
    
    def render_frame(self):
        pygame.display.flip()
    
    def run(self):
        clock = pygame.time.Clock()
        running = True
        
        while running:
            running = self.handle_events()
            self.render_frame()
            clock.tick(60)
        
        pygame.quit()
