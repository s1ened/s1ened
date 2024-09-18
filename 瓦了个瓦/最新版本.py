import pygame
from pygame.locals import *
from sys import exit
from random import randint, shuffle
from time import sleep
from os.path import exists


# Constants
WINDOW_WIDTH = 900
WINDOW_HEIGHT = 900
ICON_SIZE = 220
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

# Load background images
background_image = pygame.image.load('background1.jpg')
background_image = pygame.transform.scale(background_image, (WINDOW_WIDTH, WINDOW_HEIGHT))
level_choice_background = pygame.image.load('level_choice_background.jpg')
level_choice_background = pygame.transform.scale(level_choice_background, (WINDOW_WIDTH, WINDOW_HEIGHT))
game_background_image = pygame.image.load('game_background.jpg')
game_background_image = pygame.transform.scale(game_background_image, (WINDOW_WIDTH, WINDOW_HEIGHT))


def shuffle_data(data):
    for r in range(GRID_SIZE):
        for c in range(GRID_SIZE):
            r1 = randint(0, GRID_SIZE - 1)
            c1 = randint(0, GRID_SIZE - 1)
            data[r][c], data[r1][c1] = data[r1][c1], data[r][c]


def start_screen(screen, high_score):
    start = True
    title_font = pygame.font.Font('title_font.ttf', 60)
    while start:
        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()
                exit()
            if event.type == MOUSEBUTTONUP:
                x, y = event.pos
                if 350 < x < 550 and 450 < y < 500:
                    return True
                elif 350 < x < 550 and 500 < y < 550:
                    pygame.quit()
                    exit()

        screen.blit(background_image, (0, 0))
        title_text = title_font.render('瓦了个瓦', True, BLUE)
        screen.blit(title_text, (350, 200))
        text = title_font.render('Click to start', True, BLUE)
        screen.blit(text, (350, 450))
        text = title_font.render('Click to exit', True, BLUE)
        screen.blit(text, (350, 500))
        high_score_text = title_font.render(f'High Score: {high_score}', True, RED)
        screen.blit(high_score_text, (350, 300))
        pygame.display.update()


def game_over_screen(screen, font, high_score):
    game_over = True
    while game_over:
        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()
                exit()

        screen.fill(WHITE)
        game_over_text = font.render('Game Over! You have failed.', True, RED)
        screen.blit(game_over_text, (350, 450))
        high_score_text = font.render(f'High Score: {high_score}', True, RED)
        screen.blit(high_score_text, (350, 400))
        pygame.display.update()
        sleep(3)
        game_over = False


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
    total_score = 0
    score = 0
    item_count = 5
    pygame.init()
    # 加载背景音乐
    pygame.mixer.music.load("background_music.mp3")
    # 循环播放背景音乐
    pygame.mixer.music.play(-1)
    fps_clock = pygame.time.Clock()
    screen = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
    default_font = pygame.font.get_default_font()
    font = pygame.font.SysFont(default_font, 36)

    # 选择关卡界面
    level_choice = 0
    while level_choice not in [1, 2, 3]:
        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()
                exit()
            if event.type == MOUSEBUTTONUP:
                x, y = event.pos
                if 350 < x < 550 and 400 < y < 450:  # 调整了 Easy 按钮的 y 坐标范围
                    level_choice = 1
                elif 350 < x < 550 and 450 < y < 500:
                    level_choice = 2
                elif 350 < x < 550 and 500 < y < 550:
                    level_choice = 3

        screen.blit(level_choice_background, (0, 0))
        text = font.render('Choose level:', True, (0, 0, 0))
        screen.blit(text, (350, 300))
        draw_button(screen, "Easy", 350, 400, 200, 50, BUTTON_COLOR, BUTTON_TEXT_COLOR)
        draw_button(screen, "Normal", 350, 450, 200, 50, BUTTON_COLOR, BUTTON_TEXT_COLOR)
        draw_button(screen, "Hard", 350, 500, 200, 50, BUTTON_COLOR, BUTTON_TEXT_COLOR)
        pygame.display.update()

    # 根据关卡设置时间限制
    if level_choice == 1:
        time_limit = 90
    elif level_choice == 2:
        time_limit = 60
    else:
        time_limit = 30

    start_time = pygame.time.get_ticks()
    data = []
    for _ in range(GRID_SIZE * GRID_SIZE):
        data.append(randint(1, item_count))
    shuffle(data)
    data = [data[i:i + GRID_SIZE] for i in range(0, len(data), GRID_SIZE)]

    # 随机生成每个图片的位置
    positions = []
    for _ in range(GRID_SIZE * GRID_SIZE):
        x_pos = randint(0, WINDOW_WIDTH - ICON_SIZE)
        y_pos = randint(0, WINDOW_HEIGHT - ICON_SIZE)
        positions.append((x_pos, y_pos))

    store = [0] * STORE_SIZE
    history = []

    high_score = HighScore.read_high_score()

    start_screen(screen, high_score)

    # 记录每个位置图片的层叠顺序
    layer_order = list(range(len(positions)))
    shuffle(layer_order)

    while True:
        current_time = pygame.time.get_ticks()
        elapsed_time = (current_time - start_time) / 1000

        if elapsed_time > time_limit:
            game_over_screen(screen, font, high_score)
            if total_score > high_score:
                high_score = total_score
                HighScore.write_high_score(high_score)
            break

        screen.blit(game_background_image, (0, 0))

        # 绘制剩余时间
        time_remaining = max(0, time_limit - elapsed_time)
        time_text = f"Time: {int(time_remaining)}s"
        time_surface = font.render(time_text, True, RED)
        screen.blit(time_surface, (5, 25))

        # Draw score and mission
        mission_text = f"mission {item_count - 4}"
        mission_surface = font.render(mission_text, True, GREEN)
        screen.blit(mission_surface, (5, 45))

        score_text = f"score: {total_score}"
        score_surface = font.render(score_text, True, GREEN)
        screen.blit(score_surface, (5, 65))

        # Draw game grid
        index = 0
        for r in range(GRID_SIZE):
            for c in range(GRID_SIZE):
                if data[r][c]:
                    image = images[data[r][c] - 1]
                    x_pos, y_pos = positions[layer_order[index]]
                    rect = pygame.Rect(x_pos, y_pos, ICON_SIZE, ICON_SIZE)
                    screen.blit(image, (x_pos, y_pos))
                    index += 1

        # Draw items in store
        for i in range(STORE_SIZE):
            if store[i]:
                image = images[store[i] - 1]
                screen.blit(image, ((i * 50) + 26, 620))

        # Draw undo button
        draw_button(screen, "Undo", WINDOW_WIDTH - 150, 10, 140, 50, BUTTON_COLOR, BUTTON_TEXT_COLOR)

        # Check if all store slots are filled
        if all(store):
            game_over_screen(screen, font, high_score)
            if total_score > high_score:
                high_score = total_score
                HighScore.write_high_score(high_score)
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
                        score = total_score
                index = 0
                for r in range(GRID_SIZE):
                    for c in range(GRID_SIZE):
                        if data[r][c]:
                            image = images[data[r][c] - 1]
                            x_pos, y_pos = positions[layer_order[index]]
                            rect = pygame.Rect(x_pos, y_pos, ICON_SIZE, ICON_SIZE)
                            if rect.collidepoint(x, y):
                                is_visible = True
                                for i in range(len(layer_order)):
                                    if layer_order[i] < layer_order[index]:
                                        other_pos = positions[layer_order[i]]
                                        other_rect = pygame.Rect(other_pos[0], other_pos[1], ICON_SIZE, ICON_SIZE)
                                        if (
                                            x >= other_pos[0]
                                            and x <= other_pos[0] + ICON_SIZE
                                            and y >= other_pos[1]
                                            and y <= other_pos[1] + ICON_SIZE
                                            or (
                                                x >= other_pos[0]
                                                and x <= other_pos[0] + ICON_SIZE
                                                and y + ICON_SIZE >= other_pos[1]
                                                and y + ICON_SIZE <= other_pos[1] + ICON_SIZE
                                            )
                                            or (
                                                x + ICON_SIZE >= other_pos[0]
                                                and x + ICON_SIZE <= other_pos[0] + ICON_SIZE
                                                and y >= other_pos[1]
                                                and y <= other_pos[1] + ICON_SIZE
                                            )
                                            or (
                                                x + ICON_SIZE >= other_pos[0]
                                                and x + ICON_SIZE <= other_pos[0] + ICON_SIZE
                                                and y + ICON_SIZE >= other_pos[1]
                                                and y + ICON_SIZE <= other_pos[1] + ICON_SIZE
                                            )
                                        ):
                                            is_visible = False
                                            break
                                if is_visible:
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
                                        if score > SCORE_THRESHOLD:
                                            item_count += 1
                                            score = 0

                                    # Update grid with new colors
                                    data[r][c] = randint(1, 100) % item_count + 1

                                    # Push current state to history
                                    history.append((data[:], store[:], total_score))
                            index += 1

        pygame.display.update()
        fps_clock.tick(30)


if __name__ == "__main__":
    main()
