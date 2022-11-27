import pygame, sys, time

from settings import *
from player import *
from enemy import *
from items import *
from music import *

from random import *
from datetime import *
from sprite import LongSprite, SimpleSprite



class AllSprites(pygame.sprite.Group):
    def __init__(self):
        super().__init__()
        self.offset = pygame.math.Vector2()
        self.bg = pygame.image.load('../GameProject/graphics/main/map.png').convert()
        self.fg = pygame.image.load('../GameProject/graphics/main/overlay.png').convert_alpha()
        
    def customize_draw(self):
        
        # change offset vector
        self.offset.x = player.rect.centerx - WINDOW_WIDTH/2
        self.offset.y = player.rect.centery - WINDOW_HEIGHT/2
        
        display_surface.blit(self.bg, -self.offset)
        
        for sprite in sorted(self.sprites(), key = lambda sprite: sprite.rect.centery):
            offset_pos = sprite.rect.topleft - self.offset
            display_surface.blit(sprite.image, offset_pos)
            
        display_surface.blit(self.fg, -self.offset)

pygame.init()
# create a surface
display_surface = pygame.display.set_mode((WINDOW_WIDTH,WINDOW_HEIGHT))
pygame.display.set_caption('Car Crossing')
clock = pygame.time.Clock()
fps = 120

font = pygame.font.Font(None, 50)
def Text_display(x, y, text, inflate_x , inflate_y, size):
    font = pygame.font.Font(None, size)
    Text = text
    Text_surf = font.render(Text,  True, 'black')
    Text_rect = Text_surf.get_rect(midtop = (x,y))
    display_surface.blit(Text_surf, Text_rect)
    pygame.draw.rect(display_surface, 'black', Text_rect.inflate(inflate_x,inflate_y), width = 8, border_radius = 5)
    
def Resume_Button():
    font = pygame.font.Font(None, 32)
    Resume_text = f'Leader Board'
    Resume_surf = font.render(Resume_text, True, 'white')
    Resume_rect = Resume_surf.get_rect(midtop = (WINDOW_WIDTH/2, WINDOW_HEIGHT/2 - 20))
    display_surface.blit(Resume_surf, Resume_rect)
    pygame.draw.rect(display_surface, 'white', Resume_rect.inflate(300,50), width = 8, border_radius = 5)
    
def display_level():
    level_text = f'Level : {player.level}'
    level_surf = font.render(level_text, True, 'white')
    level_rect = level_surf.get_rect(topright = (WINDOW_WIDTH - 20, 20))
    display_surface.blit(level_surf, level_rect)
    pygame.draw.rect(display_surface, 'white', level_rect.inflate(30,30), width = 8, border_radius = 5)

def display_TimeOnRoad():
    ScoreOnRoad_text = f'Score : {player.final_score}'
    ScoreOnRoad_surf = font.render(ScoreOnRoad_text, True, 'white')
    ScoreOnRoad_rect = ScoreOnRoad_surf.get_rect(topright = (WINDOW_WIDTH-20, 100))
    display_surface.blit(ScoreOnRoad_surf, ScoreOnRoad_rect)
    pygame.draw.rect(display_surface, 'white', ScoreOnRoad_rect.inflate(30,30), width = 8, border_radius = 5)

def Name_Show():
    font = pygame.font.Font(None, 32)
    name_text = f'{player.name_list[player.number-1]} is playing'
    name_surf = font.render(name_text, True, 'white')
    name_rect = name_surf.get_rect(midtop = (WINDOW_WIDTH/2, 20))
    display_surface.blit(name_surf, name_rect)
    pygame.draw.rect(display_surface, 'white', name_rect.inflate(30,30), width = 8, border_radius = 5)
Game_On = 1
Main_Menu_On = 1
Main_game_On = 0
Leaderboard_On = 0
Pause_On = 0
# groups
all_sprites = AllSprites()
obstacle_sprites = pygame.sprite.Group()

# timer
enemy_timer = pygame.event.custom_type()
pygame.time.set_timer(enemy_timer, 150)
pos_list = []
enemy_level_up_timer = pygame.event.custom_type()
pygame.time.set_timer(enemy_level_up_timer, 15000)

boost_timer = pygame.event.custom_type()
pygame.time.set_timer(boost_timer, 5000)

health_timer = pygame.event.custom_type()
pygame.time.set_timer(health_timer, 8000)

stopwatch_timer = pygame.event.custom_type()
pygame.time.set_timer(stopwatch_timer, 10000)

# sprites
player_spawn_pos = (2080,3208)
player = Player(player_spawn_pos,all_sprites, obstacle_sprites)
enemy = Enemy(choice(ENEMY_START_POSITIONS),[all_sprites, obstacle_sprites])
boost_list = []
health_list = []
stopwatch_list = []

# main game timer
Second = pygame.event.custom_type()
pygame.time.set_timer(Second, 1000)

def display_Counter():
    game_time_text = f'{game_time_format}'
    game_time_surf = font.render(game_time_text, True, 'white')
    game_time_rect = game_time_surf.get_rect(topleft = (20,20))
    display_surface.blit(game_time_surf, game_time_rect)
    pygame.draw.rect(display_surface, 'white', game_time_rect.inflate(30,30), width = 8, border_radius = 5)
    
font_1 = pygame.font.Font(None, 50)
input_box = pygame.Rect(WINDOW_WIDTH/2 - 100, WINDOW_HEIGHT/2-200, 200, 50).inflate(100,0)
color_inactive = pygame.Color(255,255,204)
color_active = pygame.Color(229,255,204)
color = color_inactive
active = False
name = ''
done = False

def box(x, y, width, height, color_rect, text, color_text, text_size, inflate_x, inflate_y, border_size, border_radius):
    font = pygame.font.Font(None, text_size)
    
    text_surf = font.render(text, True, color_text)
    text_box = pygame.Rect(x,y, width, height).inflate(inflate_x, inflate_y)
    
    display_surface.blit(text_surf, text_box)
    pygame.draw.rect(display_surface, color_rect, text_box, border_size, border_radius)

def input_name_box():
    # Render the current text.
    txt_surface = font_1.render(name, True, (0,51,51)) # color font
    # Resize the box if the text is too long.
    width = max(400, txt_surface.get_width()+20)
    input_box.w = width
    # Blit the text.
    display_surface.blit(txt_surface, (input_box.x+15, input_box.y+5))
    # Blit the input_box rect.
    pygame.draw.rect(display_surface, color, input_box, 5,5) # color rect
    
    
# draw component
def component_main_menu():
    display_surface.fill('grey')
    
    road = pygame.image.load('../GameProject/graphics/bg.jpg').convert_alpha()
    road = pygame.transform.scale(road, (1280,720))
    road_rect = road.get_rect(bottomleft = (0, WINDOW_HEIGHT))
    display_surface.blit(road, road_rect)
    
    Human = pygame.image.load('../GameProject/graphics/player/down/2.png').convert_alpha()
    Human_rect = Human.get_rect(center = (954,188))
    display_surface.blit(Human, Human_rect)
    
    Text_display(WINDOW_WIDTH-150, 30, '65010039 Kolawat Inpan',30, 30, 30)
    Text_display(353, 176, 'Input Your Name', 10000,10000, 30)
    Text_display(WINDOW_WIDTH/2,WINDOW_HEIGHT/2 - 50, 'Start', 200, 30 , 50)
    Text_display(WINDOW_WIDTH/2, WINDOW_HEIGHT/2 + 50, 'Leader Board', 200, 30, 50)
    Text_display(WINDOW_WIDTH/2, WINDOW_HEIGHT/2 + 150, 'Quit', 200, 30, 50)
    #box(500, 500,0,0,'black', 'Hello', 'black', 50, 300, 30, 2, 10)
    input_name_box()


def component_main_game():
    
    display_TimeOnRoad()
    display_level()
    display_Counter()
    #Current_Health()
    Name_Show()
    Text_display(WINDOW_WIDTH/2, WINDOW_HEIGHT/2-100, f'{player.far}', 30, 30, 32)
    # boost bar
    pygame.draw.rect(display_surface, 'red', pygame.Rect(0, WINDOW_HEIGHT-30, player.health_current*320, 15))
    pygame.draw.rect(display_surface, (204,255,255), pygame.Rect(0,WINDOW_HEIGHT - 15, player.boost_current,15))
    #print(player.score)

def component_pause():
    Text_display(WINDOW_WIDTH/2, 200, 'Resume', 200, 30, 40)
    Text_display(WINDOW_WIDTH/2, 320, 'Leader Board', 200, 30, 40)
    Text_display(WINDOW_WIDTH/2, 440, 'Back to main menu', 200, 30, 40)
    Text_display(WINDOW_WIDTH/2, 560, 'Quit', 200, 30, 40)

def component_leaderboard():
        display_surface.fill('grey')
        
        Text_display(WINDOW_WIDTH/2, 30, 'Leaderboard', 30, 30, 50)
        Text_display(300, 120, 'Name', 30,30, 40)
        for i in range(0, len(player.name_list)):
            player.list = dict(zip(player.name_list, player.score_list))
            player.list = sorted(player.list.items(), key = lambda x:x[1], reverse = 1)

            Text_display(300, 200+125*(i), f'{player.list[i][0]}', 10000, 10000, 30)
            Text_display(1000, 200+125*(i), f'{player.list[i][1]}', 10000, 10000, 30)
        
        Text_display(1000, 120, 'Score', 30, 30, 40)
        print(player.list)
def component_game_over():
    Main_game_On = 0
    display_surface.fill('grey')
    Text_display(WINDOW_WIDTH/2, 50, 'Game Over', 10000, 10000, 60)
    Text_display(WINDOW_WIDTH/2, WINDOW_HEIGHT/2-50, f'Your point are {player.score_list[player.number-1]}', 10000, 10000, 60)
    Text_display(600,600, 'Press ESC to back to main menu', 300, 30, 50)

# sprite setup
for file_name, pos_list in SIMPLE_OBJECTS.items():
    path = f'../GameProject/graphics/objects/simple/{file_name}.png'
    surf = pygame.image.load(path).convert_alpha()
    for pos in pos_list:
        SimpleSprite(surf, pos, [all_sprites, obstacle_sprites])

for file_name, pos_list in LONG_OBJECTS.items():
    path = f'../GameProject/graphics/objects/long/{file_name}.png'
    surf = pygame.image.load(path).convert_alpha()
    for pos in pos_list:
        LongSprite(surf, pos, [all_sprites, obstacle_sprites])


while Game_On:
    
    while Main_Menu_On:
        keys = pygame.key.get_pressed()
        mouse = pygame.mouse.get_pos()
        player.health_current = player.health_max
        player.boost_current = player.boost_max
        
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            component_main_menu()  
            if event.type == pygame.MOUSEBUTTONDOWN:
                if 509<mouse[0]<772 and 304<mouse[1]<352: #กดปุ่ม start
                    music_click.play()
                    Main_Menu_On = 0
                    Main_game_On = 1
                    
                    player.name_list.append(name)
                    player.number+=1
                    name = ''
                    
                    player.pos.x, player.pos.y = 2080, 3208
                    player.game_time = 360
                    player.score_on_road = 0
                    player.level = 0
                    player.boost_max = WINDOW_WIDTH/2
                    
                elif 513<mouse[0]<770 and 503<mouse[1]<552:
                    music_click.play()
                    pygame.quit()
                    sys.exit()
                elif 432<mouse[0]<847 and 402<mouse[1]<452:
                    music_click.play()
                    Main_Menu_On = 0
                    Leaderboard_On = 1
            if event.type == pygame.MOUSEBUTTONDOWN:
                if input_box.collidepoint(event.pos):
                    music_click.play()
                    active = True
                else:
                    active = False
                color = color_active if active else color_inactive
                
            if event.type == pygame.KEYDOWN:
                if active:
                    if event.key == pygame.K_BACKSPACE:
                        name = name[:-1]
                    else:
                        name += event.unicode
        print(mouse)
        pygame.display.flip()
        pygame.display.update()

    while Main_game_On:
        enemy.level = player.level
        keys = pygame.key.get_pressed()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                print('(%.2f)'%(player.pos.x)+'(%.2f)'%(player.pos.y))
            if event.type == enemy_timer:
                random_pos = choice(ENEMY_START_POSITIONS)
                if random_pos not in pos_list:
                    pos_list.append(random_pos)
                    pos = (random_pos[0], random_pos[1] + randint(-8,8))
                    Enemy(random_pos, [all_sprites ,obstacle_sprites])
                    #print(pos_list)
                if len(pos_list) > 5:
                    del pos_list[0]
                    
            if event.type == Second:
                player.game_time -= 1
                if player.game_time == 0:
                    Main_game_On = 0
                    player.GameOver = 1
                    
            if event.type == boost_timer:
                random_pos = choice(BOOST_START_POSITIONS)
                if random_pos not in boost_list:
                    boost_list.append(random_pos)
                    Boost(random_pos, [all_sprites, obstacle_sprites])
                    
                if len(boost_list) > 5:
                    del boost_list[0]
            
            if event.type == health_timer:
                random_pos = choice(HEALTH_START_POSITIONS)
                if random_pos not in health_list:
                    health_list.append(random_pos)
                    Health(random_pos, [all_sprites, obstacle_sprites])
                    
                if len(health_list) > 5:
                    del health_list[0]
            
            if event.type == stopwatch_timer:
                random_pos = choice(STOPWATCH_START_POSITIONS)
                if random_pos not in stopwatch_list:
                    stopwatch_list.append(random_pos)
                    Stopwatch(random_pos, [all_sprites, obstacle_sprites])
                    
                if len(stopwatch_list) > 5:
                    del stopwatch_list[0]
                
            if keys[pygame.K_ESCAPE]:
                Main_game_On = 0
                Pause_On = 1
                
            if enemy.pos.x == player.pos.x and enemy.pos.y == player.pos.y:
                pygame.quit()
                sys.exit()
        
        dt = clock.tick(fps)/1000
        
        game_time_sec = player.game_time % 60
        game_time_min = player.game_time // 60
        game_time_format = '{:02d}:{:02d}'.format(game_time_min, game_time_sec)
        
        # draw bg
        display_surface.fill('black')

        # update
        all_sprites.update(dt)
        
        # draw
        all_sprites.customize_draw()
        
        if player.health_current <= 0:
            music_engine.stop()
            music_died.play()
            player.score_list.append(player.final_score)
            Main_game_On = 0
            player.GameOver = 1
        
        component_main_game() 
        pygame.display.update()
        
    while Pause_On:
        keys = pygame.key.get_pressed()
        mouse = pygame.mouse.get_pos()
        display_surface.fill((128,128,128))
        component_pause()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                if (492<mouse[0]<789 and 189<mouse[1]<237): # resume
                    music_click.play()
                    Pause_On = 0
                    Main_game_On = 1
                elif 452<mouse[0]<827 and 312<mouse[1]<357: # leader board
                    music_rage_quit.play()
                    Pause_On = 0
                    player.score_list.append(player.final_score)
                    Leaderboard_On = 1
                    
                elif 414<mouse[0]<864 and 432<mouse[1]<477: # back to main menu
                    music_rage_quit.play()
                    Pause_On = 0
                    player.score_list.append(player.final_score)
                    Main_Menu_On = 1
                elif 517<mouse[0]<763 and 552<mouse[1]<596: # quit
                    music_rage_quit.play()
                    pygame.quit()
                    sys.exit()
        
        #print(mouse)
        pygame.display.update()
        
    while Leaderboard_On:
        
        keys = pygame.key.get_pressed()
        mouse = pygame.mouse.get_pos()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if keys[pygame.K_ESCAPE]:
                Leaderboard_On = 0
                Main_Menu_On = 1
        component_leaderboard()        
        pygame.display.flip()
        pygame.display.update()
    
    while player.GameOver:
        component_game_over()
        keys = pygame.key.get_pressed()
        mouse = pygame.mouse.get_pressed()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if keys[pygame.K_ESCAPE]:
                player.GameOver = 0
                Main_Menu_On = 1
        pygame.display.update()