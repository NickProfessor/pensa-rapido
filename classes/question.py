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

RODAPE_Y = HEIGHT - 30  # posição do rodapé

def quebrar_texto_em_linhas(texto, fonte, largura_max):
    palavras = texto.split()
    linhas = []
    linha_atual = ""
    for palavra in palavras:
        teste = linha_atual + (" " if linha_atual else "") + palavra
        largura, _ = fonte.size(teste)
        if largura <= largura_max:
            linha_atual = teste
        else:
            if linha_atual:
                linhas.append(linha_atual)
            linha_atual = palavra
    if linha_atual:
        linhas.append(linha_atual)
    return linhas


class Question:
    def __init__(self, enunciado, alternativas, indice_correta, tempo_limite, numero, resposta_troll=None):
        self.enunciado = enunciado
        self.alternativas = alternativas
        self.indice_correta = indice_correta
        self.tempo_limite = tempo_limite
        self.inicio_tempo = None
        self.resposta_dada = None
        self.resultado_cor = None
        self.numero = numero
        self.resposta_troll = resposta_troll

    def iniciar_tempo(self):
        self.inicio_tempo = pygame.time.get_ticks()

    def tempo_restante(self):
        if self.inicio_tempo is None:
            return self.tempo_limite
        decorrido = (pygame.time.get_ticks() - self.inicio_tempo) // 1000
        return max(0, self.tempo_limite - decorrido)

    def tempo_expirou(self):
        return self.tempo_restante() <= 0

    def desenhar(self, tela):
        numero_texto = f"{self.numero + 1}"
        numero_render = FONT.render(numero_texto, True, BLACK)
        tela.blit(numero_render, (30, 30))

        # Quebra do enunciado
        largura_max = WIDTH * 0.8
        linhas = quebrar_texto_em_linhas(self.enunciado, FONT, largura_max)
        self.palavras_pos = []
        y = ENUNCIADO_POS[1]
        espaço_entre_linhas = 5

        for linha in linhas:
            palavras = linha.split()
            largura_total = sum(FONT.size(p)[0] + FONT.size(" ")[0] for p in palavras) - FONT.size(" ")[0]
            x = ENUNCIADO_POS[0] - largura_total // 2
            for palavra in palavras:
                render = FONT.render(palavra, True, BLACK)
                rect = render.get_rect(topleft=(x, y))
                tela.blit(render, rect)
                self.palavras_pos.append((palavra, rect))
                x += render.get_width() + FONT.size(" ")[0]
            y += FONT.get_height() + espaço_entre_linhas

        # Alternativas
        for i, alt in enumerate(self.alternativas):
            col = i % 2
            row = i // 2
            x = START_X + col * (ALT_WIDTH + ALT_SPACING_X)
            y_alt = START_Y + row * (ALT_HEIGHT + ALT_SPACING_Y)
            rect = pygame.Rect(x, y_alt, ALT_WIDTH, ALT_HEIGHT)
            pygame.draw.rect(tela, (200, 200, 200), rect)
            pygame.draw.rect(tela, (0, 0, 255), rect, 3)

            cor_texto = self.get_cor_alternativa(i)
            texto = f"{chr(65 + i)}) {alt}"
            alt_render = FONT.render(texto, True, cor_texto)
            text_rect = alt_render.get_rect(center=rect.center)
            tela.blit(alt_render, text_rect)

        # Tempo
        if self.inicio_tempo is not None:
            tempo_texto = f"00:{self.tempo_restante()}"
            tempo_render = FONT.render(tempo_texto, True, BLACK)
            padding_x, padding_y = 20, 10
            tempo_rect = tempo_render.get_rect()
            box_width = tempo_rect.width + 2 * padding_x
            box_height = tempo_rect.height + 2 * padding_y
            box_x = WIDTH - box_width - 30
            box_y = HEIGHT - 120
            caixa_rect = pygame.Rect(box_x, box_y, box_width, box_height)
            pygame.draw.rect(tela, (200, 200, 200), caixa_rect)
            pygame.draw.rect(tela, (0, 0, 255), caixa_rect, 3)
            tempo_texto_pos = tempo_render.get_rect(center=caixa_rect.center)
            tela.blit(tempo_render, tempo_texto_pos)

        self.rodape_chars_pos = []
        rodape_texto = "Todos os direitos reservados © Pensa Rápido 2025"
        largura_total = sum(FONT.size(c)[0] for c in rodape_texto)
        x = WIDTH // 2 - largura_total // 2
        y = RODAPE_Y - FONT.get_height() // 2

        for caractere in rodape_texto:
            render = FONT.render(caractere, True, BLACK)
            rect = render.get_rect(topleft=(x, y))
            tela.blit(render, rect)
            self.rodape_chars_pos.append((caractere, rect))
            x += render.get_width()



    def get_cor_alternativa(self, i):
        if self.resposta_dada is None:
            return BLACK
        elif self.resposta_dada == i:
            return GREEN if i == self.indice_correta else RED
        else:
            return BLACK

    def checar_resposta(self, pos):
        pos_x, pos_y = pos
        # Checar alternativas
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

        # Checar locais "troll"
        if self.resposta_troll:
            if isinstance(self.resposta_troll, dict) and self.resposta_troll.get("local") == "enunciado":
                alvo = self.resposta_troll.get("palavra", "").strip(',.!?').lower()
                for w, rect in self.palavras_pos:
                    if w.strip(',.!?').lower() == alvo and rect.collidepoint(pos_x, pos_y):
                        self.resposta_dada = -1
                        self.resultado_cor = GREEN
                        return True
            elif self.resposta_troll == "numero":
                rect = FONT.render(str(self.numero + 1), True, BLACK).get_rect(topleft=(30, 30))
                if rect.collidepoint(pos_x, pos_y):
                    self.resposta_dada = -1
                    self.resultado_cor = GREEN
                    return True
            elif isinstance(self.resposta_troll, dict) and self.resposta_troll.get("local") == "rodape":
                alvo = self.resposta_troll.get("palavra", "")
                for c, rect in getattr(self, "rodape_chars_pos", []):
                    if c == alvo and rect.collidepoint(pos_x, pos_y):
                        self.resposta_dada = -1
                        self.resultado_cor = GREEN
                        return True


            elif self.resposta_troll == "tempo":
                tempo_texto = f"00:{self.tempo_restante()}"
                tempo_render = FONT.render(tempo_texto, True, BLACK)
                padding_x, padding_y = 20, 10
                tempo_rect = tempo_render.get_rect()
                box_width = tempo_rect.width + 2 * padding_x
                box_height = tempo_rect.height + 2 * padding_y
                box_x = WIDTH - box_width - 30
                box_y = HEIGHT - 120
                tempo_area = pygame.Rect(box_x, box_y, box_width, box_height)
                if tempo_area.collidepoint(pos_x, pos_y):
                    self.resposta_dada = -1
                    self.resultado_cor = GREEN
                    return True


        return False

    def foi_respondida(self):
        return self.resposta_dada is not None

    def resposta_correta(self):
        if self.indice_correta == -1:
            return self.resposta_dada == -1
        return self.resposta_dada == self.indice_correta
