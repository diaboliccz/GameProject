import pygame
from os import walk
from random import *
from player import *
from settings import *
class Boost(pygame.sprite.Sprite):
    def __init__(self, pos, groups):
        super().__init__(groups)
        self.name = 'boost'
        self.pos = pos
        

        self.image = pygame.image.load('../GameProject/graphics/items/boost.png').convert_alpha()
        self.image = pygame.transform.scale(self.image, (60,75))
        self.rect = self.image.get_rect(center = pos)
        
        self.pos = pygame.math.Vector2(self.rect.center)
        
        self.direction = pygame.math.Vector2(0,1)
        
        self.speed = 500
        self.hitbox = self.rect.inflate(0, -self.rect.height / 2)
        
    def update(self, dt):
        self.pos += self.direction * self.speed * dt
        self.hitbox.center = (round(self.pos.x), round(self.pos.y))
        self.rect.center = self.hitbox.center
        #print(self.name)
        if not 660<self.rect.x<2500:
            self.kill()
        if self.rect.y == choice(ITEMS_END_POSITIONS):
            self.speed = 0
            
class Health(pygame.sprite.Sprite):
    def __init__(self, pos, groups):
        super().__init__(groups)
        self.name = 'health'
        self.pos = pos
        
        self.image = pygame.image.load('../GameProject/graphics/items/health.png').convert_alpha()
        self.image = pygame.transform.scale(self.image, (60,50))
        self.rect = self.image.get_rect(center = pos)
        
        self.pos = pygame.math.Vector2(self.rect.center)
        
        self.direction = pygame.math.Vector2(0,1)
        
        self.speed = 300
        self.hitbox = self.rect.inflate(0, -self.rect.height / 2)
        
    def update(self, dt):
        self.pos += self.direction * self.speed * dt
        self.hitbox.center = (round(self.pos.x), round(self.pos.y))
        self.rect.center = self.hitbox.center
        #print(self.name)
        if not 660<self.rect.x<2500:
            self.kill()        
        if self.rect.y == choice(ITEMS_END_POSITIONS):
            self.speed = 0
            
class Stopwatch(pygame.sprite.Sprite):
    def __init__(self, pos, groups):
        super().__init__(groups)
        self.name = 'stopwatch'
        self.pos = pos
        
        self.image = pygame.image.load('../GameProject/graphics/items/stopwatch.png').convert_alpha()
        self.image = pygame.transform.scale(self.image, (60,75))
        self.rect = self.image.get_rect(center = pos)
        
        self.pos = pygame.math.Vector2(self.rect.center)
        
        self.direction = pygame.math.Vector2(0,1)
        
        self.speed = 200
        self.hitbox = self.rect.inflate(0, -self.rect.height / 2)
        
    def update(self, dt):
        self.pos += self.direction * self.speed * dt
        self.hitbox.center = (round(self.pos.x), round(self.pos.y))
        self.rect.center = self.hitbox.center
        #print(self.name)
        
        if not 660<self.rect.x<2500:
            self.kill()
        if self.rect.y > 2800:
            self.kill()
        
        if self.rect.y == choice(ITEMS_END_POSITIONS):
            self.speed = 0