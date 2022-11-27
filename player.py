import pygame, sys
from enemy import *
from items import Boost, Health, Stopwatch
from settings import *
from music import *
from math import *

pygame.init()
class Player(pygame.sprite.Sprite):
    def __init__(self, pos, groups, collision_sprites):
        super().__init__(groups)
        self.level = 0
        self.score_on_road = 0
        self.final_score = 0
        self.GameOver = 0
        
        self.boost_max = WINDOW_WIDTH/2
        self.boost_current = self.boost_max
        
        self.health_max = WINDOW_WIDTH/320
        self.health_current = self.health_max
        
        self.enemy_damage = 1
        self.hit_count = 0
        
        self.number = 0
        
        self.name_list = []
        self.score_list = []
        self.list = {}
        
        self.game_time = 360
        
        self.spawn_pos = (2080,3208)
        
        # image
                
        self.image = pygame.image.load('../GameProject/graphics/cars/green.png')
        self.rect = self.image.get_rect(center = pos)
        
        self.pos = pygame.math.Vector2(self.rect.center)
        self.direction = pygame.math.Vector2(1,0)
        self.far = 0
        self.speed = 0.1
        
        # collision
        self.collision_sprites = collision_sprites
        self.hitbox = self.rect.inflate(0, -self.rect.height / 2)
        
    def collision(self, direction):
        for sprite in self.collision_sprites.sprites():
            if sprite.hitbox.colliderect(self.hitbox):
                if hasattr(sprite, 'name'):
                    if sprite.name == 'enemy':
                        pygame.sprite.spritecollide(self, self.collision_sprites, True)
                        music_hit.play()
                        self.hit_count += 1
                        self.health_current -= self.enemy_damage
                    if sprite.name == 'health':
                        pygame.sprite.spritecollide(self, self.collision_sprites, True)
                        music_heal.play()
                        if self.health_current < 3:
                            self.health_current += 1
                        else:
                            self.health_current = self.health_max
                    if sprite.name == 'boost':
                        pygame.sprite.spritecollide(self, self.collision_sprites, True)
                        music_booster.play()
                        if self.boost_current < 1200:
                            self.boost_max += 80
                        else:
                            self.boost_max = 1280
                    if sprite.name == 'stopwatch':
                        pygame.sprite.spritecollide(self, self.collision_sprites, True)
                        music_stopwatch.play()
                        if self.game_time < 340:
                            self.game_time += 20
                        else:
                            self.game_time = 360
                else:
                    if direction == 'horizontal':
                        if self.direction.x > 0:
                            self.hitbox.right = sprite.hitbox.left
                            self.rect.centerx = self.hitbox.centerx
                            self.pos.x = self.hitbox.centerx
                        if self.direction.x < 0:
                            self.hitbox.left = sprite.hitbox.right
                            self.rect.centerx = self.hitbox.centerx
                            self.pos.x = self.hitbox.centerx
                    if direction == 'vertical':
                        if self.direction.y > 0:
                            self.hitbox.bottom = sprite.hitbox.top
                            self.rect.centery = self.hitbox.centery
                            self.pos.y = self.hitbox.centery
                        if  self.direction.y < 0:
                            self.hitbox.top = sprite.hitbox.bottom
                            self.rect.centery = self.hitbox.centery
                            self.pos.y = self.hitbox.centery
    
    def move(self, dt):
        if self.direction.magnitude() != 0:
            self.direction = self.direction.normalize()
        
        # horinoztal move + collide
        self.pos.x += self.direction.x * self.speed * dt
        self.hitbox.centerx = round(self.pos.x)
        self.rect.centerx = self.hitbox.centerx
        self.collision('horizontal')
            
        self.pos.y += self.direction.y * self.speed * dt
        self.hitbox.centery = round(self.pos.y)
        self.rect.centery = self.hitbox.centery
        self.collision('vertical')
    
    def score_road(self):
        if (1270 < self.pos.y < 1429) or (1612 < self.pos.y < 2005) or (2444 < self.pos.y < 2580) or (2801 < self.pos.y < 3103):
            self.score_on_road+=1*(self.level)
    
    def level_up(self):        
        if self.level %2 == 0:
            if self.pos.y <= 1180:
                self.level += 1
                music_levelup.play()
        else:
            if self.pos.y >= 3200:
                self.level += 1
                music_levelup.play()
    
    def input(self):
        green_right = pygame.image.load('../GameProject/graphics/objects/simple/green_right.png')
        green_left = pygame.image.load('../GameProject/graphics/objects/simple/green_left.png')
        green_up = pygame.image.load('../GameProject/graphics/objects/simple/green_up.png')
        green_down = pygame.image.load('../GameProject/graphics/objects/simple/green_down.png')
        keys = pygame.key.get_pressed()
        if keys[pygame.K_RIGHT] or keys[pygame.K_LEFT]:
            self.direction.y = 0
            if keys[pygame.K_RIGHT]:
                self.direction.x = 1
                self.image = green_right
            elif keys[pygame.K_LEFT]:
                self.direction.x = -1
                self.image = green_left
            else:
                self.direction.x = 0
        elif keys[pygame.K_UP] or keys[pygame.K_DOWN]:
            self.direction.x = 0
            if keys[pygame.K_UP]:
                self.direction.y = -1
                self.image = green_up
            elif keys[pygame.K_DOWN]:
                self.direction.y = 1
                self.image = green_down
            else:
                self.direction.y = 0
        else:
            self.direction.x = 0
            self.direction.y = 0
        if (keys[pygame.K_DOWN] or keys[pygame.K_UP]) and (keys[pygame.K_LEFT] or keys[pygame.K_RIGHT]):
            self.direction.x = 0
            self.direction.y = 0    
            
        if self.boost_current > 0 and keys[pygame.K_LSHIFT]:
            music_engine.play()
            self.speed = 400
            self.boost_current-=5
        else:
            music_engine.stop()
            self.speed = 200
        
        if keys[pygame.K_r]:
            self.pos.x, self.pos.y = 2080,3208
            self.game_time = 0
            self.TimeOnRoad = 0
    
    def restrict(self):
        if self.rect.left < 640:
            self.pos.x = 640 + self.rect.width / 2
            self.hitbox.left = 640
            self.rect.left = 640
        if self.rect.right > 2560:
            self.pos.x = 2560 - self.rect.width / 2
            self.hitbox.right = 2560
            self.rect.right = 2560
        if self.rect.bottom > 3500:
            self.pos.y = 3500 - self.rect.width / 2
            self.rect.bottom = 3500
            self.hitbox.bottom = self.rect.bottom
    
    def update(self, dt):
        self.input()
        self.move(dt)
        self.restrict()
        self.score_road()
        self.level_up()
        
        self.final_score = (10000*self.level)+(self.score_on_road)
        self.list = dict(zip(self.name_list, self.score_list))
        
        self.list = sorted(self.list.items(), key = lambda x:x[1], reverse = 1)
        #self.health_current -=1
        if self.level %2 == 0:
            self.far = int(sqrt((self.pos.x-1623)**2+(self.pos.y-1161)**2))
        else:
            self.far = int(sqrt((self.pos.x-2080)**2+(self.pos.y-3208)**2))
            
        self.enemy_damage =  1 + self.level//5
        
    
        self.health_current -= 0.0001 * self.level
        if self.boost_current <= self.boost_max:
            self.boost_current+=1