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
    def __init__(self, enunciado, alternativas, indice_correta, tempo_limite, numero):
        self.enunciado = enunciado
        self.alternativas = alternativas
        self.indice_correta = indice_correta
        self.tempo_limite = tempo_limite
        self.inicio_tempo = None
        self.resposta_dada = None
        self.resultado_cor = None
        self.numero = numero

    def iniciar_tempo(self):
        self.inicio_tempo = pygame.time.get_ticks()

    def tempo_restante(self):
        if self.inicio_tempo is None:
            return self.tempo_limite
        decorrido = (pygame.time.get_ticks() - self.inicio_tempo) // 1000
        restante = max(0, self.tempo_limite - decorrido)
        return restante

    def tempo_expirou(self):
        return self.tempo_restante() <= 0


    def desenhar(self, tela):
        numero_texto = f"{self.numero + 1}"
        numero_render = FONT.render(numero_texto, True, (0, 0, 0))
        tela.blit(numero_render, (30, 30))


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
            pygame.draw.rect(tela, (181, 101, 29), rect)        
            pygame.draw.rect(tela, (101, 67, 33), rect, width=3)   # borda azul

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

        # Tempo restante
        if self.inicio_tempo is not None:
            tempo_texto = f"00:{self.tempo_restante()}"
            tempo_render = FONT.render(tempo_texto, True, (0, 0, 0))

            # Define a área do retângulo (baseado no texto)
            padding_x, padding_y = 20, 10
            tempo_rect = tempo_render.get_rect()
            box_width = tempo_rect.width + 2 * padding_x
            box_height = tempo_rect.height + 2 * padding_y

            # Posiciona no meio vertical e na lateral direita
            box_x = WIDTH - box_width - 30
            box_y = 60
            caixa_rect = pygame.Rect(box_x, box_y, box_width, box_height)

            # Desenha o fundo cinza
            pygame.draw.rect(tela, (200, 200, 200), caixa_rect)

            # Desenha a borda azul
            pygame.draw.rect(tela, (0, 0, 255), caixa_rect, 3)

            # Renderiza o texto no centro do retângulo
            tempo_texto_pos = tempo_render.get_rect(center=caixa_rect.center)
            tela.blit(tempo_render, tempo_texto_pos)



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
