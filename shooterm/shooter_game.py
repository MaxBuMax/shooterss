from pygame import *
from random import randint
from time import time as timer
import os
mixer.init()
mixer.music.load('space.ogg')
mixer.music.play()
fire_sound = mixer.Sound('fire.ogg')
font.init()
font1 = font.SysFont('Arial', 80)
win = font1.render('ПОБЕДА!', True, (255, 255, 255))
lose = font1.render(':(', True, (205, 35, 20))
font2 = font.SysFont('Arial', 30)
font3 = font.SysFont('Arial', 50)
mixfnt = font3.render("glhf", True, (100, 100, 100))
img_back = "galaxy.png" 
img_hero = "rocket.png"
img_bullet = "bullet.png" 
img_enemy = "ufo.png" 
img_aster = "asteroid.png"
img_hero2 = "rocket2.png"
score = 0 
lost = 0 
max_lost = 20 
goal = 25

num_fire = 0
rel_time = False
def pause(window):
    run = True
    font1 = font.Font(None, 35)
    while run:
        for e in event.get():
            if e.type == KEYDOWN:
                if e.key == K_p:
                    run = False

class GameSprite(sprite.Sprite):

   def __init__(self, player_image, player_x, player_y, size_x, size_y, player_speed):
       sprite.Sprite.__init__(self)
       self.image = transform.scale(image.load(player_image), (size_x, size_y))
       self.speed = player_speed
       self.rect = self.image.get_rect()
       self.rect.x = player_x
       self.rect.y = player_y

   def reset(self):
       window.blit(self.image, (self.rect.x, self.rect.y))

class Player(GameSprite):

   def update(self):
        keys = key.get_pressed()
        if keys[K_LEFT] and self.rect.x > 5:
           self.rect.x -= self.speed
        if keys[K_RIGHT] and self.rect.x < win_width - 80:
           self.rect.x += self.speed
        if keys[K_UP] and self.rect.y > 5:
           self.rect.y -= self.speed
        if keys[K_DOWN] and self.rect.y < win_height - 80:
           self.rect.y += self.speed

  
        keys = key.get_pressed()
        if keys[K_a] and self.rect.x > 5:
           self.rect.x -= self.speed
        if keys[K_d] and self.rect.x < win_width - 80:
           self.rect.x += self.speed
        if keys[K_w] and self.rect.y > 5:
           self.rect.y -= self.speed
        if keys[K_s] and self.rect.y < win_height - 80:
           self.rect.y += self.speed











   def fire(self):
       bullet = Bullet(img_bullet, self.rect.centerx, self.rect.top, 60, 40, -15)
       bullets.add(bullet)

class Enemy(GameSprite):
   def update(self):
       self.rect.y += self.speed
       global lost
       if self.rect.y > win_height:
           self.rect.x = randint(80, win_width - 80)
           self.rect.y = 0
           lost = lost + 1













class Aster(GameSprite):
   def update(self):
       self.rect.y += self.speed
       global lost
       if self.rect.y > win_height:
           self.rect.x = randint(30, win_width - 80)
           self.rect.y = 0
















class Bullet(GameSprite):
   def update(self):
       self.rect.y += self.speed
       if self.rect.y < 0:
           self.kill()
win_width = 1000
win_height = 600
display.set_caption("StarShooter")
window = display.set_mode((win_width, win_height))
background = transform.scale(image.load(img_back), (win_width, win_height))
ship = Player(img_hero, 5, win_height - 100, 115, 100, 10)
monsters = sprite.Group()

asters = sprite.Group()
for i in range(1, 6):
   monster = Enemy(img_enemy, randint(12, win_width - 80), -200, 100, 50, randint(1, 6))
   monsters.add(monster)





for i in range(1, 3):
   aster = Aster(img_aster, randint(250, win_width - 50), -40, 90, 50, randint(1, 4))
   asters.add(aster)
bullets = sprite.Group()
finish = False
run = True 
while run:
    for e in event.get():
        if e.type == QUIT:
            run = False
        if e.type == KEYDOWN:
            if e.key == K_p:
                pause(window)
            
        elif e.type == KEYUP:
            if e.key == K_SPACE and rel_time == False:
                    if num_fire < 5:
                        fire_sound.play()
                        ship.fire()
                        num_fire += 1
                    else:
                        last_time = timer()
                        rel_time = True

    if not finish:
            window.blit(background,(0,0))
            text = font2.render("Счет: " + str(score), 1, (100, 100, 200))
            window.blit(text, (30, 30))
            text_lose = font2.render("Пропущено: " + str(lost), 1, (100, 100, 00))
            window.blit(text_lose, (10, 65))
            window.blit(mixfnt, (10, 200))


            ship.update()
            monsters.update()
            bullets.update()
            asters.update()
            ship.reset()
            monsters.draw(window)
            bullets.draw(window)
            asters.draw(window)
            
            collides = sprite.groupcollide(monsters, bullets, True, True)
            collides1 = sprite.groupcollide(asters, bullets, False, True)
            
            for c in collides:
                score += 1
                monster = Enemy(img_enemy, randint(80, win_width - 80), -40, 80, 50, randint(1, 5))
                monsters.add(monster)
            if lost == max_lost:
                finish = True
                window.blit(lose, (200, 200))

            if sprite.spritecollide(ship, monsters, False):
                finish = True
                window.blit(lose, (200, 200))
            
            if sprite.spritecollide(ship, asters, False):
                finish = True
                window.blit(lose, (400, 400))

            if score >= goal:
                finish = True
                window.blit(win, (400,400))

            if rel_time == True:
                now_time = timer()
                if now_time - last_time < 1:
                    reload = font2.render("Reload", 1,(150,0,0))
                    window.blit(reload, (190, 460))
                else:
                    num_fire = 0
                    rel_time = False
            
            display.update()
            
    time.delay(50)
