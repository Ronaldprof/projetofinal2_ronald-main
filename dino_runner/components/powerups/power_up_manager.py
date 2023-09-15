import random
import pygame
from dino_runner.components.powerups.shield import Shield

class PowerUpManeger():
    def __init__(self):
        self.powe_ups = []
        self.when_appers = 0

    def generate_power_up(self, score): # se o meu pode for = 0 
        if len(self.power_ups) == 0 and self.when_appars == score:
             self.when_appars += random.randint(200, 300) # a cada a 200 e 300 pontos o shild aparece
             self.power_ups.append(Shield())

    def update(self,score, game_speed, player):
        self.generate_power_up(score)
        for power_up in self.power_ups:
         power_up.update(game_speed, self.power_ups)
         if player.dino_rect.colliderect(power_up.rect): # se ele colidir com alguma coisa ele morre
             power_up.start_time = pygame.time.get_ticks()
             player.shield = True # poder
             player.has_power_up = True
             player.type = power_up.type  
             player.power_up_tining = power_up.start_time + (power_up.duratin * 1000)
             self.power_ups.remove(power_up)# passou de 10 seg removeu
             # atulizar no jogo ex pontuaçao velocidade s
             # se o jogador ta true ou false
    def draw(self, screen):
        for power_up in self.power_ups:
            power_up.draw(screen)

    def reset_power_up(self):
        self.power_up = []
        self.when_appers = random.randint(200, 300) #resetar o power up para voltar aleatorio