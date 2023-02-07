
# The beginning of a side project: my first game - PONG with the help of pygame and
# https://www.youtube.com/watch?v=Qf3-aDXG8q4&t=16s

# TO DO: difficulty settings, background image

import pygame
import sys
import random
from enum import Enum


class difficulty_level(Enum):
    LEVEL1 = 1
    LEVEL2 = 2
    LEVEL3 = 3


def timer():
    current_time = pygame.time.get_ticks()
    ticks = current_time - start_time
    seconds = int(ticks / 1000 % 60)
    minutes = int(ticks / 60000 % 24)
    out = '{minutes:02d}:{seconds:02d}'.format(minutes=minutes, seconds=seconds)
    out_1 = small_score_font.render(out, True, light_grey)
    screen.blit(out_1, (screen_width-200, screen_height-100))
    

def balls_animations():
    global ball_speed_x, ball_speed_y, player_score, opponent_score, score_time, rockImage
    balls.x += ball_speed_x
    balls.y += ball_speed_y

    # Collisions with the ball in screen or in the players
    if balls.top <= 0 or balls.bottom >= screen_height:
        ball_speed_y *= -1
        collision_ball_player_soundEffect.set_volume(0.2)
        collision_ball_player_soundEffect.play(0)

    if balls.left <= 0:
        player_score += 1
        winPoint_soundEffect.set_volume(1)
        winPoint_soundEffect.play(0)
        score_time = pygame.time.get_ticks()

    if balls.right >= screen_width:
        # Game over if opponent score > 5
        opponent_score += 1
        screen.blit(theRockMeme, (screen_width/2 - 430, screen_height/2 - 430))
        pygame.display.update(theRockMeme.get_rect())
        losePoint_soundEffect.play(0)
        score_time = pygame.time.get_ticks()

    if balls.colliderect(player) or balls.colliderect(opponent):
        ball_speed_x *= -1
        collision_ball_player_soundEffect.set_volume(0.2)
        collision_ball_player_soundEffect.play(0)


def player_animations():
    player.y += player_speed
    if player.top <= 0:
        player.top = 0
    if player.bottom >= screen_height:
        player.bottom = screen_height


def opponent_animations():
    if opponent.top < balls.y:
        opponent.top += opponent_speed
    if opponent.bottom > balls.y:
        opponent.bottom -= opponent_speed

    if opponent.top <= 0:
        opponent.top = 0
    if opponent.bottom >= screen_height:
        opponent.bottom = screen_height


def balls_restart():
    global ball_speed_x, ball_speed_y, score_time, rockImage

    current_time = pygame.time.get_ticks()
    balls.center = (screen_width/2, screen_height/2)

    if current_time - score_time < 700:
        number_three = small_score_font.render('3', True, light_grey)
        screen.blit(number_three, (screen_width/2 - 10, screen_height/2 + 40))
    if 700 < current_time - score_time < 1400:
        number_two = small_score_font.render('2', True, light_grey)
        screen.blit(number_two, (screen_width/2 - 10, screen_height/2 + 40))
    if 1400 < current_time - score_time < 2100:
        number_one = small_score_font.render('1', True, light_grey)
        screen.blit(number_one, (screen_width/2 - 10, screen_height/2 + 40))

    if current_time - score_time < 2100:
        ball_speed_x, ball_speed_y = 0, 0
    else:
        ball_speed_y = 7 * random.choice((-1, 1))
        ball_speed_x = 7 * random.choice((-1, 1))
        score_time = False


def mainMenu():
    main_menu = True

    pygame.mixer.music.load('elevator-music-kevin-macleod-gaming-background-music-hd (online-audio-converter.com).wav')
    pygame.mixer.music.play(-1)
    screen.blit(bg_img, (0, 0))
    while main_menu:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.mixer.music.stop()
                pygame.quit()
                sys.exit()

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    pygame.mixer.music.stop()
                    main_menu = False

                elif event.key == pygame.K_q:
                    pygame.mixer.music.stop()
                    pygame.quit()
                    quit()

        main_menu_text = big_main_menu_font.render('PONG: The Game', True, light_grey)
        main_menu_rect = main_menu_text.get_rect(center=(screen_width/2, 120))
        screen.blit(main_menu_text, main_menu_rect)

        controls_text = small_paused_font.render('UP key to move up, DOWN key to move down, ', True,  light_grey)
        controls_rect = controls_text.get_rect(center=(screen_width/2, 270))
        screen.blit(controls_text, controls_rect)

        controls_text = small_paused_font.render('P to pause and Q to quit. ', True, light_grey)
        controls_rect = controls_text.get_rect(center=(screen_width/2, 340))
        screen.blit(controls_text, controls_rect)

        controls_text = small_paused_font.render('Press SPACE to continue', True, light_grey)
        controls_rect = controls_text.get_rect(center=(screen_width/2, screen_height / 2 + 410))
        screen.blit(controls_text, controls_rect)

        pygame.display.flip()


def pause():
    global start_time, i

    paused = True
    before_pause_time = pygame.time.get_ticks()

    screen.blit(bg_img, (i, 0))
    while paused:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_c:
                    paused = False

                elif event.key == pygame.K_q:
                    pygame.quit()
                    quit()

        paused_text = paused_font.render('Paused', True, light_grey)
        paused_text_rect = paused_text.get_rect(center=(screen_width/2, 100))
        screen.blit(paused_text, paused_text_rect)

        extra_text = small_paused_font.render('Press C to continue or Q to quit.', True, light_grey)
        extra_text_rect = extra_text.get_rect(center=(screen_width/2, 250))
        screen.blit(extra_text, extra_text_rect)

        # Pause rectangles
        p_left = pygame.Rect(screen_width/2 - 70, screen_height/2 - 70, 40, 140)
        pygame.draw.rect(screen, light_grey, p_left)
        p_right = pygame.Rect(screen_width/2 + 20, screen_height/2 - 70, 40, 140)
        pygame.draw.rect(screen, light_grey, p_right)

        controls_text = small_paused_font.render('UP key to move up, DOWN key to move down, ', True, light_grey)
        controls_rect = controls_text.get_rect(center=(screen_width / 2, screen_height / 2 + 355))
        screen.blit(controls_text, controls_rect)

        controls_text = small_paused_font.render('P to pause and Q to quit. ', True, light_grey)
        controls_rect = controls_text.get_rect(center=(screen_width / 2, screen_height / 2 + 420))
        screen.blit(controls_text, controls_rect)

        pygame.display.flip()

    after_pause = pygame.time.get_ticks()
    paused_time = after_pause - before_pause_time
    start_time += paused_time


# General Setup for the window
pygame.mixer.pre_init(44100, -16, 2, 256)
pygame.init()
clock = pygame.time.Clock()

# Setup for the window where the game will be played
screen_width = 1280
screen_height = 960
screen = pygame.display.set_mode((screen_width, screen_height))
pygame.display.set_caption('Pong')

# Sound effects
# pygame.mixer.music.load('elevator-music-kevin-macleod-gaming-background-music-hd (online-audio-converter.com).wav')
# pygame.mixer.music.load('gameBackgroundMusic.wav')
winPoint_soundEffect = pygame.mixer.Sound('super-mario-coin-sound.wav')
losePoint_soundEffect = pygame.mixer.Sound('the-rock-meme-sound.wav')
levelUp_soundEffect = pygame.mixer.Sound('level-up-sound-effect.wav')
collision_ball_player_soundEffect = pygame.mixer.Sound('270343__littlerobotsoundfactory__shoot_01.wav')

theRockMeme = pygame.image.load('theRock.jpeg')

# Fonts
paused_font = pygame.font.Font('PixeloidSans-JR6qo.ttf', 80)
small_paused_font = pygame.font.Font('PixeloidSans-JR6qo.ttf', 40)
small_score_font = pygame.font.Font('PixeloidSans-JR6qo.ttf', 40)
big_main_menu_font = pygame.font.Font('PixeloidSans-JR6qo.ttf', 100)

# Game Rectangles
balls = pygame.Rect(screen_width/2 - 15, screen_height/2 - 15, 30, 30)
player = pygame.Rect(screen_width - 20, screen_height/2 - 70, 10, 140)
opponent = pygame.Rect(10, screen_height/2 - 70, 10, 140)
player_score = 0
opponent_score = 0

color_bg = pygame.Color('grey12')
bg_img = pygame.image.load('1643224858.jpg')
light_grey = (200, 200, 200)

ball_speed_x = 7 * random.choice((-1, 1))
ball_speed_y = 7 * random.choice((-1, 1))
player_speed = 0
opponent_speed = 8      # the opponent speed will symbolize the difficulty
mainMenu()
current_level = difficulty_level.LEVEL1

pygame.mixer.music.unload()
pygame.mixer.music.load('gameBackgroundMusic.wav')
pygame.mixer.music.set_volume(0.5)
pygame.mixer.music.play(-1)

# Score Timer, and clock timer
score_time = True
start_time = pygame.time.get_ticks()

i = 0
# main game loop
while True:
    screen.fill((0, 0, 0))
    screen.blit(bg_img, (i, 0))
    screen.blit(bg_img, (screen_width + i, 0))
    if i == -screen_width:
        screen.blit(bg_img, (screen_width + i, 0))
        i = 0
    i -= 1

    # Handling inputs
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

        # When a key is pressed
        if event.type == pygame.KEYDOWN:
            # Movement
            if event.key == pygame.K_DOWN:
                player_speed += 7
            elif event.key == pygame.K_UP:
                player_speed -= 7

            # For the pause button
            elif event.key == pygame.K_p:
                volume = pygame.mixer.music.get_volume()
                pygame.mixer.music.set_volume(0.1)
                pause()

                pygame.mixer.music.set_volume(volume)

            elif event.key == pygame.K_q:
                pygame.quit()
                quit()

        # When a key is released
        if event.type == pygame.KEYUP:
            # Movement
            if event.key == pygame.K_DOWN:
                player_speed -= 7
            elif event.key == pygame.K_UP:
                player_speed += 7

    # Ball animation with its Collisions
    balls_animations()
    # Player animation and Collisions
    player_animations()
    # Opponent animation and Collisions
    opponent_animations()

    # Visuals
    pygame.draw.rect(screen, light_grey, player)
    pygame.draw.rect(screen, light_grey, opponent)
    pygame.draw.ellipse(screen, light_grey, balls)
    pygame.draw.aaline(screen, light_grey, (screen_width/2, 0), (screen_width/2, screen_height))

    # Display score
    opponent_score_text = small_score_font.render(str(opponent_score), True, light_grey)
    screen.blit(opponent_score_text, (screen_width/2 - 65, screen_height/2))
    player_score_text = small_score_font.render(str(player_score), True, light_grey)
    screen.blit(player_score_text, (screen_width/2 + 45, screen_height/2))

    # Score Timer
    if score_time:
        balls_restart()

    # Display game timer
    timer()

    # Updating the window
    pygame.display.flip()
    # Controlling the speed
    clock.tick(60)

