import pygame
from os import walk
from random import choice
from player import *
from settings import *

class Items(pygame.sprite.Sprite):
    def __init__(self, pos, groups):
        super().__init__(groups)
        
        self.level = 0
        
        for _, _, img_list in walk('../GameProject/graphics/items/'):
            item_name = choice(img_list)
        self.name = item_name[:-4]
        
        self.image = pygame.image.load('../GameProject/graphics/items/' + item_name).convert_alpha()
        self.image = pygame.transform.scale(self.image, (60,75))
        #self.image = pygame.image.load('../GameProject/graphics/objects/simple/enemy.png').convert_alpha()
        self.rect = self.image.get_rect(center = pos)
        
        self.pos = pygame.math.Vector2(self.rect.center)
        
        self.direction = pygame.math.Vector2(0,1)
        
        self.speed = 0
        self.hitbox = self.rect.inflate(0, -self.rect.height / 2)
        
    def update(self,dt):
        self.pos += self.direction * self.speed * (self.level+1) * dt
        self.hitbox.center = (round(self.pos.x), round(self.pos.y))
        self.rect.center = self.hitbox.center
        #print(self.name)
        if self.rect.y == choice(ITEMS_END_POSITIONS):
            self.speed = 0