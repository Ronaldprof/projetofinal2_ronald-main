import pygame
import os
from pygame.sprite import Sprite
from dino_runner.utils.constants import RUNNING, JUMPING, DUCKING, DEFAULT_TYPE, DUCKING_HAMMER, JUMPING_HAMMER, HAMMER_TYPE, RUNNING_HAMMER, SHIELD_TYPE, DUCKING_SHIELD, JUMPING_SHIELD, RUNNING_SHIELD, JUMP_SOUND
# Constantes algo que nunca muda
DUCK_IMG = {DEFAULT_TYPE: DUCKING, SHIELD_TYPE: DUCKING_SHIELD, HAMMER_TYPE: DUCKING_HAMMER} # cada um em um estado especifico 
JUMP_IMG = {DEFAULT_TYPE: JUMPING, SHIELD_TYPE: JUMPING_SHIELD, HAMMER_TYPE: JUMPING_HAMMER}
RUN_IMG = {DEFAULT_TYPE: RUNNING, SHIELD_TYPE: RUNNING_SHIELD, HAMMER_TYPE: RUNNING_HAMMER}

X_POS = 80
Y_POS = 310
Y_POS_DUCK = 340
JUMP_VEL = 8.5  # Velocidade inicial do salto do dinossauro.

class Dinosaur(Sprite): # sprite images que se movimenta
    def __init__(self):
        super().__init__() # chamar class ma
        self.type = DEFAULT_TYPE
        self.image = RUN_IMG[self.type][0]
        self.dino_rect = self.image.get_rect()
        self.dino_rect.x = X_POS
        self.dino_rect.y = Y_POS
        self.step_index = 0
        self.dino_run = True
        self.dino_jump = False
        self.dino_duck = False
        self.jump_vel = JUMP_VEL
        self.setup_state()
        self.jump_sound = JUMP_SOUND
        self.jump_sound_is_playing = False  # o som de pulo esta tocando?

    def setup_state(self): #  variáveis de estado  com o power up
        self.has_power_up = False
        self.shield = False
        self.show_text = False
        self.shield_time_up = 0

    def update(self, user_input):
        if self.dino_run:
            self.run()

        if self.dino_jump:
            self.jump()
        
        if self.dino_duck:
            self.duck()

        if user_input[pygame.K_UP] and not self.dino_jump:
            self.dino_run = False
            self.dino_jump = True
            self.dino_duck = False

        elif user_input[pygame.K_DOWN] and not self.dino_jump:
            self.dino_run = False
            self.dino_jump = False
            self.dino_duck = True

        elif not self.dino_jump and not self.dino_duck:
            self.dino_run = True
            self.dino_jump = False
            self.dino_duck = False

        if self.step_index >= 10:
            self.step_index = 0

    def run(self): # correndo
        self.image = RUN_IMG[self.type][self.step_index // 5]
        self.dino_rect.x = X_POS
        self.dino_rect.y = Y_POS
        self.step_index += 1

    def jump(self):  # pulando
        self.image = JUMP_IMG[self.type]
        if self.dino_jump: 
            self.dino_rect.y -= self.jump_vel * 4
            self.jump_vel -= 0.8
            if not self.jump_sound_is_playing:
                self.jump_sound.play() # quando ele ta no ar e true,e nao vai tocar varias vezes
                self.jump_sound_is_playing = True
        if self.jump_vel < -JUMP_VEL:
            self.dino_rect.y = Y_POS
            self.dino_jump = False
            self.jump_vel = JUMP_VEL
            self.jump_sound_is_playing = False #quando ele ta no chao e ele ta false
        
          
    def duck(self): # atualizar a image de acordo com estado atual
        self.image = DUCK_IMG[self.type][self.step_index // 5]
        self.dino_rect = self.image.get_rect()
        self.dino_rect.x = X_POS
        self.dino_rect.y = Y_POS_DUCK
        self.step_index += 1
        self.dino_duck = False
        
    def draw(self, screen): #  desenhar a imagem do dinossauro na tela.
        screen.blit(self.image, (self.dino_rect.x, self.dino_rect.y))
        
    
