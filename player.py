import pygame

WIDTH = 980
HEIGHT = 720

class Player(pygame.sprite.Sprite):
    def __init__(self, *groups):
        super().__init__(*groups)
        self.images = [pygame.image.load('Imagens/sprite/s1.png'),
                        pygame.image.load('Imagens/sprite/s2.png'),
                        pygame.image.load('Imagens/sprite/s3.png'),
                        pygame.image.load('Imagens/sprite/s4.png'),
                        pygame.image.load('Imagens/sprite/s5.png'),
                        pygame.image.load('Imagens/sprite/s6.png'),
                        pygame.image.load('Imagens/sprite/s7.png'),
                        pygame.image.load('Imagens/sprite/s8.png'),]

        self.current_image = 0
        self.rect = pygame.Rect(460, 570, 50, 50)
    
    def update(self):
        
        comandos = pygame.key.get_pressed()
        self.current_image = (self.current_image + 1) % 8
        self.image = self.images[self.current_image]
    
        
        if comandos[pygame.K_w] or comandos[pygame.K_UP]:
            self.rect.y -= 13
        if comandos[pygame.K_s] or comandos[pygame.K_DOWN]:
            self.rect.y += 13
        if comandos[pygame.K_d] or comandos[pygame.K_RIGHT]:
            self.rect.x += 13
        if comandos[pygame.K_a] or comandos[pygame.K_LEFT]:
            self.rect.x -= 13

        # Limitando area do personagem andar
        if self.rect.top < 200:
            self.rect.top = 200
        if self.rect.bottom > HEIGHT + 20:
            self.rect.bottom = HEIGHT + 20
        if self.rect.left < 125:
            self.rect.left = 125
        if self.rect.right > 860:
            self.rect.right = 860


class Lançar(pygame.sprite.Sprite):
    def __init__(self, *groups):
        super().__init__(*groups)
        self.images = [pygame.image.load('Imagens/sprite/l1.png'),
                       pygame.image.load('Imagens/sprite/l2.png'),
                       pygame.image.load('Imagens/sprite/l3.png'),
                       pygame.image.load('Imagens/sprite/l4.png'),]

        self.current_image = 0
        self.image = pygame.image.load('Imagens/jogo/boneco1.png')
        self.image = pygame.transform.scale(self.image, [69, 146])
        self.rect = pygame.Rect(460, 570, 100, 100)

    def update(self, *args):
        comandos = pygame.key.get_pressed()
        self.current_image = (self.current_image + 1) % 4
        self.image = self.images[self.current_image]

        if comandos[pygame.K_w] or comandos[pygame.K_UP]:
            self.rect.y -= 13
        if comandos[pygame.K_s] or comandos[pygame.K_DOWN]:
            self.rect.y += 13
        if comandos[pygame.K_d] or comandos[pygame.K_RIGHT]:
            self.rect.x += 13
        if comandos[pygame.K_a] or comandos[pygame.K_LEFT]:
            self.rect.x -= 13

        # Limitando area do personagem andar
        if self.rect.top < 200:
            self.rect.top = 200
        if self.rect.bottom > HEIGHT + 20:
            self.rect.bottom = HEIGHT + 20
        if self.rect.left < 125:
            self.rect.left = 125
        if self.rect.right > 905:
            self.rect.right = 905
