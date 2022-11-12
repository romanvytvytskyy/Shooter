from pygame import *
from random import randint
from time import time as timer
# Music
mixer.init()
mixer.music.load("space.ogg")
mixer.music.play()
fire_sound = mixer.Sound('fire.ogg')
lost_sound = mixer.Sound('lost.ogg')

# Images
img_back = "galaxy.jpg"
img_hero = "rocket.png"
img_enemy = "ufo.png"
img_bullet = "bullet.png"
img_ast = "asteroid.png"
width, height = 700, 500
mw = display.set_mode((width, height))
display.set_caption("Shooter")
background = transform.scale(image.load(img_back), (width, height))
lost = 0

# Text
font.init()
text = font.SysFont("Arial", 36)
text1 = font.SysFont("Arial", 80)
win = text1.render("YOU WIN!", True, (0, 255, 0))
lose = text1.render("ENEMIES WIN!", True, (255, 0, 0))

# Classes


class GameSprite(sprite.Sprite):
    def __init__(self, player_image, player_x, player_y, size_x, size_y, speed):
        sprite.Sprite.__init__(self)

        self.image = transform.scale(
            image.load(player_image), (size_x, size_y))
        self.speed = speed
        self.rect = self.image.get_rect()
        self.rect.x = player_x
        self.rect.y = player_y

    def reset(self):
        mw.blit(self.image, (self.rect.x, self.rect.y))


class Player(GameSprite):
    def updete(self):
        keys = key.get_pressed()
        if keys[K_a] and self.rect.x > 5:
            self.rect.x -= self.speed

        if keys[K_d] and self.rect.x < width - 80:
            self.rect.x += self.speed

    def fire(self):
        bullet = Bullet(img_bullet, self.rect.centerx,
                        self.rect.top, 15, 20, 15)
        bullets.add(bullet)


class Enemy(GameSprite):
    def update(self):
        global lost
        self.rect.y += self.speed
        if self.rect.y > height:
            self.rect.x = randint(80, width-160)
            self.rect.y = 0
            lost += 1
            lost_sound.play()


class Bullet(GameSprite):
    def update(self):
        self.rect.y -= self.speed
        if self.rect.y < 0:
            self.kill()


class Button():
    def __init__(self, color, text, x, y, width, height, fsize, txt_color):
        self.color = color
        self.width = width
        self.height = height
        self.image = Surface([self.width, self.height])
        self.image.fill((color))
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        self.fsize = fsize
        self.text = text
        self.txt_color = txt_color
        self.txt_image = font.SysFont(
            "Arial", fsize).render(text, True, txt_color)

    def draw(self, s_x, s_y):
        mw.blit(self.image, (self.rect.x, self.rect.y))
        mw.blit(self.txt_image, (self.rect.x+s_x, self.rect.y + s_y))


ship = Player(img_hero, 300, height - 100, 80, 100, 10)
monsters = sprite.Group()
asteroids = sprite.Group()
btn_play = Button((178, 35, 35), "PLAY", 250, 150,
                  200, 70, 50, (255, 255, 255))
btn_exit = Button((178, 35, 35), "EXIT", 250, 250,
                  200, 70, 50, (255, 255, 255))


def create_enemies():
    for i in range(1, 6):
        monster = Enemy(img_enemy, randint(
            80, width-160), -40, 80, 50, randint(1, 5))
        monsters.add(monster)
    # Реалізувати групу астероїдів
    for i in range(1, 3):
        asteroid = Enemy(img_ast, randint(80, width-160), -
                         40, 80, 50, randint(1, 7))
        asteroids.add(asteroid)


create_enemies()


def menu():
    # mixer.music.load("menu.ogg")
    # mixer.music.play()
    name = text.render("Star Track", True, (255, 255, 255))
    menu = True
    while menu:
        pos_x, pos_y = mouse.get_pos()
        for e in event.get():
            if e.type == QUIT:
                menu = False
            if btn_play.rect.collidepoint((pos_x, pos_y)) and e.type == MOUSEBUTTONDOWN:
                menu = False
                # mixer.music.stop()
                game()
            if btn_exit.rect.collidepoint((pos_x, pos_y)) and e.type == MOUSEBUTTONDOWN:
                menu = False
        mw.blit(background, (0, 0))
        mw.blit(name, (300, 50))
        btn_play.draw(50, 10)
        btn_exit.draw(50, 10)

        display.update()
        time.delay(40)


def game():
    global lost, score, bullets
    run = True
    finish = False
    bullets = sprite.Group()
    score = 0
    goal = 10
    rel_time = False
    num_fire = 0
    life = 3

    while run:
        for e in event.get():
            if e.type == QUIT:
                run = False
            elif e.type == KEYDOWN:
                if e.key == K_SPACE:
                    if num_fire < 5 and rel_time == False:
                        num_fire = num_fire + 1
                        ship.fire()
                        fire_sound.play()
                    if num_fire >= 5 and rel_time == False:
                        last_time = timer()
                        rel_time = True

        if not finish:
            mw.blit(background, (0, 0))
            text_score = text.render(
                "Рахунок: " + str(score), 1, (255, 255, 255))
            mw.blit(text_score, (10, 20))
            text_lost = text.render(
                "Пропущено: " + str(lost), 1, (255, 255, 255))
            mw.blit(text_lost, (10, 50))
            ship.updete()
            ship.reset()
            # TODO автоматичне переміщення астероїда
            monsters.update()
            monsters.draw(mw)

            asteroids.update()
            asteroids.draw(mw)

            bullets.update()
            bullets.draw(mw)

            if rel_time:
                now_time = timer()
                if now_time - last_time < 3:
                    reload = text.render("Reloading...", 1, (255, 255, 0))
                    mw.blit(reload, (250, 450))
                else:
                    num_fire = 0
                    rel_time = False

            collides = sprite.groupcollide(monsters, bullets, True, True)
            for collide in collides:
                score += 1
                monster = Enemy(img_enemy, randint(
                    80, width-160), -40, 80, 50, randint(1, 5))
                monsters.add(monster)

            if sprite.spritecollide(ship, monsters,
                                    False) or sprite.spritecollide(ship, asteroids, False):
                sprite.spritecollide(ship, asteroids, True)
                sprite.spritecollide(ship, asteroids, True)
                life -= 1

            if life == 0 or lost >= 10:
                finish = True
                mw.blit(lose, (200, 200))

            if life == 3:
                life_color = (0, 150, 0)
            if life == 2:
                life_color = (150, 150, 0)
            if life == 1:
                life_color = (150, 0, 0)

            text_life = text1.render(str(life), 1, life_color)
            mw.blit(text_life, (650, 10))

            if score >= goal:
                finish = True
                mw.blit(win, (200, 200))

            display.update()
        else:
            finish = False
            score = 0
            lost = 0
            num_fire = 0
            life = 3
            for bullet in bullets:
                bullet.kill()
            for monster in monsters:
                monster.kill()
            for asteroid in asteroids:
                asteroid.kill()
            menu()
            time.delay(3000)
            create_enemies()

            display.update()

        time.delay(50)


menu()
