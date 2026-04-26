import pygame
import random
import os
import sys

# ---------------- INITIALIZATION ----------------
pygame.init()
pygame.mixer.init()

# ---------------- SCREEN SETTINGS ----------------
WIDTH = 400
HEIGHT = 600

screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Practice 11 Racer")

clock = pygame.time.Clock()
FPS = 60

# ---------------- COLORS ----------------
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
GRAY = (80, 80, 80)
RED = (220, 0, 0)
YELLOW = (255, 220, 0)
ORANGE = (255, 140, 0)
PURPLE = (160, 0, 220)

# ---------------- FONTS ----------------
font = pygame.font.SysFont("Verdana", 22)
small_font = pygame.font.SysFont("Verdana", 14)
big_font = pygame.font.SysFont("Verdana", 45)

# ---------------- RESOURCE PATH ----------------
BASE_DIR = os.path.dirname(__file__)
RESOURCE_DIR = os.path.join(BASE_DIR, "resources")


def load_image(filename, size=None):
    """
    Loads image from resources folder.
    If image is missing, returns None, and the game uses drawn fallback shapes.
    """
    path = os.path.join(RESOURCE_DIR, filename)

    try:
        image = pygame.image.load(path).convert_alpha()

        if size is not None:
            image = pygame.transform.scale(image, size)

        return image
    except Exception:
        return None


def load_sound(filename):
    """
    Loads sound from resources folder.
    If sound is missing, returns None.
    """
    path = os.path.join(RESOURCE_DIR, filename)

    try:
        return pygame.mixer.Sound(path)
    except Exception:
        return None


# ---------------- LOAD ASSETS ----------------
road_image = load_image("AnimatedStreet.png", (WIDTH, HEIGHT))
player_image = load_image("Player.png", (50, 90))
enemy_image = load_image("Enemy.png", (50, 90))
coin_image = load_image("coin.png", (35, 35))

crash_sound = load_sound("crash.wav")

# Background music
try:
    background_path = os.path.join(RESOURCE_DIR, "background.wav")
    if os.path.exists(background_path):
        pygame.mixer.music.load(background_path)
        pygame.mixer.music.play(-1)
except Exception:
    pass


class Player(pygame.sprite.Sprite):
    """Player car controlled with left and right arrow keys."""

    def __init__(self):
        super().__init__()

        if player_image:
            self.image = player_image
        else:
            self.image = pygame.Surface((50, 90), pygame.SRCALPHA)
            pygame.draw.rect(self.image, (0, 120, 255), (0, 0, 50, 90), border_radius=8)
            pygame.draw.rect(self.image, BLACK, (0, 0, 50, 90), 2, border_radius=8)

        self.rect = self.image.get_rect()
        self.rect.center = (WIDTH // 2, HEIGHT - 80)
        self.speed = 7

    def update(self):
        keys = pygame.key.get_pressed()

        if keys[pygame.K_LEFT]:
            self.rect.x -= self.speed

        if keys[pygame.K_RIGHT]:
            self.rect.x += self.speed

        # Keep player inside the road area.
        if self.rect.left < 40:
            self.rect.left = 40

        if self.rect.right > WIDTH - 40:
            self.rect.right = WIDTH - 40


class Enemy(pygame.sprite.Sprite):
    """Enemy car moves from top to bottom."""

    def __init__(self):
        super().__init__()

        if enemy_image:
            self.image = enemy_image
        else:
            self.image = pygame.Surface((50, 90), pygame.SRCALPHA)
            pygame.draw.rect(self.image, RED, (0, 0, 50, 90), border_radius=8)
            pygame.draw.rect(self.image, BLACK, (0, 0, 50, 90), 2, border_radius=8)

        self.rect = self.image.get_rect()
        self.speed = 5
        self.reset_position()

    def reset_position(self):
        self.rect.center = (random.randint(80, WIDTH - 80), -100)

    def update(self):
        self.rect.y += self.speed

        if self.rect.top > HEIGHT:
            self.reset_position()


class Coin(pygame.sprite.Sprite):
    """Coin with different weights: 1, 2, or 5."""

    def __init__(self):
        super().__init__()

        # Different coin weights.
        # 1 appears often, 2 appears sometimes, 5 appears rarely.
        self.value = random.choice([1, 1, 1, 2, 2, 5])

        self.image = pygame.Surface((35, 35), pygame.SRCALPHA)

        if coin_image:
            self.image.blit(coin_image, (0, 0))
        else:
            if self.value == 1:
                color = YELLOW
            elif self.value == 2:
                color = ORANGE
            else:
                color = PURPLE

            pygame.draw.circle(self.image, color, (17, 17), 16)
            pygame.draw.circle(self.image, BLACK, (17, 17), 16, 2)

        # Write value on the coin.
        value_text = small_font.render(str(self.value), True, BLACK)
        self.image.blit(value_text, (12, 8))

        self.rect = self.image.get_rect()
        self.speed = 5
        self.reset_position()

    def reset_position(self):
        # Coin appears randomly on the road.
        self.rect.center = (
            random.randint(70, WIDTH - 70),
            random.randint(-600, -50)
        )

    def update(self):
        self.rect.y += self.speed

        if self.rect.top > HEIGHT:
            self.reset_position()


# ---------------- OBJECTS ----------------
player = Player()
enemy = Enemy()

all_sprites = pygame.sprite.Group()
enemy_group = pygame.sprite.Group()
coin_group = pygame.sprite.Group()

all_sprites.add(player)
all_sprites.add(enemy)
enemy_group.add(enemy)

# Create multiple coins.
for _ in range(3):
    coin = Coin()
    coin_group.add(coin)
    all_sprites.add(coin)

# ---------------- GAME VARIABLES ----------------
score = 0
coins_collected = 0

# Enemy speed increases after every N collected coins.
N_COINS_TO_INCREASE_SPEED = 5

road_y = 0
game_over = False


def draw_road():
    """Draw scrolling road background."""
    global road_y

    if road_image:
        screen.blit(road_image, (0, road_y))
        screen.blit(road_image, (0, road_y - HEIGHT))

        road_y += 5

        if road_y >= HEIGHT:
            road_y = 0
    else:
        # Fallback road if image is not found.
        screen.fill((50, 150, 60))
        pygame.draw.rect(screen, GRAY, (50, 0, WIDTH - 100, HEIGHT))

        for y in range(-40, HEIGHT, 80):
            pygame.draw.rect(screen, WHITE, (WIDTH // 2 - 5, y + road_y, 10, 40))

        road_y = (road_y + 5) % 80


def show_hud():
    """Show score, coins, and enemy speed."""
    score_text = font.render(f"Score: {score}", True, BLACK)
    coins_text = font.render(f"Coins: {coins_collected}", True, BLACK)
    speed_text = font.render(f"Enemy speed: {enemy.speed}", True, BLACK)

    screen.blit(score_text, (10, 10))
    screen.blit(coins_text, (10, 40))
    screen.blit(speed_text, (10, 70))


def show_game_over():
    """Show game over screen."""
    screen.fill(BLACK)

    title = big_font.render("GAME OVER", True, RED)
    final_score = font.render(f"Score: {score}", True, WHITE)
    info = font.render("Press ESC to quit", True, WHITE)

    screen.blit(title, title.get_rect(center=(WIDTH // 2, HEIGHT // 2 - 70)))
    screen.blit(final_score, final_score.get_rect(center=(WIDTH // 2, HEIGHT // 2)))
    screen.blit(info, info.get_rect(center=(WIDTH // 2, HEIGHT // 2 + 50)))


# ---------------- MAIN LOOP ----------------
running = True

while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                running = False

    if not game_over:
        player.update()
        enemy.update()
        coin_group.update()

        # Collision with enemy ends the game.
        if pygame.sprite.spritecollideany(player, enemy_group):
            if crash_sound:
                crash_sound.play()

            pygame.mixer.music.stop()
            game_over = True

        # Collect coins.
        collected = pygame.sprite.spritecollide(player, coin_group, False)

        for coin in collected:
            score += coin.value
            coins_collected += 1
            coin.reset_position()

            # Increase enemy speed after earning N coins.
            if coins_collected % N_COINS_TO_INCREASE_SPEED == 0:
                enemy.speed += 1

        draw_road()
        all_sprites.draw(screen)
        show_hud()
    else:
        show_game_over()

    pygame.display.flip()
    clock.tick(FPS)

pygame.quit()
sys.exit()
