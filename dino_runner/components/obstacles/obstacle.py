import pygame

class Obstaculo(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = pygame.Surface((30, 30))  
        self.image.fill((255, 255, 255))  
        self.rect = self.image.get_rect()
        self.rect.x = 800  
        self.rect.y = 400  
        self.velocidade = -5  #

    def update(self):
        self.rect.x += self.velocidade

        # o obstáculo saiu da tela
        if self.rect.right < 0:
            self.kill()  # Remove o obstáculo da lista de sprites

#  criação de um grupo de obstáculos
grupo_obstaculos = pygame.sprite.Group()
