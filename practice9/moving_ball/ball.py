import pygame

pygame.init()

WIDTH = 800
HEIGHT = 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Ball")
WHITE = (255, 255, 255)
RED = (255, 0, 0)
x = WIDTH // 2
y = HEIGHT // 2
radius = 25
step = 20

clock = pygame.time.Clock()
running = True

while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    keys = pygame.key.get_pressed()

    if keys[pygame.K_UP] and y - step - radius >= 0:
        y -= step
    if keys[pygame.K_DOWN] and y + step + radius <= HEIGHT:
        y += step
    if keys[pygame.K_LEFT] and x - step - radius >= 0:
        x -= step
    if keys[pygame.K_RIGHT] and x + step + radius <= WIDTH:
        x += step

    screen.fill(WHITE)
    pygame.draw.circle(screen, RED, (x, y), radius)

    pygame.display.flip()
    clock.tick(60)

pygame.quit()