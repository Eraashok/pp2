import pygame
import sys
import random
import time
import os
from pygame.locals import *

pygame.init()

# -------------------- SETTINGS --------------------
WIDTH = 400
HEIGHT = 600
FPS = 60

WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
GOLD = (255, 215, 0)

SPEED = 5
SCORE = 0
COINS = 0

screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Racer")
clock = pygame.time.Clock()

font_small = pygame.font.SysFont("Verdana", 20)
font_big = pygame.font.SysFont("Verdana", 50)

# -------------------- RESOURCE PATHS --------------------
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
RESOURCES_DIR = os.path.join(BASE_DIR, "resources")

background_path = os.path.join(RESOURCES_DIR, "AnimatedStreet.png")
player_path = os.path.join(RESOURCES_DIR, "Player.png")
enemy_path = os.path.join(RESOURCES_DIR, "Enemy.png")
crash_sound_path = os.path.join(RESOURCES_DIR, "crash.wav")

# -------------------- LOAD FILES --------------------
background = pygame.image.load(background_path)
player_img = pygame.image.load(player_path)
enemy_img = pygame.image.load(enemy_path)

# -------------------- CLASSES --------------------
class Enemy(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = enemy_img
        self.rect = self.image.get_rect()
        self.reset_position()

    def reset_position(self):
        # Enemy screen-нің үстінен random жерде пайда болады
        self.rect.center = (random.randint(40, WIDTH - 40), -50)

    def move(self):
        global SCORE
        self.rect.move_ip(0, SPEED)

        # Enemy экраннан шығып кетсе, қайтадан жоғары шығады
        if self.rect.top > HEIGHT:
            SCORE += 1
            self.reset_position()


class Player(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = player_img
        self.rect = self.image.get_rect()
        self.rect.center = (160, 520)

    def move(self):
        pressed_keys = pygame.key.get_pressed()

        # Солға жүру
        if pressed_keys[K_LEFT] and self.rect.left > 0:
            self.rect.move_ip(-5, 0)

        # Оңға жүру
        if pressed_keys[K_RIGHT] and self.rect.right < WIDTH:
            self.rect.move_ip(5, 0)


class Coin(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()

        # Егер coin суреті жоқ болса, өзіміз алтын түсті дөңгелек жасаймыз
        self.image = pygame.Surface((24, 24), pygame.SRCALPHA)
        pygame.draw.circle(self.image, GOLD, (12, 12), 10)
        pygame.draw.circle(self.image, BLACK, (12, 12), 10, 2)

        self.rect = self.image.get_rect()
        self.speed = 4
        self.reset_position()

    def reset_position(self):
        # Coin жолдың ішінде random жерде пайда болады
        self.rect.center = (
            random.randint(40, WIDTH - 40),
            random.randint(-300, -50)
        )

    def move(self):
        self.rect.move_ip(0, self.speed)

        # Экраннан түсіп кетсе, қайтадан жоғарыға шығады
        if self.rect.top > HEIGHT:
            self.reset_position()


# -------------------- CREATE OBJECTS --------------------
player = Player()
enemy = Enemy()
coin = Coin()

enemies = pygame.sprite.Group()
enemies.add(enemy)

coins_group = pygame.sprite.Group()
coins_group.add(coin)

all_sprites = pygame.sprite.Group()
all_sprites.add(player)
all_sprites.add(enemy)
all_sprites.add(coin)

# -------------------- SPEED EVENT --------------------
INC_SPEED = pygame.USEREVENT + 1
pygame.time.set_timer(INC_SPEED, 1500)

# -------------------- GAME LOOP --------------------
while True:
    for event in pygame.event.get():
        if event.type == QUIT:
            pygame.quit()
            sys.exit()

        # Әр 1.5 секунд сайын жылдамдық өседі
        if event.type == INC_SPEED:
            SPEED += 0.3

    # Background шығару
    screen.blit(background, (0, 0))

    # Score сол жақ жоғарыда
    score_text = font_small.render(f"Score: {SCORE}", True, BLACK)
    screen.blit(score_text, (10, 10))

    # Coins саны оң жақ жоғарыда
    coins_text = font_small.render(f"Coins: {COINS}", True, BLACK)
    coins_rect = coins_text.get_rect(topright=(WIDTH - 10, 10))
    screen.blit(coins_text, coins_rect)

    # Барлық sprite-тарды шығару және қозғалысын жаңарту
    for entity in all_sprites:
        screen.blit(entity.image, entity.rect)
        entity.move()

    # Player enemy-ге тисе game over
    if pygame.sprite.spritecollideany(player, enemies):
        # Егер дыбыс файлы бар болса, соны ойнатамыз
        if os.path.exists(crash_sound_path):
            try:
                pygame.mixer.Sound(crash_sound_path).play()
                time.sleep(0.5)
            except:
                pass

        game_over_text = font_big.render("Game Over", True, BLACK)
        screen.fill(RED)
        screen.blit(game_over_text, (70, 250))
        pygame.display.update()
        time.sleep(2)
        pygame.quit()
        sys.exit()

    # Player coin-ға тисе coin саны өседі
    if pygame.sprite.spritecollideany(player, coins_group):
        COINS += 1
        coin.reset_position()

    pygame.display.update()
    clock.tick(FPS)