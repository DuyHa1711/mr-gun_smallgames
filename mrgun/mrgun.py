import pygame
from sys import exit
from random import randint
import math
#layout0:main tab
#layout1:gameplay
pygame.init()
pygame.mixer.init()
clock = pygame.time.Clock()
screen = pygame.display.set_mode((400,600))
background = pygame.Surface((400,600))
pygame.display.set_caption('Mr Gun Fake by Ha Duc Duy')
game_layout = 0
pygame.mixer.music.load('audio/theme.mp3')
pygame.mixer.music.play(-1)
boom = pygame.mixer.Sound('audio/boom.mp3')
headshot = pygame.mixer.Sound('audio/headshot.mp3')
#This is the set up the layout 0
class Maintab:
    def __init__(self):
        with open('fonts/level.txt') as file:
            level = file.read()
            level = int(level)
        self.title = pygame.image.load('image/title.PNG').convert_alpha()
        self.title_rect = self.title.get_rect(center=(200,100))

        self.start_line = pygame.image.load('image/startline.PNG').convert_alpha()
        self.start_line_rect = self.start_line.get_rect(center=(200,400))
        self.faded_speed = 255

        self.font = pygame.font.Font(None,30)
        self.level = self.font.render(f'Level {level}',True,'White')
        self.level_rect = self.level.get_rect(center = (200,150))
    def draw(self):
        screen.blit(background,(0,0))
        screen.blit(self.title,self.title_rect)
        screen.blit(self.level,self.level_rect)
        screen.blit(self.start_line,self.start_line_rect)
    def event(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()
            if event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
                global game_layout
                game_layout = 1
#all thing about character

class stair:
    def __init__(self):
        self.step = randint(3,7)
        self.surf = pygame.Surface((400,self.step*20))
        self.rect = self.surf.get_rect(midbottom = (200,420))
        self.starting_point = 200
        self.starting_point_oppo = 250
        self.color = 200
        self.color_transition=20
        self.rect1 = []
        self.rect2 = []
    def get_rect1_and2(self):
        for y in range(self.step):
            rect1 = pygame.Rect(0,self.step*20 - 20*(y+1) , self.starting_point - 20*y ,20)
            rect2 = pygame.Rect(self.starting_point-20*y, 20*(self.step-y-1),400-self.starting_point+20*y,20)
            self.rect1.append(rect1)
            self.rect2.append(rect2)
    def get_rect1_and2_oppo(self):
        for y in range(self.step):
            rect1 = pygame.Rect(self.starting_point_oppo+20*y,20*(self.step-y-1),400-(self.starting_point_oppo+20*y),20)
            rect2 = pygame.Rect(0,20*(self.step-y-1),self.starting_point_oppo+20*y,20)
            self.rect1.append(rect1)
            self.rect2.append(rect2)

    def draw(self):
        for y in range(self.step):
            surf1 = pygame.Surface((self.starting_point-20*y,20))
            surf2 = pygame.Surface((400-self.starting_point+20*y,20))
            surf1.fill((self.color,self.color,self.color))
            surf2.fill((self.color-self.color_transition,self.color-self.color_transition,self.color-self.color_transition))
            self.surf.blit(surf1,self.rect1[y])
            self.surf.blit(surf2,self.rect2[y])
        screen.blit(self.surf,self.rect)
    def draw_oppo(self):
        for y in range(self.step):
            surf1 = pygame.Surface((400-self.starting_point_oppo-20*y,20))
            surf2 = pygame.Surface((self.starting_point_oppo+20*y,20))
            surf1.fill((self.color-20,self.color-20,self.color-20))
            surf2.fill((self.color-40,self.color-40,self.color-40))
            self.surf.blit(surf1,self.rect1[y])
            self.surf.blit(surf2,self.rect2[y])
        screen.blit(self.surf,self.rect)
class Character:
    def __init__(self,x_pos,y_pos):
        self.x_pos = x_pos
        self.y_pos = y_pos
        self.body = pygame.Surface((15,25))
        self.body_rect = self.body.get_rect(midbottom = (self.x_pos,self.y_pos))
        self.body.fill('Pink')
        self.head = pygame.Surface((19,17))
        self.head_rect = self.head.get_rect(midbottom=self.body_rect.midtop)
        self.head.fill('White')
        #set up for the gun of the character
        #basic gun set up
        self.gun_org = pygame.image.load('image/gun.png').convert_alpha()
        self.gun_org = pygame.transform.rotozoom(self.gun_org,0,0.7)
        self.gun_org = pygame.transform.flip(self.gun_org,True,False)
        self.gun = self.gun_org
        self.gun_rect = self.gun.get_rect(midright = self.body_rect.center)
        self.gun_state = True
        self.gun_angle = 0
        #line at the gun
        self.gunline_surf = pygame.Surface((69,19),pygame.SRCALPHA)
        self.im_rect = self.gun.get_rect(topleft = (41,0))
        pygame.draw.line(self.gunline_surf, 'White' , (self.im_rect.left,self.im_rect.top +4), (0,self.im_rect.top+4), 1)
        self.gunline_surf.blit(self.gun, self.im_rect)
        self.gunline_rect = self.gunline_surf.get_rect(midright = self.body_rect.center)
        self.gunline_surf_org = self.gunline_surf
        self.ammo = pygame.Surface((5,5))
        self.ammo.fill('White')
        self.ammo_rect = self.ammo.get_rect()
    def draw(self):
        self.head_rect = self.head.get_rect(midbottom=self.body_rect.midtop)
        screen.blit(self.head,self.head_rect)
        screen.blit(self.body,self.body_rect)
        screen.blit(self.gun,self.gun_rect)
    def draw_gunline(self):
        self.head_rect = self.head.get_rect(midbottom = self.body_rect.midtop)
        screen.blit(self.head,self.head_rect)
        screen.blit(self.body,self.body_rect)
        screen.blit(self.gunline_surf,self.gunline_rect)
class Enemy:
    def __init__(self,x_pos,y_pos):
        #initial set up (will add multiple enemy)
        self.x_pos = x_pos
        self.y_pos = y_pos
        self.body = pygame.Surface((15,25))
        self.body_rect = self.body.get_rect(midbottom = (self.x_pos,self.y_pos))
        self.body.fill('Pink')
        self.head = pygame.Surface((19,17))
        self.head_rect = self.head.get_rect(midbottom=self.body_rect.midtop)
        self.head.fill('White')
        #gun image for the dude
        self.gun_org = pygame.image.load('image/gun.png').convert_alpha()
        self.gun_org = pygame.transform.rotozoom(self.gun_org,0,0.7)
        self.gun = self.gun_org
        self.gun_rect = self.gun.get_rect(midleft = self.body_rect.center)
        #ammo for shooting our main character
        self.ammo = pygame.Surface((5,5))
        self.ammo.fill('White')
        self.ammo_rect = self.ammo.get_rect()
    def draw(self):
        self.head_rect = self.head.get_rect(midbottom=self.body_rect.midtop)
        screen.blit(self.head,self.head_rect)
        screen.blit(self.body,self.body_rect)
        screen.blit(self.gun,self.gun_rect)
        
class Ingame:
    def __init__(self):
        self.num_of_stair = 20
        self.stair_list = []
        self.index = 1
        self.blockunder = pygame.Surface((400,180))
        self.blockunder.fill((200,200,200))
        self.blockunder_rect = self.blockunder.get_rect(topleft = (0,420))
        self.char = Character(300,420)
        self.jump_index = 0
        #set up for enemy spawning
        self.enemy_spawn_state = True
    def stair_process(self):
        #add the stair to the list
        for x in range(self.num_of_stair):
            self.stair_list.append(stair())
            if x%2 == 0:
                self.stair_list[x].get_rect1_and2()
            elif x%2 == 1:
                self.stair_list[x].get_rect1_and2_oppo()
    def stair_x_and_y_update(self):
        #add the x_pos and y_pos for each of the stair
        self.stair_list[0].rect.midbottom = (200,self.blockunder_rect.top)
        while self.index < self.num_of_stair:
            obj = self.stair_list[self.index]
            objbef = self.stair_list[self.index - 1]
            obj.rect.midbottom = objbef.rect.midtop
            self.index = self.index + 1
        self.index = 1
    

    def render(self):
        screen.blit(self.blockunder,self.blockunder_rect)
        for x in range(self.num_of_stair):
            if x%2 == 0:
                self.stair_list[x].draw()
            elif x%2 == 1:
                self.stair_list[x].draw_oppo()
        self.char.draw()
        pygame.display.update()
        clock.tick(60)
        
    def render_gunline(self):
        screen.blit(self.blockunder,self.blockunder_rect)
        for x in range(self.num_of_stair):
            if x%2 == 0:
                self.stair_list[x].draw()
            elif x%2 == 1:
                self.stair_list[x].draw_oppo()
        self.char.draw_gunline()
        self.enemy.draw()
        
    def flip_char(self):
        self.char.gunline_surf_org = pygame.transform.flip(self.char.gunline_surf_org,True,False)
        self.char.gun = pygame.transform.flip(self.char.gun,True,False)
        if self.jump_index % 2 == 0:
            self.char.gun_rect.midleft = self.char.body_rect.center
        elif self.jump_index % 2 == 1:
            self.char.gun_rect.midright = self.char.body_rect.center
    def jump_and_victory(self):
        #set the angle back to zero
        self.char.gun_angle = 0
        #make the char jump
        obj = self.stair_list[self.jump_index]
        if self.jump_index % 2 == 0:
            while self.char.body_rect.left >= obj.rect1[0].right:
                self.char.body_rect.left -= 10 
                self.char.gun_rect = self.char.gun.get_rect(midright = self.char.body_rect.center)
                self.render()
                if self.char.body_rect.left < obj.rect1[0].right: 
                    self.char.body_rect.left = obj.rect1[0].right + 3
                    self.char.gun_rect = self.char.gun.get_rect(midright = self.char.body_rect.center)
                    self.render()
                    break
            for x in range(1,obj.step):
                while self.char.body_rect.left >= obj.rect1[x].right:
                    self.char.body_rect.bottom -= 20
                    self.char.gun_rect = self.char.gun.get_rect(midright = self.char.body_rect.center)
                    self.render()
                    self.char.body_rect.left -= 20
                    self.char.gun_rect = self.char.gun.get_rect(midright= self.char.body_rect.center)
                    self.render()
                    self.blockunder_rect.top += 20
                    self.char.body_rect.bottom += 20
                    self.stair_x_and_y_update()
        elif self.jump_index % 2 == 1:
            while self.char.body_rect.right <= obj.rect1[0].left:
                self.char.body_rect.right += 10
                self.char.gun_rect = self.char.gun.get_rect(midleft = self.char.body_rect.center)
                self.render()
                if self.char.body_rect.right > obj.rect1[0].left:
                    self.char.body_rect.right = obj.rect1[0].left - 3
                    self.char.gun_rect = self.char.gun.get_rect(midleft = self.char.body_rect.center)
                    self.render()
                    break
            for x in range(1,obj.step):
                while self.char.body_rect.right <= obj.rect1[x].left:
                    self.char.body_rect.bottom -= 20
                    self.blockunder_rect.top += 20
                    self.stair_x_and_y_update()
                    self.char.gun_rect = self.char.gun.get_rect(midleft = self.char.body_rect.center)
                    self.render()
                    self.char.body_rect.left += 20
                    self.char.body_rect.bottom += 20
                    self.char.gun_rect = self.char.gun.get_rect(midleft = self.char.body_rect.center)
                    self.render()
        self.flip_char()
        self.enemy_spawn_state = True
        self.jump_index += 1
    def gun_rotate(self):
        if self.jump_index % 2 == 0:
            if self.char.gun_state:
                self.char.gun_angle -= 1
                self.char.gunline_surf = pygame.transform.rotate(self.char.gunline_surf_org,self.char.gun_angle)
                if self.char.gun_angle < -60: self.char.gun_state = False
            else:
                self.char.gun_angle += 1
                self.char.gunline_surf = pygame.transform.rotate(self.char.gunline_surf_org,self.char.gun_angle)
                if self.char.gun_angle > -1: self.char.gun_state = True
            self.char.gunline_rect = self.char.gunline_surf.get_rect(bottomright = self.char.body_rect.midbottom)
        elif self.jump_index % 2 == 1:
            if self.char.gun_state:
                self.char.gun_angle += 1
                self.char.gunline_surf = pygame.transform.rotate(self.char.gunline_surf_org,self.char.gun_angle)
                if self.char.gun_angle > 60: self.char.gun_state = False
            else:
                self.char.gun_angle -= 1
                self.char.gunline_surf = pygame.transform.rotate(self.char.gunline_surf_org,self.char.gun_angle)
                if self.char.gun_angle < 1: self.char.gun_state = True
            self.char.gunline_rect = self.char.gunline_surf.get_rect(bottomleft = self.char.body_rect.midbottom)
    def game_check(self):
        #check wethr if the ammo hit the floor
        rect_list = []
        if self.jump_index % 2 == 0:
            for x in range(self.stair_list[self.jump_index].step):
                rect_list.append(pygame.Rect(0,420-20*(x+1), 200 - 20*x, 20))
        if self.jump_index % 2 == 1:
            for x in range(self.stair_list[self.jump_index].step):
                rect_list.append(pygame.Rect(250+20*x , 420 - 20*(x+1) , 400-(250+20*x),20))
        for y in rect_list:
            if self.char.ammo_rect.colliderect(y):
                return 0
        if self.char.ammo_rect.colliderect(self.enemy.body_rect):
            return 1
        if self.char.ammo_rect.colliderect(self.enemy.head_rect):
            headshot.play()
            return 1
        if self.char.ammo_rect.left > 400 or self.char.ammo_rect.left < 0:
            return 0
        return 2
    def shoot(self):
        org_point = self.char.body_rect.midbottom
        if self.jump_index % 2 == 0:
            radian = math.radians(-self.char.gun_angle)
            start_point = (org_point[0] - 28*math.cos(radian) - 4*math.sin(radian), org_point[1] - 28*math.sin(radian) - 15*math.cos(radian))
            end_point = (start_point[0] - 41*math.cos(radian), start_point[1] - 41*math.sin(radian))
            vector = (start_point[1] - end_point[1] , end_point[0] - start_point[0])
            const = vector[0]*start_point[0] + vector[1]*start_point[1]
            x = start_point[0]
            y = start_point[1]
        elif self.jump_index % 2 == 1:
            radian = math.radians(self.char.gun_angle)
            start_point = (org_point[0] + 28*math.cos(radian) + 4*math.sin(radian), org_point[1] - 28*math.sin(radian) - 15*math.cos(radian))
            end_point = (start_point[0] + 41*math.cos(radian), start_point[1] - 41*math.sin(radian))
            vector = (start_point[1] - end_point[1] , end_point[0] - start_point[0])
            const = vector[0]*start_point[0] + vector[1]*start_point[1]
            x = start_point[0]
            y = start_point[1]
        boom.play()
        while x > -10 and x < 500:
            self.char.ammo_rect.center = (x,y)
            self.render_gunline()
            screen.blit(self.char.ammo, self.char.ammo_rect)
            if self.game_check() == 0:
                global game_layout
                game_layout = 0
                break
            elif self.game_check() == 1:
                break
            pygame.display.update()
            clock.tick(100)
            y -= 10
            x = (const - vector[1]*y) / vector[0]
            
    def spawn_enemy(self):
        if self.jump_index % 2 == 0:
            self.enemy = Enemy(0,self.stair_list[self.jump_index].rect.top)
            while self.enemy.body_rect.right < self.stair_list[self.jump_index].rect1[-1].right - 10:
                self.enemy.body_rect.right += 10
                self.render()
                self.enemy.gun_rect = self.enemy.gun.get_rect(midleft = self.enemy.body_rect.center)
                self.enemy.draw()
                pygame.display.update()
                clock.tick(60)
        else:
            self.enemy = Enemy(400,self.stair_list[self.jump_index].rect.top)
            self.enemy.gun = pygame.transform.flip(self.enemy.gun,True,False)
            while self.enemy.body_rect.left > self.stair_list[self.jump_index].rect1[-1].left + 10:
                self.enemy.body_rect.left -= 10
                self.render()
                self.enemy.gun_rect = self.enemy.gun.get_rect(midright = self.enemy.body_rect.center)
                self.enemy.draw()
                pygame.display.update()
                clock.tick(60)
        self.enemy_spawn_state = False
    def end_game(self):
        if self.jump_index == 18:
            with open('fonts/level.txt','r') as file:
                temp = file.read()
                temp = int(temp)
            with open('fonts/level.txt','w') as file:
                file.write(f'{temp + 1}')
            self.char.gun = pygame.transform.flip(self.char.gun,True,False)
            self.char.gunline_surf = pygame.transform.flip(self.char.gun,True,False)
            while self.char.body_rect.left < 400:
                self.char.body_rect.left += 5
                self.char.gun_rect.left += 5
                self.render()
                global game_layout
                game_layout = 0
maintab = Maintab()
character = Character(200,300)

while True:
    if game_layout == 0:
        maintab.event()
        maintab.draw()
        character.draw()
        pygame.display.update()
        pygame.time.Clock().tick(60)
        a = Ingame()
        a.stair_process()
        a.stair_x_and_y_update()
    elif game_layout == 1:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()
            if event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
                a.shoot()
                a.end_game()
                if game_layout == 0:
                    maintab = Maintab()
                    continue
                a.jump_and_victory()
                
        if a.enemy_spawn_state:
            a.spawn_enemy()   
        a.render_gunline()
        pygame.display.update()
        clock.tick(60)
        a.gun_rotate()

    
