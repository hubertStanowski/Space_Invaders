import pygame
import random

pygame.init()
pygame.mixer.init()

win_width = 600
win_height = 800
win = pygame.display.set_mode((win_width, win_height))
pygame.display.set_caption("Space Invaders")


class Player(object):
    def __init__(self):
        self.img = pygame.image.load("imgs/spaceship.png")
        self.x = win_width//2 - self.img.get_width()/2
        self.y = 710
        self.vel = 5
        self.health = 10
        self.shoot_cd = 60
        self.hitbox = (self.x, self.y,
                       self.img.get_width(), self.img.get_height())
        self.score = 0
        self.visible = True

    def draw(self, surface):
        surface.blit(self.img, (self.x, self.y))
        self.hitbox = (self.x, self.y,
                       self.img.get_width(), self.img.get_height())
       # pygame.draw.rect(surface, (255, 255, 255), self.hitbox, 2)

        pygame.draw.rect(
            surface, (255, 0, 0), (self.hitbox[0], self.hitbox[1]-20, self.hitbox[2], 6))
        if self.health > 0:
            pygame.draw.rect(
                surface, (0, 0, 255), (self.hitbox[0], self.hitbox[1]-20, self.hitbox[2]-7.7*(10-self.health), 6))

    def explode(self, surface):
        player_death = pygame.mixer.Sound("audio/explosion.wav")
        player_death.set_volume(0.35)
        player_death.play()
        player_explosion = Explosion(self.x, self.y)
        for _ in range(5):
            player_explosion.draw(surface)
            pygame.display.update()
            pygame.time.delay(30)


class Enemy(object):
    aliens = [pygame.image.load("imgs/alien1.png"), pygame.image.load("imgs/alien2.png"), pygame.image.load("imgs/alien3.png"),
              pygame.image.load("imgs/alien4.png"), pygame.image.load("imgs/alien5.png")]

    def __init__(self, x, y, health, vel):
        self.img = random.choice(Enemy.aliens)
        self.start_health = health
        self.health = health
        self.visible = True
        self.x = x
        self.y = y
        self.vel = vel
        self.shoot_cd = random.choice([0, 20, 40, 60, 80])
        self.hitbox = (self.x, self.y,
                       self.img.get_width(), self.img.get_height())

    def draw(self, surface):
        surface.blit(self.img, (self.x, self.y))

        self.hitbox = (self.x, self.y,
                       self.img.get_width(), self.img.get_height())
        # pygame.draw.rect(surface, (255, 255, 255), self.hitbox, 2)


class Bullet(object):
    imgs = [pygame.image.load(
        "imgs/bullet.png"), pygame.image.load("imgs/alien_bullet.png")]

    def __init__(self, x, y, facing, alien):
        self.x = x
        self.y = y
        self.facing = facing
        self.vel = 10 * self.facing
        self.alien = alien
        if self.alien == True:
            self.img = Bullet.imgs[1]
        else:
            self.img = Bullet.imgs[0]

    def draw(self, surface):
        surface.blit(self.img, (self.x, self.y))


class Explosion(object):
    imgs = [pygame.image.load("imgs/exp1.png"), pygame.image.load("imgs/exp2.png"), pygame.image.load("imgs/exp3.png"),
            pygame.image.load("imgs/exp4.png"), pygame.image.load("imgs/exp5.png")]

    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.exp_count = 0

    def draw(self, surface):
        if self.exp_count <= 8:
            surface.blit(self.imgs[self.exp_count//2], (self.x, self.y))
            self.exp_count += 1


def draw_window(surface, player, enemies, bullets, enemy_bullets):

    bg = pygame.image.load("imgs/bg.png")
    surface.blit(bg, (0, 0))

    for enemy in enemies:
        enemy.draw(surface)

    for bullet in bullets:
        bullet.draw(surface)

    for bullet in enemy_bullets:
        bullet.draw(surface)

    if player.visible == True:
        player.draw(surface)

    text_mid_screen(surface, 20, ("Score: " + str(player.score)))

    pygame.display.update()


def text_mid_screen(surface, y, text, size=30, bold=True):
    font = pygame.font.SysFont("comicsans", size, bold)
    text = font.render(text, 1, (255, 255, 255))
    x = win_width//2 - text.get_width()/2
    win.blit(text, (x, y))


def max_score():
    with open("highscore.txt", "r") as f:
        lines = f.readlines()
        score = int(lines[0].strip())

        return score


def update_score(new_score):
    score = max_score()

    with open("highscore.txt", "w") as f:
        if score < new_score:
            f.write(str(new_score))
        else:
            f.write(str(score))


def main_menu(surface):
    run = True
    while run:
        win.fill((0, 0, 0))
        text_mid_screen(surface, 100, ("High Score: " +
                                       str(max_score())), 40, False)
        text_mid_screen(surface, win_height/2, "Press Any Key To Play", 60)
        pygame.display.update()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
            if event.type == pygame.KEYDOWN:
                main(surface)

    pygame.quit()


def main(surface):
    run = True
    clock = pygame.time.Clock()
    # spawn_cd = 0
    wave = 1
    player = Player()
    bullets = []
    new_wave = [Enemy(50, random.choice([40, 50, 60]), 1*wave, 0.8),
                Enemy(150, random.choice([40, 50, 60]), 1*wave, 0.8),
                Enemy(250, random.choice([40, 50, 60]), 1*wave, 0.8),
                Enemy(350, random.choice([40, 50, 60]), 1*wave, 0.8),
                Enemy(450, random.choice([40, 50, 60]), 1*wave, 0.8),
                Enemy(550, random.choice([40, 50, 60]), 1*wave, 0.8)]
    enemy_bullets = []
    explosions = []
    enemies = new_wave.copy()

    while(run):
        clock.tick()
        player.shoot_cd += 1
        if len(enemies) == 0:
            wave += 1
            new_wave = [Enemy(50, random.choice([40, 50, 60]), wave, 0.8),
                        Enemy(150, random.choice([40, 50, 60]), wave, 0.8),
                        Enemy(250, random.choice([40, 50, 60]), wave, 0.8),
                        Enemy(350, random.choice([40, 50, 60]), wave, 0.8),
                        Enemy(450, random.choice([40, 50, 60]), wave, 0.8),
                        Enemy(550, random.choice([40, 50, 60]), wave, 0.8)]
            enemies = new_wave.copy()
        # spawn_cd += clock.get_rawtime()
        keys = pygame.key.get_pressed()

        # if spawn_cd / 1000 > 2:
        #   spawn_cd = 0
        #    enemies.append(Enemy(player.x, 100, 1, 0.8))

        if len(enemies) == 0:
            wave += 1
            enemies = new_wave.copy()

        for bullet in bullets:
            for enemy in enemies:
                if (bullet.x + bullet.img.get_width()//2) >= enemy.x + 5 and (bullet.x + bullet.img.get_width()//2) <= enemy.x+player.hitbox[2]:
                    if (bullet.y-bullet.img.get_height()) <= enemy.y+enemy.img.get_height():
                        if enemy.health-1 <= 0:
                            enemy_explosion = pygame.mixer.Sound(
                                "audio/explosion2.wav")
                            enemy_explosion.set_volume(0.20)
                            enemy_explosion.play()
                            enemies.pop(enemies.index(enemy))
                            enemy.visible = False
                            explosions.append(Explosion(enemy.x, enemy.y))
                            player.score += enemy.start_health
                        else:
                            enemy.health -= 1

                        bullets.pop(bullets.index(bullet))
        for bullet in bullets:
            if bullet.y < 0 or bullet.y > win_height:
                bullets.pop(bullets.index(bullet))
            else:
                bullet.y += bullet.vel

        for bullet in enemy_bullets:
            if (bullet.x + bullet.img.get_width()//2) >= player.x + 5 and (bullet.x + bullet.img.get_width()//2) <= player.x+player.hitbox[2]:
                if (bullet.y-bullet.img.get_height()) >= player.y and bullet in enemy_bullets:
                    enemy_bullets.pop(enemy_bullets.index(bullet))
                    player.health -= 1

            if bullet in enemy_bullets and bullet.y < 0 or bullet.y > win_height:
                try:
                    enemy_bullets.pop(enemy_bullets.index(bullet))
                except:
                    continue
            else:
                bullet.y += bullet.vel

        for enemy in enemies:
            if enemy.y >= win_height:
                enemy.visible = False
                enemies.pop(enemies.index(enemy))
                player.score -= enemy.start_health

            if enemy.shoot_cd == 120:
                enemy_shot = pygame.mixer.Sound("audio/laser.wav")
                enemy_shot.set_volume(0.03)
                enemy_shot.play()
                enemy.shoot_cd = 0
                enemy_bullets.append(
                    Bullet(enemy.x+enemy.img.get_width()/2-5, enemy.y+enemy.img.get_height()+5, 1, True))
            else:
                enemy.shoot_cd += 1

            if (enemy.x + enemy.img.get_width()//2) >= player.x + 5 and (enemy.x + enemy.img.get_width()//2) <= player.x+player.hitbox[2]:
                if (enemy.y+enemy.img.get_height()) >= player.y and enemy.visible:
                    player.health -= enemy.health
                    enemy_explosion = pygame.mixer.Sound(
                        "explosion2.wav")
                    enemy_explosion.set_volume(0.20)
                    enemy_explosion.play()
                    explosions.append(Explosion(enemy.x, enemy.y))
                    enemies.pop(enemies.index(enemy))
                    enemy.visible = False

            enemy.y += enemy.vel
    
        for explosion in explosions:
            if explosion.exp_count > 8:
                explosions.pop(explosions.index(explosion))
            else:
                explosion.draw(surface)
                pygame.display.update()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False

        if keys[pygame.K_a] or keys[pygame.K_LEFT]:
            if player.x - player.vel > 0:
                player.x -= player.vel

        if keys[pygame.K_d] or keys[pygame.K_RIGHT]:
            if player.x + player.img.get_width() + player.vel < win_width:
                player.x += player.vel

        if keys[pygame.K_SPACE] or keys[pygame.K_UP]:
            if len(bullets) <= 5 and player.shoot_cd >= 30-(wave-1)*8:
                player_shot = pygame.mixer.Sound("audio/laser.wav")
                player_shot.set_volume(0.15)
                player_shot.play()
                bullets.append(Bullet(player.x+32, player.y - 20, -1, False))
                player.shoot_cd = 0

        draw_window(surface, player, enemies, bullets, enemy_bullets)

        if player.health <= 0:
            player.visible = False
            draw_window(surface, player, enemies, bullets, enemy_bullets)
            player.explode(surface)
            draw_window(surface, player, enemies, bullets, enemy_bullets)
            run = False
            text = "YOU LOST!"
            text_mid_screen(surface, win_height//2, text, 100)
            pygame.display.update()
            pygame.time.delay(2000)

        update_score(player.score)


main_menu(win)
