import pygame
import sys

# ---------------- INITIALIZATION ----------------
pygame.init()

# ---------------- SCREEN SETTINGS ----------------
WIDTH = 900
HEIGHT = 650
TOOLBAR_HEIGHT = 90

screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Practice 11 Paint")

clock = pygame.time.Clock()
FPS = 60

# ---------------- COLORS ----------------
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
GRAY = (210, 210, 210)
DARK_GRAY = (80, 80, 80)
RED = (220, 0, 0)
GREEN = (0, 170, 0)
BLUE = (0, 80, 220)
YELLOW = (240, 210, 0)
PURPLE = (150, 0, 180)
ORANGE = (255, 130, 0)

# ---------------- FONTS ----------------
font = pygame.font.SysFont("Arial", 18)

# ---------------- CANVAS ----------------
canvas = pygame.Surface((WIDTH, HEIGHT - TOOLBAR_HEIGHT))
canvas.fill(WHITE)

# ---------------- DRAWING VARIABLES ----------------
current_color = BLACK
tool = "rectangle"
brush_size = 3

drawing = False
start_pos = None
current_pos = None

# ---------------- BUTTONS ----------------
tool_buttons = [
    ("Rect(R)", "rectangle", pygame.Rect(10, 10, 85, 30)),
    ("Circle(C)", "circle", pygame.Rect(105, 10, 85, 30)),
    ("Eraser(E)", "eraser", pygame.Rect(200, 10, 85, 30)),
    ("Square(S)", "square", pygame.Rect(295, 10, 90, 30)),
    ("RightTri(T)", "right_triangle", pygame.Rect(395, 10, 105, 30)),
    ("EqTri(Q)", "equilateral_triangle", pygame.Rect(510, 10, 85, 30)),
    ("Rhombus(H)", "rhombus", pygame.Rect(605, 10, 105, 30)),
]

color_buttons = [
    (BLACK, pygame.Rect(10, 50, 30, 30)),
    (RED, pygame.Rect(50, 50, 30, 30)),
    (GREEN, pygame.Rect(90, 50, 30, 30)),
    (BLUE, pygame.Rect(130, 50, 30, 30)),
    (YELLOW, pygame.Rect(170, 50, 30, 30)),
    (PURPLE, pygame.Rect(210, 50, 30, 30)),
    (ORANGE, pygame.Rect(250, 50, 30, 30)),
    (WHITE, pygame.Rect(290, 50, 30, 30)),
]


def screen_to_canvas(pos):
    """Convert screen position to canvas position."""
    x, y = pos
    return x, y - TOOLBAR_HEIGHT


def is_on_canvas(pos):
    """Check if mouse is inside canvas area."""
    x, y = pos
    return 0 <= x < WIDTH and TOOLBAR_HEIGHT <= y < HEIGHT


def draw_toolbar():
    """Draw toolbar buttons."""
    pygame.draw.rect(screen, GRAY, (0, 0, WIDTH, TOOLBAR_HEIGHT))

    for label, value, rect in tool_buttons:
        button_color = (170, 220, 255) if tool == value else (235, 235, 235)

        pygame.draw.rect(screen, button_color, rect)
        pygame.draw.rect(screen, DARK_GRAY, rect, 2)

        text = font.render(label, True, BLACK)
        screen.blit(text, (rect.x + 5, rect.y + 6))

    for color_value, rect in color_buttons:
        pygame.draw.rect(screen, color_value, rect)
        pygame.draw.rect(screen, DARK_GRAY, rect, 2)

        if current_color == color_value:
            pygame.draw.rect(screen, BLACK, rect, 4)

    info = font.render(f"Tool: {tool} | Brush: {brush_size}", True, BLACK)
    screen.blit(info, (350, 55))


def handle_toolbar_click(pos):
    """Handle click on tool or color button."""
    global tool, current_color

    for label, value, rect in tool_buttons:
        if rect.collidepoint(pos):
            tool = value
            return

    for color_value, rect in color_buttons:
        if rect.collidepoint(pos):
            current_color = color_value
            return


def draw_square(surface, color, start, end):
    """Draw square."""
    x1, y1 = start
    x2, y2 = end

    side = min(abs(x2 - x1), abs(y2 - y1))

    if x2 < x1:
        x1 -= side

    if y2 < y1:
        y1 -= side

    rect = pygame.Rect(x1, y1, side, side)
    pygame.draw.rect(surface, color, rect, brush_size)


def draw_right_triangle(surface, color, start, end):
    """Draw right triangle."""
    x1, y1 = start
    x2, y2 = end

    points = [
        (x1, y1),
        (x1, y2),
        (x2, y2)
    ]

    pygame.draw.polygon(surface, color, points, brush_size)


def draw_equilateral_triangle(surface, color, start, end):
    """Draw equilateral-like triangle."""
    x1, y1 = start
    x2, y2 = end

    top = ((x1 + x2) // 2, y1)
    left = (x1, y2)
    right = (x2, y2)

    pygame.draw.polygon(surface, color, [top, left, right], brush_size)


def draw_rhombus(surface, color, start, end):
    """Draw rhombus."""
    x1, y1 = start
    x2, y2 = end

    mid_x = (x1 + x2) // 2
    mid_y = (y1 + y2) // 2

    points = [
        (mid_x, y1),
        (x2, mid_y),
        (mid_x, y2),
        (x1, mid_y)
    ]

    pygame.draw.polygon(surface, color, points, brush_size)


def draw_shape(surface, selected_tool, color, start, end):
    """Draw selected shape."""
    x1, y1 = start
    x2, y2 = end

    rect = pygame.Rect(
        min(x1, x2),
        min(y1, y2),
        abs(x2 - x1),
        abs(y2 - y1)
    )

    if selected_tool == "rectangle":
        pygame.draw.rect(surface, color, rect, brush_size)

    elif selected_tool == "circle":
        pygame.draw.ellipse(surface, color, rect, brush_size)

    elif selected_tool == "square":
        draw_square(surface, color, start, end)

    elif selected_tool == "right_triangle":
        draw_right_triangle(surface, color, start, end)

    elif selected_tool == "equilateral_triangle":
        draw_equilateral_triangle(surface, color, start, end)

    elif selected_tool == "rhombus":
        draw_rhombus(surface, color, start, end)


def draw_preview():
    """Draw shape preview on canvas copy."""
    if drawing and start_pos and current_pos and tool != "eraser":
        preview = canvas.copy()
        draw_shape(preview, tool, current_color, start_pos, current_pos)
        screen.blit(preview, (0, TOOLBAR_HEIGHT))


# ---------------- MAIN LOOP ----------------
running = True

while running:
    screen.fill(WHITE)
    screen.blit(canvas, (0, TOOLBAR_HEIGHT))

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        # Keyboard shortcuts.
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_r:
                tool = "rectangle"
            elif event.key == pygame.K_c:
                tool = "circle"
            elif event.key == pygame.K_e:
                tool = "eraser"
            elif event.key == pygame.K_s:
                tool = "square"
            elif event.key == pygame.K_t:
                tool = "right_triangle"
            elif event.key == pygame.K_q:
                tool = "equilateral_triangle"
            elif event.key == pygame.K_h:
                tool = "rhombus"
            elif event.key == pygame.K_ESCAPE:
                running = False

        # Start drawing.
        if event.type == pygame.MOUSEBUTTONDOWN:
            if event.pos[1] < TOOLBAR_HEIGHT:
                handle_toolbar_click(event.pos)

            elif is_on_canvas(event.pos):
                drawing = True
                start_pos = screen_to_canvas(event.pos)
                current_pos = start_pos

        # Update current mouse position.
        if event.type == pygame.MOUSEMOTION:
            if drawing and is_on_canvas(event.pos):
                current_pos = screen_to_canvas(event.pos)

                # Eraser draws white circles.
                if tool == "eraser":
                    pygame.draw.circle(canvas, WHITE, current_pos, 12)

        # Finish drawing.
        if event.type == pygame.MOUSEBUTTONUP:
            if drawing and is_on_canvas(event.pos):
                end_pos = screen_to_canvas(event.pos)

                if tool != "eraser":
                    draw_shape(canvas, tool, current_color, start_pos, end_pos)

            drawing = False
            start_pos = None
            current_pos = None

    draw_preview()
    draw_toolbar()

    pygame.display.flip()
    clock.tick(FPS)

pygame.quit()
sys.exit()
