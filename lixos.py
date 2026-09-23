import pygame
from random import randint

clock = pygame.time.Clock()
pygame.mixer.init()

LIXOVELOCIDADE = 10

class LixoL(pygame.sprite.Sprite):
    def __init__(self, *groups):
        super().__init__(*groups)
        self.images = [pygame.image.load('Imagens/jogo/L1.png'),
                    pygame.image.load('Imagens/jogo/L2.png'),
                    pygame.image.load('Imagens/jogo/L3.png'),
                    pygame.image.load('Imagens/jogo/L4.png'),
                    pygame.image.load('Imagens/jogo/L5.png')]

        self.current_image = randint(0, 4)
        self.rect = pygame.Rect(130, randint(-150, 0), 40, 20)

    def update(self, *args):
        self.image = self.images[self.current_image]
        self.rect.y += LIXOVELOCIDADE
        if self.rect.bottom > 750:
            self.kill()


class LixoR(pygame.sprite.Sprite):
    def __init__(self, *groups):
        super().__init__(*groups)
        self.images = [pygame.image.load('Imagens/jogo/L1.png'),
                    pygame.image.load('Imagens/jogo/L2.png'),
                    pygame.image.load('Imagens/jogo/L3.png'),
                    pygame.image.load('Imagens/jogo/L4.png'),
                    pygame.image.load('Imagens/jogo/L5.png')]

        self.current_image = randint(0, 4)
        self.rect = pygame.Rect(810, randint(-150, 0), 50, 20)

    def update(self, *args):
        self.image = self.images[self.current_image]
        self.rect.y += LIXOVELOCIDADE
        if self.rect.bottom > 750:
            self.kill()

class tiro(pygame.sprite.Sprite):
    def __init__(self, *groups, speed=28, charge=0.0):
        super().__init__(*groups)
        self.images = [pygame.image.load('Imagens/jogo/L1.png'),
                    pygame.image.load('Imagens/jogo/L2.png'),
                    pygame.image.load('Imagens/jogo/L3.png'),
                    pygame.image.load('Imagens/jogo/L4.png'),
                    pygame.image.load('Imagens/jogo/L5.png')]

        self.current_image = randint(0, 4)
        self.rect = pygame.Rect(0, 10, 50, 50)
        self.speed = speed
        self.charge = charge
        
    def update(self, *args):
        self.image = self.images[self.current_image]
        self.rect.y -= self.speed
        if self.rect.bottom < -10:
            self.kill()
