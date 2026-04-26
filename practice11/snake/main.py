import pygame
import random
import sys

# ---------------- INITIALIZATION ----------------
pygame.init()

# ---------------- SCREEN SETTINGS ----------------
WIDTH = 600
HEIGHT = 600
CELL_SIZE = 20

COLS = WIDTH // CELL_SIZE
ROWS = HEIGHT // CELL_SIZE

screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Practice 11 Snake")

clock = pygame.time.Clock()

# ---------------- COLORS ----------------
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
GREEN = (0, 200, 0)
DARK_GREEN = (0, 120, 0)
RED = (220, 0, 0)
ORANGE = (255, 140, 0)
PURPLE = (160, 0, 220)

# ---------------- FONTS ----------------
font = pygame.font.SysFont("Verdana", 22)
small_font = pygame.font.SysFont("Verdana", 14)
big_font = pygame.font.SysFont("Verdana", 45)

# ---------------- GAME VARIABLES ----------------
snake = [(10, 10), (9, 10), (8, 10)]
direction = (1, 0)
next_direction = (1, 0)

score = 0
level = 1
speed = 8

foods_eaten = 0
FOODS_FOR_NEXT_LEVEL = 4

# Food disappears after 5 seconds.
FOOD_LIFETIME = 5000

food = None
game_over = False


def random_food_position():
    """Generate random food position that does not overlap with snake."""
    while True:
        pos = (random.randint(0, COLS - 1), random.randint(0, ROWS - 1))

        if pos not in snake:
            return pos


def spawn_food():
    """Create food with random weight and timer."""
    value = random.choice([1, 1, 1, 2, 2, 5])

    if value == 1:
        color = RED
    elif value == 2:
        color = ORANGE
    else:
        color = PURPLE

    return {
        "pos": random_food_position(),
        "value": value,
        "color": color,
        "spawn_time": pygame.time.get_ticks()
    }


def draw_cell(pos, color):
    """Draw one grid cell."""
    x, y = pos

    rect = pygame.Rect(
        x * CELL_SIZE,
        y * CELL_SIZE,
        CELL_SIZE,
        CELL_SIZE
    )

    pygame.draw.rect(screen, color, rect)
    pygame.draw.rect(screen, BLACK, rect, 1)


def draw_game():
    """Draw all game objects."""
    screen.fill(WHITE)

    # Draw food.
    draw_cell(food["pos"], food["color"])

    food_x = food["pos"][0] * CELL_SIZE + 5
    food_y = food["pos"][1] * CELL_SIZE

    value_text = small_font.render(str(food["value"]), True, WHITE)
    screen.blit(value_text, (food_x, food_y))

    # Draw snake.
    for i, segment in enumerate(snake):
        if i == 0:
            draw_cell(segment, DARK_GREEN)
        else:
            draw_cell(segment, GREEN)

    # Draw score information.
    score_text = font.render(f"Score: {score}", True, BLACK)
    level_text = font.render(f"Level: {level}", True, BLACK)
    speed_text = font.render(f"Speed: {speed}", True, BLACK)

    screen.blit(score_text, (10, 10))
    screen.blit(level_text, (10, 40))
    screen.blit(speed_text, (10, 70))


def show_game_over():
    """Show final screen."""
    screen.fill(BLACK)

    title = big_font.render("GAME OVER", True, RED)
    score_text = font.render(f"Score: {score}", True, WHITE)
    level_text = font.render(f"Level: {level}", True, WHITE)
    info = font.render("Press ESC to quit", True, WHITE)

    screen.blit(title, title.get_rect(center=(WIDTH // 2, HEIGHT // 2 - 80)))
    screen.blit(score_text, score_text.get_rect(center=(WIDTH // 2, HEIGHT // 2 - 20)))
    screen.blit(level_text, level_text.get_rect(center=(WIDTH // 2, HEIGHT // 2 + 20)))
    screen.blit(info, info.get_rect(center=(WIDTH // 2, HEIGHT // 2 + 70)))


def handle_input(event):
    """Change direction with arrow keys."""
    global next_direction

    if event.type == pygame.KEYDOWN:
        if event.key == pygame.K_UP and direction != (0, 1):
            next_direction = (0, -1)

        elif event.key == pygame.K_DOWN and direction != (0, -1):
            next_direction = (0, 1)

        elif event.key == pygame.K_LEFT and direction != (1, 0):
            next_direction = (-1, 0)

        elif event.key == pygame.K_RIGHT and direction != (-1, 0):
            next_direction = (1, 0)


def move_snake():
    """Move snake, check food and collisions."""
    global direction, score, food, game_over, level, speed, foods_eaten

    direction = next_direction

    head_x, head_y = snake[0]
    dx, dy = direction

    new_head = (head_x + dx, head_y + dy)

    # Wall collision.
    if new_head[0] < 0 or new_head[0] >= COLS or new_head[1] < 0 or new_head[1] >= ROWS:
        game_over = True
        return

    # Self collision.
    if new_head in snake:
        game_over = True
        return

    # Add new head.
    snake.insert(0, new_head)

    # If snake eats food, score increases and snake grows.
    if new_head == food["pos"]:
        score += food["value"] * 10
        foods_eaten += 1

        # Increase level and speed after every N foods.
        if foods_eaten % FOODS_FOR_NEXT_LEVEL == 0:
            level += 1
            speed += 2

        food = spawn_food()
    else:
        # If food is not eaten, remove tail.
        snake.pop()


# First food.
food = spawn_food()

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
            handle_input(event)

    if not game_over:
        # If food stayed too long, it disappears and respawns.
        now = pygame.time.get_ticks()

        if now - food["spawn_time"] > FOOD_LIFETIME:
            food = spawn_food()

        move_snake()
        draw_game()
    else:
        show_game_over()

    pygame.display.flip()
    clock.tick(speed)

pygame.quit()
sys.exit()
