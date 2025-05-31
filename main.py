import pygame
import pygame_gui

pygame.init()

janela = pygame.display.set_mode((600, 400))
pygame.display.set_caption("Pensa-Rápido")

gerenciador = pygame_gui.UIManager((600, 400))

botao_start = pygame_gui.elements.UIButton(
    relative_rect=pygame.Rect((200, 150), (200, 50)),
    text='Start - Pensa-Rápido',
    manager=gerenciador
)


titulo = pygame_gui.elements.UILabel(
    relative_rect=pygame.Rect((150, 50), (300, 50)),
    text='PENSA-RÁPIDO',
    manager=gerenciador
)

clock = pygame.time.Clock()
rodando = True

while rodando:
    tempo = clock.tick(60)

    for evento in pygame.event.get():
        if evento.type == pygame.QUIT:
            rodando = False

        if evento.type == pygame_gui.UI_BUTTON_PRESSED:
            if evento.ui_element == botao_start:
                print("Jogo iniciado! Prepare-se para o desafio do Pensa-Rápido!")

        gerenciador.process_events(evento)

    gerenciador.update(tempo)

    janela.fill((0, 0, 30)) 

    gerenciador.draw_ui(janela)
    pygame.display.update()

pygame.quit()