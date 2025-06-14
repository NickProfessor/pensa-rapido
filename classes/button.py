import pygame
from .config import FONT, WHITE, BLUE

class Button:
    def __init__(self, text, x, y, width, height, callback):
        self.rect = pygame.Rect(x, y, width, height)
        self.text = text
        self.callback = callback
        self.color = BLUE

    def draw(self, surface):
        pygame.draw.rect(surface, self.color, self.rect)
        text_surf = FONT.render(self.text, True, WHITE)
        text_rect = text_surf.get_rect(center=self.rect.center)
        surface.blit(text_surf, text_rect)

    def check_click(self, pos):
        if self.rect.collidepoint(pos):
            self.callback()
