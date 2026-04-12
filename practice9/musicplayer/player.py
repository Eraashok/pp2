import pygame
import os

pygame.init()
pygame.mixer.init()

screen = pygame.display.set_mode((600, 400))
pygame.display.set_caption("Music Player")

font = pygame.font.Font(None, 30)
clock = pygame.time.Clock()

music_dir = "musics"
music_files = [f for f in os.listdir(music_dir) if f.endswith(".mp3")]

current = 0
playing = False
paused = False


def load_music():
    path = os.path.join(music_dir, music_files[current])
    pygame.mixer.music.load(path)


def play():
    global playing, paused
    pygame.mixer.music.play()
    playing = True
    paused = False


def stop():
    global playing, paused
    pygame.mixer.music.stop()
    playing = False
    paused = False


def next_song():
    global current
    current = (current + 1) % len(music_files)
    load_music()
    play()


def prev_song():
    global current
    current = (current - 1) % len(music_files)
    load_music()
    play()


if music_files:
    load_music()

running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        if event.type == pygame.KEYDOWN:

            if event.key == pygame.K_p:
                if not playing:
                    play()
                elif paused:
                    pygame.mixer.music.unpause()
                    paused = False

            elif event.key == pygame.K_s:
                stop()

            elif event.key == pygame.K_n:
                next_song()

            elif event.key == pygame.K_b:
                prev_song()

            elif event.key == pygame.K_SPACE:
                if playing and not paused:
                    pygame.mixer.music.pause()
                    paused = True
                elif playing and paused:
                    pygame.mixer.music.unpause()
                    paused = False

            elif event.key == pygame.K_q:
                running = False

    screen.fill((255, 255, 255))

    title = font.render("Music Player", True, (0, 0, 0))
    screen.blit(title, (220, 20))

    controls = font.render("P-Play  S-Stop  N-Next  B-Back  SPACE-Pause", True, (0, 0, 0))
    screen.blit(controls, (40, 70))

    if music_files:
        track = font.render(f"Now: {music_files[current]}", True, (0, 0, 255))
        screen.blit(track, (80, 150))

        status = "Playing" if playing and not paused else "Paused" if paused else "Stopped"
        status_text = font.render(f"Status: {status}", True, (255, 0, 0))
        screen.blit(status_text, (80, 200))
    else:
        no_music = font.render("No music found", True, (255, 0, 0))
        screen.blit(no_music, (200, 150))

    pygame.display.flip()
    clock.tick(30)

pygame.quit()