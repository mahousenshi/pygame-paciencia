'''
Grupo

Fabio Luis Ortolan
Fabrizzio Caron Michelazzo
Pedro Vitor Marques de Castro
'''
from game import Game
from random import randint

import pygame
import sys


# Inicialização do Pygame
pygame.init()

SCREEN_WIDTH = 1200
SCREEN_HEIGHT = 800

window = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption('Paciencia')

clock = pygame.time.Clock()

# Fundo de tela.
background = pygame.image.load('imgs/background.jpg')
fatec_logo = pygame.image.load('imgs/fatec_logo.png')

color = (randint(0, 255), randint(0, 255), randint(0, 255))

# Inicialização das variaves do jogo.
game = Game()

# Loop
while True:
    # Eventos.
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

        if event.type == pygame.KEYUP:
            if event.key == pygame.K_F2:
                game.reset(pygame.time.get_ticks())

        if event.type == pygame.MOUSEBUTTONDOWN:
            game.mousedown(event, pygame.time.get_ticks())

        if event.type == pygame.MOUSEMOTION:
            game.mousemotion(event)

        if event.type == pygame.MOUSEBUTTONUP:
            game.mouseup(event)

    # Desenha a tela.
    window.blit(background, [0, 0])
    window.blit(fatec_logo, [128, 201])
    game.draw(window)

    # Tela final
    if sum(len(p) for p in game.foundations) == 52:
        winner = pygame.Rect(0, 0, SCREEN_WIDTH, SCREEN_HEIGHT)
        
        # Muda a cor do fundo e do texto de maneira lenta.
        if pygame.time.get_ticks() - game.last_click > 600:
            game.last_click = pygame.time.get_ticks()
            color = (randint(0, 255), randint(0, 255), randint(0, 255))

        end_background = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT))
        end_background.set_alpha(64)
        end_background.fill(color)
        window.blit(end_background, (0, 0))

        end_white_bg = pygame.Surface((SCREEN_WIDTH, 300))
        end_white_bg.fill((255, 255, 255))
        window.blit(end_white_bg, (0, 250))

        ganhou = pygame.font.Font(None, 250)
        ganhou = ganhou.render("Ganhou!!!", True, color)
        window.blit(ganhou, (195, 325))

        recomeca = pygame.font.Font(None, 50)
        recomeca = recomeca.render("F2 recomeça!", True, color)
        window.blit(recomeca, (490, 490))

    # Finaliza o loop.
    pygame.display.flip()
    clock.tick(60)
