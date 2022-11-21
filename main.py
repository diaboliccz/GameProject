import pygame, sys, time

from settings import *
from player import *
from enemy import *
from items import *
from random import choice, randint
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


#font = pygame.font.Font('../GameProject/font/Cloey.ttf', 50)
font = pygame.font.Font(None, 50)
def Text_display(x, y, text, inflate_x , inflate_y, size):
    font = pygame.font.Font(None, size)
    Text = text
    Text_surf = font.render(Text,  True, 'white')
    Text_rect = Text_surf.get_rect(midtop = (x,y))
    display_surface.blit(Text_surf, Text_rect)
    pygame.draw.rect(display_surface, 'white', Text_rect.inflate(inflate_x,inflate_y), width = 8, border_radius = 5)
    
def Resume_Button():
    font = pygame.font.Font(None, 32)
    Resume_text = f'Leader Board'
    Resume_surf = font.render(Resume_text, True, 'white')
    Resume_rect = Resume_surf.get_rect(midtop = (WINDOW_WIDTH/2, WINDOW_HEIGHT/2 - 20))
    display_surface.blit(Resume_surf, Resume_rect)
    pygame.draw.rect(display_surface, 'white', Resume_rect.inflate(300,50), width = 8, border_radius = 5)
    
def display_level():
    level_text = f'Level : {level_format}'
    level_surf = font.render(level_text, True, 'white')
    level_rect = level_surf.get_rect(topright = (WINDOW_WIDTH - 20, 20))
    display_surface.blit(level_surf, level_rect)
    pygame.draw.rect(display_surface, 'white', level_rect.inflate(30,30), width = 8, border_radius = 5)

def display_TimeOnRoad():
    ScoreOnRoad_text = f'Score : {player.TimeOnRoad}'
    ScoreOnRoad_surf = font.render(ScoreOnRoad_text, True, 'white')
    ScoreOnRoad_rect = ScoreOnRoad_surf.get_rect(bottomleft = (20, WINDOW_HEIGHT - 20))
    display_surface.blit(ScoreOnRoad_surf, ScoreOnRoad_rect)
    pygame.draw.rect(display_surface, 'white', ScoreOnRoad_rect.inflate(30,30), width = 8, border_radius = 5)


    
def Current_Health():
    font = pygame.font.Font(None, 32)
    Health_Text = f'Health : {player.health}'
    Health_Text_surf = font.render(Health_Text, True, 'white')
    Health_Text_rect = Health_Text_surf.get_rect(bottomright = (WINDOW_WIDTH - 20, WINDOW_HEIGHT - 20))
    display_surface.blit(Health_Text_surf, Health_Text_rect)
    pygame.draw.rect(display_surface, 'white', Health_Text_rect.inflate(30,30), width = 8, border_radius = 5)

def Name_Show():
    font = pygame.font.Font(None, 32)
    name_text = f'{player.name[player.number-2]} is playing'
    name_surf = font.render(name_text, True, 'white')
    name_rect = name_surf.get_rect(midtop = (WINDOW_WIDTH/2, 20))
    display_surface.blit(name_surf, name_rect)
    pygame.draw.rect(display_surface, 'white', name_rect.inflate(30,30), width = 8, border_radius = 5)

# groups
all_sprites = AllSprites()
obstacle_sprites = pygame.sprite.Group()

# timer
enemy_timer = pygame.event.custom_type()
pygame.time.set_timer(enemy_timer, 150)
pos_list = []
items_timer = pygame.event.custom_type()
pygame.time.set_timer(items_timer, 100)

# sprites
player_spawn_pos = (2080,3208)
player = Player(player_spawn_pos,all_sprites, obstacle_sprites)
#items = Items(choice(ITEMS_START_POSITIONS), all_sprites)
items_list_pos = []

# main game timer
In_Game_Counter = 0
pygame.time.set_timer(pygame.USEREVENT, 1000)
def display_Counter():
    In_Game_Time_Text = f'{In_Game_format}'
    In_Game_Time_surf = font.render(In_Game_Time_Text, True, 'white')
    In_Game_Time_rect = In_Game_Time_surf.get_rect(topleft = (20,20))
    display_surface.blit(In_Game_Time_surf, In_Game_Time_rect)
    pygame.draw.rect(display_surface, 'white', In_Game_Time_rect.inflate(30,30), width = 8, border_radius = 5)

# music
class Music():
    
    def __init__(self, name, volume):
        self.music = pygame.mixer.Sound(f'../GameProject/sound/{name}.mp3')
        self.volume = volume
        self.volume_mode = 0
        self.image = pygame.image.load('../GameProject/graphics/music_0.jpg')
        self.music.set_volume(self.volume/100)
        
    def Music_Status(self):
        Image_0 = pygame.image.load('../GameProject/graphics/music_0.jpg')
        Image_1 = pygame.image.load('../GameProject/graphics/music_1.jpg')
        Image_2 = pygame.image.load('../GameProject/graphics/music_2.jpg')
        Image_3 = pygame.image.load('../GameProject/graphics/music_3.jpg')
        if self.volume_mode == 0:
            self.image = Image_0
            self.volume = 0
        elif self.volume_mode == 1:
            self.image = Image_1
            self.volume = 2
        elif self.volume_mode == 2:
            self.image = Image_2
            self.volume = 50
        elif self.volume_mode == 3:
            self.image = Image_3
            self.volume = 100
        
        self.image = pygame.transform.scale(self.image, (100,100))
        self.image_rect = self.image.get_rect(bottomleft = (0, WINDOW_HEIGHT))
        display_surface.blit(self.image, self.image_rect)
        if self.volume_mode != 0:
            self.music.play(-1)
        else:
            self.music.stop()

    def Stop(self):
        self.music.stop()
        
Bg_music = Music('music', 15)

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

Game_On = 1
Main_Menu_On = 1
Main_game_On = 0
Leader_Board_On = 0
Pause_On = 0

font_1 = pygame.font.Font(None, 50)
input_box = pygame.Rect(WINDOW_WIDTH/2 - 100, WINDOW_HEIGHT/2-200, 200, 50).inflate(100,0)
color_inactive = pygame.Color('lightskyblue3')
color_active = pygame.Color('dodgerblue2')
color = color_inactive
active = False
name = ''
done = False
while Game_On:
    while Main_Menu_On:
        keys = pygame.key.get_pressed()
        mouse = pygame.mouse.get_pos()
        
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            
            if (event.type == pygame.MOUSEBUTTONDOWN) and 509<mouse[0]<772 and 304<mouse[1]<352:
                Main_Menu_On = 0
                Main_game_On = 1
                player.name.append(name)
                player.number+=1
                name = ''
            
            if (event.type == pygame.MOUSEBUTTONDOWN) and 513<mouse[0]<770 and 503<mouse[1]<552:
                pygame.quit()
                sys.exit()
            
            if (event.type == pygame.MOUSEBUTTONDOWN) and 432<mouse[0]<847 and 402<mouse[1]<452:
                Main_Menu_On = 0
                Leader_Board_On = 1
            
            if event.type == pygame.MOUSEBUTTONDOWN:
                if input_box.collidepoint(event.pos):
                    active = True
                else:
                    active = False
                color = color_active if active else color_inactive
                
                if Bg_music.image_rect.collidepoint(event.pos):
                    Bg_music.volume_mode += 1
                    Bg_music.volume_mode%= 4
                    
            if event.type == pygame.KEYDOWN:
                if active:
                    if event.key == pygame.K_RETURN:
                        player.name.append(name)
                        player.number+=1
                        print(player.name)
                        name = ''
                    elif event.key == pygame.K_BACKSPACE:
                        name = name[:-1]
                    else:
                        name += event.unicode
            

        display_surface.fill('black')
        # Render the current text.
        txt_surface = font_1.render(name, True, color)
        # Resize the box if the text is too long.
        width = max(200, txt_surface.get_width()+10)
        input_box.w = width
        # Blit the text.
        display_surface.blit(txt_surface, (input_box.x+10, input_box.y+10))
        # Blit the input_box rect.
        pygame.draw.rect(display_surface, color, input_box, 2)
        
        print(mouse)
        #print(Bg_music.volume)
        #print(player.number)
        Text_display(353, 176, 'Input Your Name', 10000,10000, 30)
        Text_display(WINDOW_WIDTH/2,WINDOW_HEIGHT/2 - 50, 'Start', 200, 30 , 50)
        Text_display(WINDOW_WIDTH/2, WINDOW_HEIGHT/2 + 50, 'Leader Board', 200, 30, 50)
        Text_display(WINDOW_WIDTH/2, WINDOW_HEIGHT/2 + 150, 'Quit', 200, 30, 50)
        Bg_music.Music_Status()
        pygame.display.flip()
        clock.tick(fps)
        
        pygame.display.update()

    while Main_game_On:
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
                    Enemy(random_pos, [all_sprites, obstacle_sprites])
                    #print(pos_list)
                
                if len(pos_list) > 5:
                    del pos_list[0]
            
            if event.type == pygame.USEREVENT:
                player.game_time += 1
                if player.game_time < 0:
                    player.game_time = 0
            
            if event.type == items_timer:
                random_pos = choice(ITEMS_START_POSITIONS)
                if random_pos not in items_list_pos:
                    items_list_pos.append(random_pos)
                    Items(random_pos, [all_sprites, obstacle_sprites])
                    
                if len(items_list_pos) > 5:
                    del items_list_pos[0]
            
            if keys[pygame.K_z]:
                Main_Menu_On = 1
                Main_game_On = 0
            
            if keys[pygame.K_ESCAPE]:
                Main_game_On = 0
                Pause_On = 1
                
        In_Game_min = player.game_time//60
        In_Game_sec = player.game_time - (60*In_Game_min)
        In_Game_format = '{:02d}:{:02d}'.format(In_Game_min, In_Game_sec)
        dt = clock.tick()/1000
        
        # draw bg
        display_surface.fill('black')
        
        if player.level %2 == 0:
            if player.pos.y <= 1180:
                player.level += 1
        else:
            if player.pos.y >= 3200:
                player.level += 1
        
        # update
        all_sprites.update(dt)
        level_format = f'{player.level}'
        # draw
        all_sprites.customize_draw()
        
        display_TimeOnRoad()
        display_level()
        display_Counter()
        Current_Health()
        Name_Show()
        #print(items_list_pos)
        #print(pos_list)
        pygame.display.update()
    
    while Leader_Board_On:
        keys = pygame.key.get_pressed()
        mouse = pygame.mouse.get_pos()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
                
            if keys[pygame.K_ESCAPE]:
                Leader_Board_On = 0
                Main_Menu_On = 1
        display_surface.fill('black')
        
        Text_display(WINDOW_WIDTH/2, 30, 'Leader Board', 30, 30, 50)
        Text_display(300, 120, 'Name', 30,30, 40)
        for i in range(1, player.number):
            Text_display(300, 120+75*(i), f'{player.name[player.number-2]}', 10000, 10000, 30)
        Text_display(1000, 120, 'Score', 30, 30, 40)
        pygame.display.flip()
        pygame.display.update()
    '''while Pause_On:
        '''