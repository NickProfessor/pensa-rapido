import pygame


pygame.init()

janela = pygame.display.set_mode((600, 400))

clock = pygame.time.Clock()
rodando = True

while rodando:
    tempo = clock.tick(60)

    for evento in pygame.event.get():
        if evento.type == pygame.QUIT:
            rodando = False

pygame.quit()