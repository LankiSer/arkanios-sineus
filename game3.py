import pgzrun
import random

TITLE = "Arkanoid"
WIDTH = 800
HEIGHT = 500

# Game states
STATE_MENU = 0
STATE_PLAYING = 1
STATE_INSTRUCTIONS = 2
STATE_GAME_OVER = 3

game_state = STATE_MENU

# Paddle and ball setup
paddle = Actor("paddleblue.png")
paddle.x = 120
paddle.y = 420

ball = Actor("ballblue.png")
ball.x = 100
ball.y = 300

ball_x_speed = -2
ball_y_speed = -2

bars_list = []

def draw():
    if game_state == STATE_MENU:
        draw_menu()
    elif game_state == STATE_PLAYING:
        draw_game()
    elif game_state == STATE_INSTRUCTIONS:
        draw_instructions()
    elif game_state == STATE_GAME_OVER:
        draw_game_over()

def draw_menu():
    screen.clear()
    screen.blit("background.png", (0, 0))
    screen.draw.text("Arkanoid Clone", center=(WIDTH // 2, HEIGHT // 4), fontsize=60, color="white")
    screen.draw.text("Play", center=(WIDTH // 2, HEIGHT // 2), fontsize=40, color="white")
    screen.draw.text("Instructions", center=(WIDTH // 2, HEIGHT // 2 + 60), fontsize=40, color="white")

def draw_game():
    screen.blit("background.png", (0, 0))
    paddle.draw()
    ball.draw()
    for bar in bars_list:
        bar.draw()

def draw_instructions():
    screen.clear()
    screen.blit("background.png", (0, 0))
    screen.draw.text("Instructions", center=(WIDTH // 2, HEIGHT // 4), fontsize=60, color="white")
    screen.draw.text("Use LEFT and RIGHT arrow keys to move the paddle.", center=(WIDTH // 2, HEIGHT // 2), fontsize=30, color="white")
    screen.draw.text("Break all the blocks to win.", center=(WIDTH // 2, HEIGHT // 2 + 40), fontsize=30, color="white")
    screen.draw.text("Press ESC to go back to the menu.", center=(WIDTH // 2, HEIGHT // 2 + 80), fontsize=30, color="white")

def draw_game_over():
    screen.clear()
    screen.blit("background.png", (0, 0))
    screen.draw.text("You Lose", center=(WIDTH // 2, HEIGHT // 2), fontsize=60, color="white")
    screen.draw.text("Press R to Restart", center=(WIDTH // 2, HEIGHT // 2 + 60), fontsize=40, color="white")

def generate_level():
    global bars_list
    bars_list = []
    coloured_box_list = ["element_blue_rectangle_glossy.png", "element_green_rectangle_glossy.png", "element_red_rectangle_glossy.png"]
    max_rows = random.randint(3, 6)
    max_cols = random.randint(6, 12)
    x_start = 120
    y_start = 100
    x_gap = 70
    y_gap = 50

    for row in range(max_rows):
        for col in range(max_cols):
            if random.random() < 0.8:  # 80% chance of generating a block
                bar = Actor(random.choice(coloured_box_list))
                bar.x = x_start + col * x_gap
                bar.y = y_start + row * y_gap
                bars_list.append(bar)


def update():
    global game_state, ball_x_speed, ball_y_speed

    if game_state == STATE_PLAYING:
        # Обработка движения ракетки влево
        if keyboard.left:
            paddle.x = max(paddle.x - 5, paddle.width // 2)

        # Обработка движения ракетки вправо
        if keyboard.right:
            paddle.x = min(paddle.x + 5, WIDTH - paddle.width // 2)

        # Обновление позиции мяча
        update_ball()

        # Проверка столкновения мяча с блоками
        for bar in bars_list:
            if ball.colliderect(bar):
                bars_list.remove(bar)
                ball_y_speed *= -1

                # Изменение горизонтальной скорости мяча в зависимости от точки столкновения
                if ball.x < bar.x + bar.width / 3:
                    ball_x_speed = -abs(ball_x_speed)
                elif ball.x > bar.x + bar.width * 2 / 3:
                    ball_x_speed = abs(ball_x_speed)

        # Проверка столкновения мяча с ракеткой
        if paddle.colliderect(ball):
            ball_y_speed = -abs(ball_y_speed)

            # Изменение горизонтальной скорости мяча в зависимости от точки столкновения с ракеткой
            if ball.x < paddle.x + paddle.width / 3:
                ball_x_speed = -abs(ball_x_speed)
            elif ball.x > paddle.x + paddle.width * 2 / 3:
                ball_x_speed = abs(ball_x_speed)
            else:
                ball_x_speed = 0

        # Проверка, упал ли мяч за пределы экрана (проигрыш)
        if ball.y > HEIGHT:
            game_state = STATE_GAME_OVER

        # Обработка нажатия клавиши "R" для перезапуска игры
        if keyboard.r:
            reset_game()
            generate_level()

    elif game_state == STATE_INSTRUCTIONS:
        # Обработка нажатия клавиши "Escape" для возврата в главное меню
        if keyboard.escape:
            game_state = STATE_MENU

    elif game_state == STATE_GAME_OVER:
        # Обработка нажатия клавиши "R" для перезапуска игры после проигрыша
        if keyboard.r:
            reset_game()
            generate_level()
            game_state = STATE_PLAYING


def reset_game():
    global ball_x_speed, ball_y_speed, bars_list
    ball.x = WIDTH // 2
    ball.y = HEIGHT - 100
    paddle.x = WIDTH // 2
    paddle.y = HEIGHT - 50
    ball_x_speed = random.choice([-2, 2])
    ball_y_speed = -2
    bars_list = []

def update_ball():
    global ball_x_speed, ball_y_speed
    ball.x += ball_x_speed
    ball.y += ball_y_speed

    # Ball collision with walls
    if ball.x <= 0 or ball.x >= WIDTH:
        ball_x_speed *= -1
    if ball.y <= 0:
        ball_y_speed *= -1

    # Ball falls below the paddle (lose condition)
    if ball.y >= HEIGHT:
        global game_state
        game_state = STATE_GAME_OVER

def on_mouse_down(pos):
    global game_state
    if game_state == STATE_MENU:
        if WIDTH // 2 - 50 < pos[0] < WIDTH // 2 + 50 and HEIGHT // 2 - 20 < pos[1] < HEIGHT // 2 + 20:
            reset_game()
            generate_level()
            game_state = STATE_PLAYING
        elif WIDTH // 2 - 100 < pos[0] < WIDTH // 2 + 100 and HEIGHT // 2 + 40 < pos[1] < HEIGHT // 2 + 80:
            game_state = STATE_INSTRUCTIONS

# Start the game
pgzrun.go()