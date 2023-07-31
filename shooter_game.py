from pygame import *
from random import randint
from time import time as timer
from oc import *

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
    def fire(self):
        bullet = Bullet('bullet.png', self.rect.centerx,self.rect.top, 15,20,-15)
        bullets.add(bullet)

goal = 10
score = 0
max_lost = 3
lost = 0
class Enemy(GameSprite):
    def update(self):
        global lost
        self.rect.y += self.speed
        if self.rect.y > win_height:
            self.rect.x = randint(80, win_height - 80) 
            self.rect.y = 0
            lost = lost + 1

class Bullet(GameSprite):
    def update(self):
        self.rect.y += self.speed
        if self.rect.y <0:
            self.kill()

mixer.init()
mixer.music.load('space.ogg')
mixer.music.play()

fire_sound = mixer.Sound('fire.ogg')


font.init()
font1 = font.Font(None, 80)     
win = font1.render('YOU WIN!', True, (255, 255, 255))
lose = font1.render('YOU LOSE!', True, (180, 0, 0))
font2 = font.Font(None, 36)

win_width = 700
win_height = 500
window = display.set_mode((win_width, win_height))
display.set_caption("shooter_game.py")
background = transform.scale(image.load("galaxy.jpg"), (win_width, win_height))

rocket = Player('rocket.png',5,420,80,100,10)

monsters  = sprite.Group()
for i in range (1, 6):
    monster = Enemy('ufo.png',randint(80, win_height - 80), -40,80,50, randint(1, 5) )
    monsters.add(monster)

bullets = sprite.Group()
    

meteorites  = sprite.Group()
for i in range (1, 6):   
    meteorite = Enemy('asteroid.png',randint(30, win_height - 80), -40,80,50, randint(1, 5) )
    meteorites.add(meteorite)


finish = False
game = True
clock = time.Clock()
FPS = 60
num_fire = 0
rel_time = False

while game:
    for e in event.get():
        if e.type == QUIT:
            game = False
        elif e.type == KEYDOWN:
            if e.key == K_SPACE:
                fire_sound.play()
                rocket.fire()
        if num_fire<5 and rel_time == False:
            num_fire=num_fire+1
            fire_sound.play()
        if num_fire>5 and rel_time == False:
            last_time = timer()
            rel_time = True
    if not finish:
        window.blit(background,(0,0))
        rocket.update()
        rocket.reset()
        bullets.update()
        bullets.draw(window)
        monsters.update()
        monsters.draw(window)
        collides = sprite.groupcollide(monsters, bullets, True, True)
        for c in collides:
            score = score + 1
            monster = Enemy('ufo.png',randint(80, win_height - 80), -40,80,50, randint(1, 5) )
            monsters.add(monster)
        
        if rel_time == True:
            now_time = timer()
            if now_time - last_time<3:
                reload = font2.render('Перезарядка', 1,(150,0,0))
                window.blit(reload,(260,460))
            else:
                num_fire = 0   
                rel_time = False      

        if sprite.spritecollide(rocket, monsters,False) or lost >= max_lost:
            finish = True
            window.blit(lose,(200,200))
        if score  >= goal:
            finish = True
            window.blit(win,(200,200))
        text = font2.render('Счет'+ str(score), 1,(255,255,255))
        window.blit(text,(10,20))
        text_lose = font2.render('Пропущено'+ str(lost), 1,(255,255,255))
        window.blit(text_lose,(10,50))
        display.update()
    else:
        finish = False
        score = 0
        lost = 0
        for d in bullets:
            d.kill()
        for m in monsters:
            m.kill()
        for a in meteorites:
            a.kill()
        time.delay(3000)
        for i in range(1, 6):
            monster = Enemy('ufo.png',randint(80, win_height - 80), -40,80,50, randint(1, 5) )
            monsters.add(monster)

        for i in range (1, 6):   
            meteorite = Enemy('asteroid.png',randint(30, win_height - 80), -40,80,50, randint(1, 5) )
            meteorite.add(meteorite)

    time.delay(50)
 
 #!The end

