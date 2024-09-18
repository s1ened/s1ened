import pygame
from pygame.locals import *
from sys import exit
from random import randint, shuffle
from time import sleep
from os.path import exists


# Constants
WINDOW_WIDTH = 900
WINDOW_HEIGHT = 900
ICON_SIZE = 200  # 这是每个图标的目标大小
GRID_SIZE = 3
SCORE_THRESHOLD = 10
STORE_SIZE = 7

# Colors
WHITE = pygame.Color(255, 255, 255)
RED = pygame.Color(255, 0, 0)
GREEN = pygame.Color(0, 255, 0)
BLUE = pygame.Color(0, 0, 255)
BUTTON_COLOR = pygame.Color(255, 165, 0)
BUTTON_TEXT_COLOR = WHITE

# Load and scale images
image_paths = [
    'pattern_1.png',
    'pattern_2.png',
    'pattern_3.png',
    'pattern_4.png',
    'pattern_5.png',
    'pattern_6.png',
    'pattern_7.png'
]
images = []
for path in image_paths:
    image = pygame.image.load(path)
    scaled_image = pygame.transform.scale(image, (ICON_SIZE, ICON_SIZE))
    images.append(scaled_image)

# Load background image
background_image = pygame.image.load('background1.jpg')
background_image = pygame.transform.scale(background_image, (WINDOW_WIDTH, WINDOW_HEIGHT))
success_background_image = pygame.image.load('success_background.jpg')
success_background_image = pygame.transform.scale(success_background_image, (WINDOW_WIDTH, WINDOW_HEIGHT))
fail_background_image = pygame.image.load('fail_background.jpg')
fail_background_image = pygame.transform.scale(fail_background_image, (WINDOW_WIDTH, WINDOW_HEIGHT))


def shuffle_data(data):
    for r in range(GRID_SIZE):
        for c in range(GRID_SIZE):
            r1 = randint(0, GRID_SIZE - 1)
            c1 = randint(0, GRID_SIZE - 1)
            data[r][c], data[r1][c1] = data[r1][c1], data[r][c]


def start_screen(screen):
    start = True
    title_font = pygame.font.Font('title_font.ttf', 48)
    selected_mode = None
    high_score = HighScore.read_high_score()
    while start:
        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()
                exit()
            if event.type == MOUSEBUTTONUP:
                x, y = event.pos
                if 350 < x < 550 and 350 < y < 400:
                    selected_mode = 'easy'
                    start = False
                elif 350 < x < 550 and 400 < y < 450:
                    selected_mode = 'normal'
                    start = False
                elif 350 < x < 550 and 450 < y < 500:
                    selected_mode = 'hard'
                    start = False
        screen.blit(background_image, (0, 0))
        title_text = title_font.render('VALORANT', True, BLUE)
        screen.blit(title_text, (350, 200))
        text = title_font.render('Easy', True, BLUE)
        screen.blit(text, (350, 350))
        text = title_font.render('Normal', True, BLUE)
        screen.blit(text, (350, 400))
        text = title_font.render('Hard', True, BLUE)
        screen.blit(text, (350, 450))
        high_score_text = title_font.render(f'High Score: {high_score}', True, GREEN)
        screen.blit(high_score_text, (350, 300))

        description_font = pygame.font.SysFont('arial', 30)
        description_text_1 = description_font.render("1: Game is three in a row elimination", True, WHITE)
        description_text_2 = description_font.render("2: If seven images in the bottom box without elimination, game over", True, WHITE)
        description_text_3 = description_font.render("3: The 'undo' button on the top right can be used for withdrawal", True, WHITE)
        screen.blit(description_text_1, (100, 500))
        screen.blit(description_text_2, (100, 550))
        screen.blit(description_text_3, (100, 600))

        pygame.display.update()
    return selected_mode


def success_screen(screen):
    success = True
    title_font = pygame.font.Font('title_font.ttf', 48)
    text_font = pygame.font.Font('text_font.ttf', 60)
    while success:
        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()
                exit()
        screen.blit(success_background_image, (0, 0))
        title_text = title_font.render('Success!', True, GREEN)
        text = text_font.render('You are success!', True, GREEN)
        screen.blit(title_text, (350, 450))
        screen.blit(text, (300, 500))
        pygame.display.update()
        sleep(3)
        success = False


def fail_screen(screen):
    fail = True
    title_font = pygame.font.Font('title_font.ttf', 48)
    text_font = pygame.font.Font('text_font.ttf', 60)
    while fail:
        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()
                exit()
        screen.blit(fail_background_image, (0, 0))
        title_text = title_font.render('Fail!', True, RED)
        text = text_font.render('You are failed!', True, RED)
        screen.blit(title_text, (350, 450))
        screen.blit(text, (300, 500))
        pygame.display.update()
        sleep(3)
        fail = False


def draw_button(screen, text, x, y, width, height, button_color, text_color):
    pygame.draw.rect(screen, button_color, (x, y, width, height))
    font = pygame.font.SysFont(None, 36)
    text_surface = font.render(text, True, text_color)
    text_rect = text_surface.get_rect(center=(x + width / 2, y + height / 2))
    screen.blit(text_surface, text_rect)


class HighScore:
    @staticmethod
    def read_high_score():
        try:
            with open('highscore.txt', 'r') as file:
                return int(file.read().strip())
        except FileNotFoundError:
            return 0

    @staticmethod
    def write_high_score(score):
        with open('highscore.txt', 'w') as file:
            file.write(str(score))


def main():
    pygame.mixer.init()
    pygame.mixer.music.load('background_music.mp3')
    pygame.mixer.music.play(-1)

    total_score = 0
    score = 0
    pygame.init()
    fps_clock = pygame.time.Clock()
    screen = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
    default_font = pygame.font.get_default_font()
    font = pygame.font.SysFont(default_font, 24)

    data = [[i + 1 for i in range(GRID_SIZE)] for j in range(GRID_SIZE)]
    shuffle_data(data)

    store = [0] * STORE_SIZE
    history = []

    offset_x = (WINDOW_WIDTH - (GRID_SIZE * (ICON_SIZE + 10) + 10)) / 2
    offset_y = (WINDOW_HEIGHT - (GRID_SIZE * (ICON_SIZE + 10) + 10)) / 2

    mode = start_screen(screen)
    if mode == 'easy':
        time_limit = 90
    elif mode == 'normal':
        time_limit = 50
    else:
        time_limit = 30
    start_time = pygame.time.get_ticks()
    while True:
        current_time = (pygame.time.get_ticks() - start_time) // 1000
        time_remaining = max(0, time_limit - current_time)
        if time_remaining == 0:
            if total_score >= 20:
                success_screen(screen)
            else:
                fail_screen(screen)
            break

        time_text = f"Time: {time_remaining:02d}"
        time_surface = font.render(time_text, True, RED)
        screen.blit(time_surface, (WINDOW_WIDTH // 2 - time_surface.get_width() // 2, 10))

        screen.blit(background_image, (0, 0))

        # Draw score
        score_text = f"score: {total_score}"
        score_surface = font.render(score_text, True, GREEN)
        screen.blit(score_surface, (5, 65))

        # Draw game grid
        for r in range(GRID_SIZE):
            for c in range(GRID_SIZE):
                if data[r][c]:
                    image = images[data[r][c] - 1]
                    screen.blit(image,
                                 (offset_x + c * (ICON_SIZE + 10), offset_y + r * (ICON_SIZE + 10)))

        # Draw items in store
        for i in range(STORE_SIZE):
            if store[i]:
                image = images[store[i] - 1]
                screen.blit(image, ((i * 50) + 26, 620))

        # Draw undo button
        draw_button(screen, "Undo", WINDOW_WIDTH - 150, 10, 140, 50, BUTTON_COLOR, BUTTON_TEXT_COLOR)

        # Draw time extend button
        draw_button(screen, "Extend Time", WINDOW_WIDTH - 150, 70, 140, 50, BUTTON_COLOR, BUTTON_TEXT_COLOR)

        # Check if all store slots are filled
        if all(store) and not any([store.count(i) == 3 for i in store]):
            fail_screen(screen)
            break

        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()
                exit()

            if event.type == MOUSEBUTTONUP:
                x, y = event.pos

                # Check for undo button click
                undo_button_rect = pygame.Rect(WINDOW_WIDTH - 150, 10, 140, 50)
                if undo_button_rect.collidepoint(x, y):
                    if history:
                        last_state = history.pop()
                        data, store, total_score = last_state

                # Check for time extend button click
                time_extend_button_rect = pygame.Rect(WINDOW_WIDTH - 150, 70, 140, 50)
                if time_extend_button_rect.collidepoint(x, y):
                    time_limit += 5

                for r in range(GRID_SIZE):
                    for c in range(GRID_SIZE):
                        rect_x = offset_x + c * (ICON_SIZE + 10)
                        rect_y = offset_y + r * (ICON_SIZE + 10)

                        if rect_x < x < rect_x + ICON_SIZE and rect_y < y < rect_y + ICON_SIZE:
                            clicked_color = data[r][c]

                            # Add color to store
                            for i in range(STORE_SIZE):
                                if store[i] == 0:
                                    store[i] = clicked_color
                                    break

                            # Check for matching colors
                            count = store.count(clicked_color)
                            if count == 3:
                                store = [0 if color == clicked_color else color for color in store]
                                score += 1
                                total_score += 1

                            # Update grid with new colors
                            data[r][c] = randint(1, 100) % 7 + 1

                            # Push current state to history
                            history.append((data[:], store[:], total_score))

        pygame.display.update()
        fps_clock.tick(30)


if __name__ == "__main__":
    main()
