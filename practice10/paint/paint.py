import pygame
import sys
import math

pygame.init()

WIDTH, HEIGHT = 800, 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Paint")

WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)

screen.fill(WHITE)

clock = pygame.time.Clock()

# Қазіргі түс
current_color = BLACK

# Қазіргі режим
mode = "brush"

# Mouse басулы ма
drawing = False

# Бастапқы нүкте
start_pos = None
last_pos = None

while True:
    for event in pygame.event.get():
        # Терезені жабу
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

        # Пернемен режим және түс ауыстыру
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_b:
                mode = "brush"
            elif event.key == pygame.K_r:
                mode = "rect"
            elif event.key == pygame.K_c:
                mode = "circle"
            elif event.key == pygame.K_e:
                mode = "eraser"

            elif event.key == pygame.K_1:
                current_color = BLACK
            elif event.key == pygame.K_2:
                current_color = RED
            elif event.key == pygame.K_3:
                current_color = GREEN
            elif event.key == pygame.K_4:
                current_color = BLUE

        # Mouse басылғанда
        if event.type == pygame.MOUSEBUTTONDOWN:
            drawing = True
            start_pos = event.pos
            last_pos = event.pos

        # Mouse қозғалғанда
        if event.type == pygame.MOUSEMOTION:
            if drawing:
                if mode == "brush":
                    pygame.draw.line(screen, current_color, last_pos, event.pos, 5)
                    last_pos = event.pos

                elif mode == "eraser":
                    pygame.draw.line(screen, WHITE, last_pos, event.pos, 15)
                    last_pos = event.pos

        # Mouse жіберілгенде
        if event.type == pygame.MOUSEBUTTONUP:
            drawing = False
            end_pos = event.pos

            if mode == "rect":
                x1, y1 = start_pos
                x2, y2 = end_pos

                rect_x = min(x1, x2)
                rect_y = min(y1, y2)
                rect_w = abs(x2 - x1)
                rect_h = abs(y2 - y1)

                pygame.draw.rect(screen, current_color, (rect_x, rect_y, rect_w, rect_h), 3)

            elif mode == "circle":
                x1, y1 = start_pos
                x2, y2 = end_pos

                radius = int(math.sqrt((x2 - x1) ** 2 + (y2 - y1) ** 2))
                pygame.draw.circle(screen, current_color, start_pos, radius, 3)

    pygame.display.update()
    clock.tick(60)