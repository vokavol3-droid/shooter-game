from random import randint
from pygame import *
from time import time as timer

class GameSprite(sprite.Sprite):
    def __init__(self, player_image, player_x, player_y, player_speed, w, h):
        super().__init__()
        self.image = transform.scale(image.load(player_image), (w, h))
        self.speed = player_speed
        self.rect = self.image.get_rect()
        self.rect.x = player_x
        self.rect.y = player_y

    def reset(self):
        window.blit(self.image, (self.rect.x, self.rect.y))

class Player(GameSprite):
    def update(self):
        keys = key.get_pressed()

        if keys[K_LEFT] and self.rect.x > 0:
            self.rect.x -= self.speed

        if keys[K_RIGHT] and self.rect.x < 635:
            self.rect.x += self.speed

    def fire(self):
        bullet = Bullet('bullet.png', self.rect.centerx-10, self.rect.y,-15, 20,20)
        bullets.add(bullet)
        
bullets = sprite.Group()
lost = 0

class Enemy(GameSprite):
    def __init__(self, player_image, player_x, player_y, player_speed, w, h):
        super().__init__(player_image, player_x, player_y, player_speed, w, h)
    
    def update(self):
        global lost
        self.rect.y += self.speed
        if self.rect.y >= 490:  
            self.rect.x = randint(5, 495)
            self.rect.y = 0
            lost += 1

class Asteroid(GameSprite):
    def update(self):
        self.rect.y += self.speed
        if self.rect.y >= 490:  
            self.rect.x = randint(5, 495)
            self.rect.y = 0


class Bullet(GameSprite):
    def update(self):
        self.rect.y += self.speed
        if self.rect.y < 0:
            self.kill()

init()
FPS = 60
clock = time.Clock()

font.init()
font1 = font.Font(None, 36)

font2 = font.Font(None, 36)


font3 = font.Font(None, 36)

font4 = font.Font(None, 36)


font5 = font.Font(None, 36)


mixer.init()
mixer.music.load('space.ogg')
mixer.music.set_volume(0.1)
mixer.music.play()
bam = mixer.Sound('fire.ogg')
bam.set_volume(0.3)

window = display.set_mode((700, 500))
display.set_caption('Space')

background = transform.scale(image.load('galaxy.jpg'), (700, 500))
player = Player('rocket.png', 250, 390, 4, 80, 100)

lives = 5
heart_img = transform.scale(image.load('heart.png'), (40, 40))

def create_monsters(count=5):
    monster_list = []
    for i in range(count):
        monster = Enemy('ufo.png', randint(5, 495), randint(0, 100), randint(1, 3), 80, 70)
        monster_list.append(monster)
    return monster_list

monsters = sprite.Group()
for i in range(5):
    monster = Enemy('ufo.png', randint(5, 495), randint(0, 100), randint(1, 3), 80, 70)
    monsters.add(monster)

asteroids = sprite.Group()
for i in range(2):
    asteroid = Asteroid('asteroid.png', randint(5, 495), randint(0, 100), randint(1, 2), 60, 50)
    asteroids.add(asteroid)

game = True
count = 0
finish = False 
num_fire=0 
rel_time = False


while game:
    for e in event.get():
        if e.type == QUIT:
            game = False
        elif e.type == KEYDOWN:
            if e.key == K_SPACE and not finish:
                
                if num_fire<5 and rel_time == False:
                    num_fire+=1
                    bam.play()
                    player.fire()

                if num_fire>=5 and rel_time == False:
                    last_time = timer()
                    rel_time = True


    if not finish:
        window.blit(background, (0, 0))
        spr_list = sprite.groupcollide(monsters, bullets, True, True)

        if sprite.spritecollide(player, monsters, True):
            lives-=1
            monster = Enemy('ufo.png', randint(5, 495), randint(0, 100), randint(1, 3), 80, 70)
            monsters.add(monster)

    
        if sprite.spritecollide(player, asteroids, True):
            lives-=1
            asteroid = Asteroid('asteroid.png', randint(5, 495), randint(0, 100), randint(1, 2), 60, 50)
            asteroids.add(asteroid)

        x = 650
        for i in range(lives):
            window.blit(heart_img, (x, 10))
            x-=45

        if rel_time == True:
            now_time = timer()

            if now_time-last_time<2:
                reload = font5.render('Перезагрузка..', 1, (150, 0,0))
                window.blit(reload, (260, 240))
            else:
                num_fire=0 
                rel_time = False
 

        for monster in spr_list: 
            count += 1
            new_monster = Enemy('ufo.png', randint(5, 495), randint(0, 100), randint(1, 3), 80, 70)
            monsters.add(new_monster)

        if lost >= 5:
            finish = True
            losetxt = font4.render('ПРОИГРЫШ!', True, (255, 0, 0))
        
        if count >= 10:
            finish = True
            wintxt = font3.render('ПОБЕДА!', True, (0, 255, 0))

        player.update()
        monsters.update()
        bullets.update()
        asteroids.update()

    
    
    lose_text = font1.render('Пропущено: ' + str(lost), True, (255, 255, 255))
    window.blit(lose_text, (5, 50))

    win_text = font1.render('Счет: ' + str(count), True, (255, 255, 255))
    window.blit(win_text, (5, 5))

    if finish:
        if count >= 10:
            window.blit(wintxt, (250, 200))
        else:
            window.blit(losetxt, (250, 200))

    player.reset()
    monsters.draw(window)
    bullets.draw(window)
    asteroids.draw(window)
    
    display.update()
    clock.tick(FPS) 