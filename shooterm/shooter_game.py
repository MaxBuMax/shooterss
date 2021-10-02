from pygame import *
from random import randint
from time import time as timer
#фоновая музыка
mixer.init()
mixer.music.load('space.ogg')
mixer.music.play()
fire_sound = mixer.Sound('fire.ogg')
#шрифты и надписи
font.init()
font1 = font.SysFont('Arial', 80)
win = font1.render('!', True, (255, 255, 255))
lose = font1.render('YOU LOSE!', True, (180, 0, 0))
font2 = font.SysFont('Arial', 36)
#нам нужны такие картинки:
img_back = "galaxy.png" #фон игры
img_hero = "rocket.png" #герой
img_bullet = "bullet.png" #пуля
img_enemy = "ufo.png" #враг
img_aster = "asteroid.png"
score = 0 #сбито кораблей
lost = 0 #пропущено кораблей
max_lost = 20 #проиграли, если пропустили столько
goal = 35

num_fire = 0
rel_time = False

#класс-родитель для других спрайтов
class GameSprite(sprite.Sprite):
 #конструктор класса
   def __init__(self, player_image, player_x, player_y, size_x, size_y, player_speed):
       #вызываем конструктор класса (Sprite):
       sprite.Sprite.__init__(self)
       #каждый спрайт должен хранить свойство image - изображение
       self.image = transform.scale(image.load(player_image), (size_x, size_y))
       self.speed = player_speed
       #каждый спрайт должен хранить свойство rect - прямоугольник, в который он вписан
       self.rect = self.image.get_rect()
       self.rect.x = player_x
       self.rect.y = player_y
 #метод, отрисовывающий героя на окне
   def reset(self):
       window.blit(self.image, (self.rect.x, self.rect.y))
#класс главного игрока
class Player(GameSprite):
   #метод для управления спрайтом стрелками клавиатуры
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
 #метод "выстрел" (используем место игрока, чтобы создать там пулю)
   def fire(self):
       bullet = Bullet(img_bullet, self.rect.centerx, self.rect.top, 20, 40, -15)
       bullets.add(bullet)
#класс спрайта-врага  
class Enemy(GameSprite):
   #движение врага
   def update(self):
       self.rect.y += self.speed
       global lost
       #исчезает, если дойдет до края экрана
       if self.rect.y > win_height:
           self.rect.x = randint(80, win_width - 80)
           self.rect.y = 0
           lost = lost + 1

class Aster(GameSprite):
   #движение врага
   def update(self):
       self.rect.y += self.speed
       global lost
       #исчезает, если дойдет до края экрана
       if self.rect.y > win_height:
           self.rect.x = randint(80, win_width - 80)
           self.rect.y = 0















#класс спрайта-пули  
class Bullet(GameSprite):
   #движение врага
   def update(self):
       self.rect.y += self.speed
       #исчезает, если дойдет до края экрана
       if self.rect.y < 0:
           self.kill()
#создаем окошко
win_width = 700
win_height = 500
display.set_caption("StarShooter")
window = display.set_mode((win_width, win_height))
background = transform.scale(image.load(img_back), (win_width, win_height))
#создаем спрайты
ship = Player(img_hero, 5, win_height - 100, 80, 100, 10)
monsters = sprite.Group()
asters = sprite.Group()
for i in range(1, 6):
   monster = Enemy(img_enemy, randint(80, win_width - 80), -40, 80, 50, randint(1, 5))
   monsters.add(monster)

for i in range(1, 3):
   aster = Aster(img_aster, randint(50, win_width - 50), -40, 60, 50, randint(1, 4))
   asters.add(aster)
bullets = sprite.Group()
#переменная "игра закончилась": как только там True, в основном цикле перестают работать спрайты
finish = False
#основной цикл игры:
print("1000-7")
#last_time = timer()
run = True #флаг сбрасывается кнопкой закрытия окна
while run:
   #событие нажатия на кнопку Закрыть
   for e in event.get():
       if e.type == QUIT:
           run = False
       #событие нажатия на пробел - спрайт стреляет
       elif e.type == KEYDOWN:
           if e.key == K_SPACE and rel_time == False:
                if num_fire < 5:
                    fire_sound.play()
                    ship.fire()
                    num_fire += 1
                else:
                    last_time = timer()
                    rel_time = True


   if not finish:
       #обновляем фон
        window.blit(background,(0,0))
        #пишем текст на экране
        text = font2.render("Счет: " + str(score), 1, (255, 255, 255))
        window.blit(text, (10, 20))
        text_lose = font2.render("Пропущено: " + str(lost), 1, (255, 255, 255))
        window.blit(text_lose, (10, 50))



        #производим движения спрайтов
        ship.update()
        monsters.update()
        bullets.update()
        asters.update()

        #обновляем их в новом местоположении при каждой итерации цикла
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
            window.blit(lose, (200, 200))

        if score >= goal:
            finish = True
            window.blit(win, (200,200))

        if rel_time == True:
            now_time = timer()
            if now_time - last_time < 1:
                reload = font2.render("Reload!", 1,(150,0,0))
                window.blit(reload, (190, 460))
            else:
                num_fire = 0
                rel_time = False
        display.update()
       
   #цикл срабатывает каждую 0.05 секунд
   time.delay(50)
