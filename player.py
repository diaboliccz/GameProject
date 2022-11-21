import pygame, sys
from enemy import Enemy

class Player(pygame.sprite.Sprite):
    def __init__(self, pos, groups, collision_sprites):
        super().__init__(groups)
        self.name = 'enemy'
        self.TimeOnRoad = 0
        self.level = 0
        self.Onroad = 0
        
        self.score = []
        
        self.name = []
        self.number = 1
        
        self.spawn_pos = (2080,3208)
        self.game_time = 0
        self.health = 750
        if self.game_time < 0:
            self.game_time = 0
        # image
        
        self.import_assets()
        self.image = pygame.image.load('../GameProject/graphics/cars/green.png')
        self.rect = self.image.get_rect(center = pos)
        
        self.pos = pygame.math.Vector2(self.rect.center)
        self.direction = pygame.math.Vector2(1,0)
        
        self.speed = 200
        
        # collision
        self.collision_sprites = collision_sprites
        self.hitbox = self.rect.inflate(0, -self.rect.height / 2)
        
    def collision(self, direction):
        if direction == 'horizontal':
            for sprite in self.collision_sprites.sprites():
                if sprite.hitbox.colliderect(self.hitbox):
                    self.health -= 1
                    if hasattr(sprite, 'name') and sprite.name == 'enemy' and self.health == 0:
                        pygame.quit()
                        sys.exit()
                        
                    if self.direction.x > 0:
                        self.hitbox.right = sprite.hitbox.left
                        self.rect.centerx = self.hitbox.centerx
                        self.pos.x = self.hitbox.centerx
                    if self.direction.x < 0:
                        self.hitbox.left = sprite.hitbox.right
                        self.rect.centerx = self.hitbox.centerx
                        self.pos.x = self.hitbox.centerx
                
        else:
            for sprite in self.collision_sprites.sprites():
                if sprite.hitbox.colliderect(self.hitbox):
                    self.health -= 1
                    if hasattr(sprite, 'name') and sprite.name == 'enemy' and self.health == 0:
                        pygame.quit()
                        sys.exit()
                        
                    if self.direction.y > 0:
                        self.hitbox.bottom = sprite.hitbox.top
                        self.rect.centery = self.hitbox.centery
                        self.pos.y = self.hitbox.centery
                    if self.direction.y < 0:
                        self.hitbox.top = sprite.hitbox.bottom
                        self.rect.centery = self.hitbox.centery
                        self.pos.y = self.hitbox.centery
        
    def import_assets(self):
        path = '../GameProject/graphics/player/right/0.png'
        #self.animation = [pygame.image.load(f'{path}{frame}.png').convert_alpha() for frame in range(4)]
    
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
    
    def Time_On_Road(self):
        if (1270 < self.pos.y < 1429) or (1612 < self.pos.y < 2005) or (2444 < self.pos.y < 2580) or (2801 < self.pos.y < 3103):
            #print('On Road')
            self.Onroad = 1
            self.TimeOnRoad+=1
            #print(self.TimeOnRoad)
    
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
            
            
        if keys[pygame.K_LSHIFT]:
            self.speed = 400
        else:
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
        self.Time_On_Road()
