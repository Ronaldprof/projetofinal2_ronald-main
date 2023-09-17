import pygame
import random
from dino_runner.components.obstacles.cactus import Cactus
from dino_runner.components.obstacles.bird import Bird
from dino_runner.utils.constants import DEATH_SOUND # importei o death-sound

class ObstacleManager:
    def __init__(self):
        self.obstacles = []
        self.death_sound = DEATH_SOUND # declarei
        self.death_sound.set_volume(0.5) # coloquei o volume


    def update(self,game):
        obstacle_type = [
            Cactus(),
            Bird(),

        ]

        if len(self.obstacles) == 0:
            self.obstacles.append(obstacle_type[random.randint(0,1)])
        for obstacle in self.obstacles:
            obstacle.update(game.game_speed, self.obstacles)
            if game.player.dino_rect.colliderect(obstacle.rect):
                if not game.player.has_power_up:
                    self.death_sound.play() # toda vez q ele morrer fazer a zuada
                    pygame.time.delay(500)
                    game.playing = False
                    game.death_count += 1 
                    break
                else:
                    self.obstacles.remove(obstacle)
    
    def reset_obstacles(self):
        self.obstacles = []

    def draw(self,screen):
        for obstacle in self.obstacles:
            obstacle.draw(screen)