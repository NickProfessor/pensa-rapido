import pygame
import sys
import json
from .button import Button
from .config import FONT, WIDTH, HEIGHT, WHITE, BLACK, FONT_TITULO
from .question import Question

SCREEN = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Pensa Rápido")

def carregar_questoes(caminho_json):
    with open(caminho_json, 'r', encoding='utf-8') as f:
        dados = json.load(f)

    perguntas = []
    for i, q in enumerate(dados):
        perguntas.append(Question(
            enunciado=q["enunciado"],
            alternativas=q["alternativas"],
            indice_correta=q.get("correta", -1),  # padrão -1 se não houver correta
            tempo_limite=q.get("tempo", 10),
            numero=i,
            resposta_troll=q.get("resposta_troll")  # pode ser None
        ))
    return perguntas




class Game:
    def __init__(self):
        self.running = True
        self.state = "menu"
        self.start_button = Button("Começar", 300, 400, 200, 60, self.start_game)
        self.retry_button = Button("Recomeçar", WIDTH - 200 - 0.1 * 200, 400, 200, 60, self.back_to_menu)
        self.questions = carregar_questoes("assets/questions.json")
        self.current_question_index = 0



    def start_game(self):
        print("Jogo começou!")
        self.state = "playing"

    def run(self):
        while self.running:
            SCREEN.fill(WHITE)

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.running = False

                if self.state == "menu":
                    if event.type == pygame.MOUSEBUTTONDOWN:
                        self.start_button.check_click(event.pos)

                elif self.state == "game_over":
                    if event.type == pygame.MOUSEBUTTONDOWN:
                        self.retry_button.check_click(event.pos)

                elif self.state == "victory":
                    if event.type == pygame.MOUSEBUTTONDOWN:
                        self.retry_button.check_click(event.pos)

                elif self.state == "playing":
                    current_question = self.questions[self.current_question_index]

                    if event.type == pygame.MOUSEBUTTONDOWN:
                        if not current_question.foi_respondida():
                            if current_question.checar_resposta(event.pos):
                                pygame.time.set_timer(pygame.USEREVENT + 1, 100)

                    if event.type == pygame.USEREVENT + 1:
                        pygame.time.set_timer(pygame.USEREVENT + 1, 0)

                        if not current_question.resposta_correta():
                            self.game_over()
                        else:
                            self.current_question_index += 1
                            if self.current_question_index >= len(self.questions):
                                self.win_game()

            # Fora do loop de eventos!
            if self.state == "menu":
                self.draw_menu()
            elif self.state == "game_over":
                self.draw_game_over()
            elif self.state == "victory":
                self.draw_victory()
            elif self.state == "playing":
                current_question = self.questions[self.current_question_index]

                # Inicia tempo só uma vez
                if current_question.inicio_tempo is None:
                    current_question.iniciar_tempo()

                current_question.desenhar(SCREEN)

                # Checa se o tempo acabou
                if not current_question.foi_respondida() and current_question.tempo_expirou():
                    self.game_over()


            pygame.display.flip()

        pygame.quit()
        sys.exit()


    def draw_menu(self):
        # Título principal
        title = FONT_TITULO.render("Pensa rápido!", True, BLACK)
        rect = title.get_rect(center=(WIDTH // 2, 150))
        SCREEN.blit(title, rect)

        # Botão de começar
        self.start_button.draw(SCREEN)

        # Texto no rodapé (créditos)
        autor_title = FONT.render("Todos os direitos reservados © Pensa Rápido 2025", True, BLACK)
        autor_rect = autor_title.get_rect(center=(WIDTH // 2, HEIGHT - 30))  # 30px a partir do fundo
        SCREEN.blit(autor_title, autor_rect)



    def game_over(self):
        self.state = "game_over"

    def back_to_menu(self):
        self.state = "menu"
        self.current_question_index = 0
        self.questions = carregar_questoes("assets/questions.json")


    def draw_game_over(self):
        game_over_text = FONT.render("You fail!", True, (255, 0, 0))
        text_rect = game_over_text.get_rect(center=(WIDTH // 2, 200))
        SCREEN.blit(game_over_text, text_rect)

        self.retry_button.draw(SCREEN)

    def draw_victory(self):
        victory_text = FONT.render("Parabéns! Você venceu!", True, (0, 180, 0))
        text_rect = victory_text.get_rect(center=(WIDTH // 2, 200))
        SCREEN.blit(victory_text, text_rect)

        self.retry_button.draw(SCREEN)

    def win_game(self):
        self.state = "victory"

