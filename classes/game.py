import pygame
import sys
from .button import Button
from .config import FONT, WIDTH, HEIGHT, WHITE, BLACK

SCREEN = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Gênio Quiz Troll")

class Game:
    def __init__(self):
        self.running = True
        self.state = "menu"
        self.start_button = Button("Começar", 300, 400, 200, 60, self.start_game)

    def start_game(self):
        print("Jogo começou!")
        self.state = "jogando"

    def run(self):
        while self.running:
            SCREEN.fill(WHITE)

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.running = False
                if self.state == "menu" and event.type == pygame.MOUSEBUTTONDOWN:
                    self.start_button.check_click(event.pos)

            if self.state == "menu":
                self.draw_menu()
            elif self.state == "jogando":
                self.draw_game()

            pygame.display.flip()

        pygame.quit()
        sys.exit()

    def draw_menu(self):
        # Título principal
        title = FONT.render("Gênio Quiz Troll", True, BLACK)
        rect = title.get_rect(center=(WIDTH // 2, 150))
        SCREEN.blit(title, rect)

        # Botão de começar
        self.start_button.draw(SCREEN)

        # Texto no rodapé (créditos)
        autor_title = FONT.render("Todos os direitos reservados © Pensa Rápido 2025", True, BLACK)
        autor_rect = autor_title.get_rect(center=(WIDTH // 2, HEIGHT - 30))  # 30px a partir do fundo
        SCREEN.blit(autor_title, autor_rect)


    def draw_game(self):
        text = FONT.render("Aqui começa o jogo!", True, BLACK)
        SCREEN.blit(text, (250, 280))
