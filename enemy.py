import pygame
from os import walk
from random import choice
from player import *
from settings import *

class Enemy(pygame.sprite.Sprite):
    def __init__(self, pos, groups):
        super().__init__(groups)
        self.name = 'enemy'
        self.level = 0
        self.pos = pos
        self.timer = 150
        
        for _, _, img_list in walk('../GameProject/graphics/player/right'):
            enemy_name = choice(img_list)
        
        self.image = pygame.image.load('../GameProject/graphics/player/right/' + enemy_name).convert_alpha()
        self.rect = self.image.get_rect(center = pos)
        
        self.pos = pygame.math.Vector2(self.rect.center)
        
        if pos[0] < 200:
            self.direction = pygame.math.Vector2(1,0)
        else:
            self.direction = pygame.math.Vector2(-1,0)
            self.image = pygame.transform.flip(self.image,True,True)
        
        self.speed = 200
        self.hitbox = self.rect.inflate(0, -self.rect.height / 2)
        
    def update(self, dt):
        self.pos += self.direction * self.speed * (3*(self.level+1)) * dt
        self.hitbox.center = (round(self.pos.x), round(self.pos.y))
        self.rect.center = self.hitbox.center
        #print(self.name)
        if not -200 < self.rect.x < 3600:
            self.kill()