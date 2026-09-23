import os
from pathlib import Path

os.chdir(Path(__file__).resolve().parent)

import pygame

from catador import Carro
from player import Player

os.environ['SDL_VIDEO_CENTERED'] = '1'
pygame.init()

fps = 60

clock = pygame.time.Clock()

# Resolução

WIDTH = 980
HEIGHT = 720

# objetos

objectGroup = pygame.sprite.Group()
player = Player(objectGroup)
catador = Carro(objectGroup)

# Janela

screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Trash Cleaner")

# Fundo
bg = pygame.image.load('Imagens/jogo/fundosemobjetos.png').convert()
bg = pygame.transform.scale(bg, (WIDTH, HEIGHT))
bg_y = 0

# Sounds
andar = pygame.mixer.Sound('Sons/passos.wav')

# Música

pygame.mixer_music.load("Sons/music.wav")
pygame.mixer.music.play(-1)

enemies_spd = 0

janela_aberta = True
while janela_aberta:
    clock.tick(fps)

    # Faz o Fundo continuar infinito
    bg_y1 = bg_y % bg.get_height()
    bg_y += 5
    screen.blit(bg, (0, bg_y1 - bg.get_height()))
    if bg_y1 < HEIGHT:
        screen.blit(bg, (0, bg_y1))
        # Desenha os objetos
        objectGroup.draw(screen)
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            var = janela_aberta = False
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE:
                andar.play()


# Update
objectGroup.update()
pygame.display.update()
screen.fill((0, 0, 0))

pygame.quit()
