import pygame
from random import randint

LIXOVELOCIDADE = 10

class buracos(pygame.sprite.Sprite):
    def __init__(self, *groups):
        super().__init__(*groups)
        self.images = [pygame.image.load('Imagens/jogo/buraco1.png'),
                    pygame.image.load('Imagens/jogo/buraco2.png')]

        self.current_image = randint(0, 1)
        self.image = self.images[self.current_image]
        self.rect = self.image.get_rect(topleft=(randint(185, 750), randint(-299, 0)))

    def update(self, *args):
        self.image = self.images[self.current_image]
        self.rect.y += LIXOVELOCIDADE
        if self.rect.bottom > 750:
            self.kill()
