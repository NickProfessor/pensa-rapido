import pygame
from .config import FONT, WIDTH, HEIGHT, BLACK, GREEN, RED

# Layout
ENUNCIADO_POS = (WIDTH // 2, 40)
ALT_WIDTH = 300
ALT_HEIGHT = 80
ALT_SPACING_X = 40
ALT_SPACING_Y = 30

GRID_WIDTH = 2 * ALT_WIDTH + ALT_SPACING_X
GRID_HEIGHT = 2 * ALT_HEIGHT + ALT_SPACING_Y
START_X = (WIDTH - GRID_WIDTH) // 2
START_Y = (HEIGHT - GRID_HEIGHT) // 2 + 40

RESULTADO_POS = (WIDTH // 2, HEIGHT - 50)


class Question:
    def __init__(self, enunciado, alternativas, indice_correta):
        self.enunciado = enunciado
        self.alternativas = alternativas
        self.indice_correta = indice_correta
        self.resposta_dada = None
        self.resultado_cor = None

    def desenhar(self, tela):
        # Enunciado
        enunciado_text = FONT.render(self.enunciado, True, BLACK)
        en_rect = enunciado_text.get_rect(center=ENUNCIADO_POS)
        tela.blit(enunciado_text, en_rect)

        # Alternativas 2x2 centralizadas
        for i, alt in enumerate(self.alternativas):
            col = i % 2
            row = i // 2
            x = START_X + col * (ALT_WIDTH + ALT_SPACING_X)
            y = START_Y + row * (ALT_HEIGHT + ALT_SPACING_Y)

            rect = pygame.Rect(x, y, ALT_WIDTH, ALT_HEIGHT)
            pygame.draw.rect(tela, (200, 200, 200), rect)        # fundo cinza
            pygame.draw.rect(tela, (0, 0, 255), rect, width=3)   # borda azul

            # Texto centralizado
            cor_texto = self.get_cor_alternativa(i)
            texto = f"{chr(65 + i)}) {alt}"
            alt_text = FONT.render(texto, True, cor_texto)
            text_rect = alt_text.get_rect(center=rect.center)
            tela.blit(alt_text, text_rect)

        # Mensagem de resultado (acerto/erro)
        if self.resposta_dada is not None:
            msg = "Resposta correta!" if self.resultado_cor == GREEN else "Resposta incorreta!"
            resultado_text = FONT.render(msg, True, self.resultado_cor)
            resultado_rect = resultado_text.get_rect(center=RESULTADO_POS)
            tela.blit(resultado_text, resultado_rect)

    def get_cor_alternativa(self, i):
        if self.resposta_dada is None:
            return BLACK
        elif i == self.indice_correta:
            return GREEN
        elif i == self.resposta_dada:
            return RED
        return BLACK

    def checar_resposta(self, pos):
        pos_x, pos_y = pos
        for i in range(len(self.alternativas)):
            col = i % 2
            row = i // 2
            x = START_X + col * (ALT_WIDTH + ALT_SPACING_X)
            y = START_Y + row * (ALT_HEIGHT + ALT_SPACING_Y)

            rect = pygame.Rect(x, y, ALT_WIDTH, ALT_HEIGHT)
            if rect.collidepoint(pos_x, pos_y):
                self.resposta_dada = i
                self.resultado_cor = GREEN if i == self.indice_correta else RED
                return True
        return False

    def foi_respondida(self):
        return self.resposta_dada is not None

    def resposta_correta(self):
        return self.resposta_dada == self.indice_correta
