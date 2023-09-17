import pygame 
pygame.init()  # iniciar pygame # 
pygame.mixer.init() # iniciar msc
# Precisa ser antes de import pois as variáveis dos sons no arquivo constants precisam do mixer já iniciado. Senão, ocorrerá um erro.
from dino_runner.utils.constants import BG, ICON, SCREEN_HEIGHT, SCREEN_WIDTH, TITLE, FPS, DEFAULT_TYPE, SCORE_SOUND
from dino_runner.components.dinosaur import Dinosaur
from dino_runner.components.obstacles.obstacle_manager import ObstacleManager
from dino_runner.utils.text_utils import draw_message_component
from dino_runner.components.powerups.power_up_manager import PowerUpManager

class Game:
    def __init__(self): # costrutor
        pygame.display.set_caption(TITLE)
        pygame.display.set_icon(ICON)
        self.screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
        self.clock = pygame.time.Clock()
        self.playing = False
        self.running = False
        self.score = 0
        self.record = 0
        self.death_count = 0 
        self.game_speed = 20
        self.x_pos_bg = 0
        self.y_pos_bg = 380
        self.player = Dinosaur()
        self.obstacle_manager = ObstacleManager()
        self.power_up_manager = PowerUpManager()
        self.score_sound = SCORE_SOUND
        self.score_sound.set_volume(0.3) # VOLUME 30 % do volume original
    
    def execute(self):
        self.running = True
        while self.running:
            if not self.playing:
                self.show_menu()
       
        pygame.display.quit()
        pygame.quit()
    
    def run(self):
        self.playing = True
        self.obstacle_manager.reset_obstacles()
        self.power_up_manager.reset_power_up()
        self.game_speed = 20
        self.score = 0

        while self.playing:
            self.events()
            self.update()
            self.draw ()

    def events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.playing = False
                self.ruinning = False
            
    def update(self):
        user_input = pygame.key.get_pressed()
        self.player.update(user_input)
        self.obstacle_manager.update(self)
        self.update_score()
        self.power_up_manager.update(self.score, self.game_speed, self.player)

    def update_score(self):  
        self.score += 1
        if self.score % 100 == 0:
            self.game_speed +=  5
            self.score_sound.play() # para iniciar, o son a cada 100 pontos

    def draw_record(self):
        draw_message_component(
        f"Recorde: {self.record}",
        self.screen,
        pos_x_center=1000,
        pos_y_center=80  # Defina a posição Y desejada para o recorde
    )

    
    def draw(self): # tela do jogo
        self.clock.tick(FPS)  
        self.screen.fill((255, 255, 255))
        self.draw_blackground()
        self.player.draw(self.screen)
        self.obstacle_manager.draw(self.screen)
        self.draw_score()
        self.draw_record() 
        self.draw_power_up_time()
        self.power_up_manager.draw(self.screen)
        pygame.display.update()
        pygame.display.flip()
        
    def draw_blackground(self):
        image_width = BG.get_width()
        self.screen.blit(BG, (self.x_pos_bg, self.y_pos_bg))
        self.screen.blit(BG, (image_width + self.x_pos_bg, self.y_pos_bg))
       
        if self.x_pos_bg <= - image_width:
            self.screen.blit(BG, (image_width + self.x_pos_bg, self.y_pos_bg))
            self.x_pos_bg = 0
            self.x_pos_bg -= self.game_speed

    def draw_score(self):
        draw_message_component(
            f"score:{self.score}",
            self.screen,
            pos_x_center = 1000,
            pos_y_center = 50
        )

    def draw_power_up_time(self): #tempo para mostrar
        if self.player.has_power_up:
            time_to_Show = round((self.player.power_up_timing - pygame.time.get_ticks()) / 1000, 2) # mostra a contagem 
            if time_to_Show >= 0:
                draw_message_component(
                    f"{self.player.type.capitalize()} disponível por  {time_to_Show} segundos",
                    self.screen,
                    font_size = 18,
                    pos_x_center = 500,
                    pos_y_center = 40
                )
            else:
                    self.player.has_power_up = False
                    self.player.type = DEFAULT_TYPE 
    
    def handle_events_on_menu(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.playing = False
                self.running = False
            
            elif event.type == pygame.KEYDOWN:
                self.run()

    def show_menu(self):
        self.screen.fill((255, 255, 255))
        half_screen_height = SCREEN_HEIGHT // 2
        hals_screen_width = SCREEN_WIDTH // 2 
        if self.death_count == 0:
            draw_message_component("Pressione qualquer tecla para iniciar", self.screen)
        
        else:
            draw_message_component("Pressione qualquer tecla para reiniciar", self.screen, pos_y_center = half_screen_height + 140)
            draw_message_component(
                f"Sua pontuaçao: {self.score}",
                self.screen,
                pos_y_center = half_screen_height - 50
            )


            draw_message_component(
                f"Contagem de vidas: {self.death_count} ",
                self.screen,
                pos_y_center = half_screen_height - 100
            )

            self.screen.blit(ICON, (hals_screen_width - 40, half_screen_height - 30))
            
        pygame.display.flip()
        self.handle_events_on_menu()