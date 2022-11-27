import pygame

pygame.init()

music_stopwatch = pygame.mixer.Sound('../GameProject/sound/stopwatch.mp3')
music_stopwatch.set_volume(0.1)

music_heal = pygame.mixer.Sound('../GameProject/sound/heal.mp3')
music_heal.set_volume(0.1)


music_levelup = pygame.mixer.Sound('../GameProject/sound/level_up.mp3')
music_levelup.set_volume(0.1)

music_rage_quit = pygame.mixer.Sound('../GameProject/sound/rage_quit.mp3')
music_rage_quit.set_volume(0.1)

music_died = pygame.mixer.Sound('../GameProject/sound/died.mp3')
music_died.set_volume(0.3)



music_engine = pygame.mixer.Sound('../GameProject/sound/car_engine.mp3')
music_engine.set_volume(0.1)

music_background = pygame.mixer.Sound('../GameProject/sound/driving.mp3')
music_background.set_volume(0.1)

music_hit = pygame.mixer.Sound('../GameProject/sound/hit.mp3')
music_hit.set_volume(0.1)

music_click = pygame.mixer.Sound('../GameProject/sound/click.mp3')
music_click.set_volume(0.1)

music_booster = pygame.mixer.Sound('../GameProject/sound/booster.mp3')
music_booster.set_volume(0.1)