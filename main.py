# The beginning of a side project: my first game - PONG with the help of pygame and
# https://www.youtube.com/watch?v=Qf3-aDXG8q4&t=16s

# TO DO: upgrade system with coins and economy, multiplayer mode and update the level up sounds since they are outdated

import pygame
import sys
import random
from enum import Enum


# Enum for the difficulty setting
class difficulty_level(Enum):
    LEVEL1 = 1
    LEVEL2 = 2
    LEVEL3 = 3


class FadeInBlack(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.rect = pygame.display.get_surface().get_rect()
        self.image = pygame.Surface(self.rect.size, flags=pygame.SRCALPHA)
        self.alpha = 0
        self.direction = 1

    def update(self):
        self.image.fill((0, 0, 0, self.alpha))
        self.alpha += self.direction
        if self.alpha > 255 or self.alpha < 0:
            self.direction *= -1
            self.alpha += self.direction


class Block(pygame.sprite.Sprite):
    def __init__(self, path, x_pos, y_pos):
        super().__init__()
        self.image = pygame.image.load(path)
        self.rect = self.image.get_rect(center=(x_pos, y_pos))


class Button(Block):
    def __init__(self, path, x_pos, y_pos):
        super().__init__(path, x_pos, y_pos)
        self.level = 1


class UpgradeSpeed(Button):
    def __init__(self, path, x_pos, y_pos):
        super().__init__(path, x_pos, y_pos)
        self.level = 1
        self.cost = 5
        self.image = pygame.transform.scale(self.image, (131, 131))

    def upgrade_button(self):
        if game_manager.coins_collected >= self.cost and self.level != 10:
            GameManager.decrease_cost_speed(game_manager)
            self.level += 1
            player.speed += 1
            paddle_group.update(ball_sprite)
            self.cost += 5
            upgrade_soundEffect.play()
        else:
            error_soundEffect.play()


class UpgradeSize(Button):
    def __init__(self, path, x_pos, y_pos):
        super().__init__(path, x_pos, y_pos)
        self.level = 1
        self.cost = 10
        self.image = pygame.transform.scale(self.image, (131, 131))

    def upgrade_button(self):
        if game_manager.coins_collected >= self.cost and self.level != 10:
            GameManager.decrease_cost_size(game_manager)
            self.level += 1

            current_width = player.rect.width
            current_height = player.rect.height
            player.rect = player.image.get_rect(center=player.rect.center)
            player.image = pygame.transform.scale(player.image, (current_width, current_height + 10))

            self.cost += 5
            upgrade_soundEffect.play()
        else:
            error_soundEffect.play()


class Coin(Block):
    def __init__(self, path, x_pos, y_pos, speed):
        super().__init__(path, x_pos, y_pos)
        self.speed = speed

    # Coin spawn screen limits
    def screen_constrain(self):
        if self.rect.top <= 0:
            self.rect.top = 0
        if self.rect.bottom >= screen_height - 170:
            self.rect.bottom = screen_height - 170

    def update(self):
        self.rect.x += self.speed
        self.screen_constrain()
        if self.rect.x >= screen_width:
            self.kill()

    def collided_with_player(self, player_rect):
        return self.rect.colliderect(player_rect)


class Player(Block):
    def __init__(self, path, x_pox, y_pos, speed):
        super().__init__(path, x_pox, y_pos)
        self.speed = speed
        self.movement = 0

    # Player screen limits
    def screen_constrain(self):
        if self.rect.top <= 10:
            self.rect.top = 10
        if self.rect.bottom >= screen_height - 170:
            self.rect.bottom = screen_height - 170

    # This is similar to the player_animation function
    def update(self, ball_group):
        self.rect.y += self.movement
        self.screen_constrain()

    # Resets the player object
    def reset_player(self):
        self.rect.x = screen_width - 20
        self.rect.y = (screen_height - 160) / 2
        self.speed = 5
        self.movement = 0


class Ball(Block):
    def __init__(self, path, x_pox, y_pox, speed_x, speed_y, paddles):
        super().__init__(path, x_pox, y_pox)
        self.speed_x = speed_x * random.choice((-1, 1))
        self.speed_y = speed_y * random.choice((-1, 1))
        self.paddles = paddles
        self.active = False
        self.score_time = 0

    # Similar to the balls_animations function
    def update(self):
        if self.active:
            self.rect.x += self.speed_x
            self.rect.y += self.speed_y
            self.collisions()
        else:
            self.restart_counter()

    # Similar to the Collision part of the balls_animations function
    def collisions(self):
        if self.rect.top <= 0 or self.rect.bottom >= screen_height - 160:
            collision_ball_player_soundEffect.set_volume(0.2)
            collision_ball_player_soundEffect.play(0)
            self.speed_y *= -1

        # Similar to the player collision section of the balls_animations function
        if pygame.sprite.spritecollide(self, self.paddles, False):
            collision_paddle = pygame.sprite.spritecollide(self, self.paddles, False)[0].rect
            collision_ball_player_soundEffect.set_volume(0.2)
            collision_ball_player_soundEffect.play(0)
            if abs(self.rect.right - collision_paddle.left) < 10 and self.speed_x > 0:
                self.speed_x *= -1
            if abs(self.rect.left - collision_paddle.right) < 10 and self.speed_x < 0:
                self.speed_x *= -1
            if abs(self.rect.top - collision_paddle.bottom) < 10 and self.speed_y < 0:
                self.rect.top = collision_paddle.bottom
                self.speed_y *= -1
            if abs(self.rect.bottom - collision_paddle.top) < 10 and self.speed_y > 0:
                self.rect.bottom = collision_paddle.top
                self.speed_y *= -1

    def reset_ball(self):
        self.active = False
        self.speed_x *= random.choice((-1, 1))
        self.speed_y *= random.choice((-1, 1))
        self.score_time = pygame.time.get_ticks()
        self.rect.center = (screen_width / 2, (screen_height - 160) / 2)

    # Similar to the balls_restart function
    def restart_counter(self):
        current_time = pygame.time.get_ticks()
        countdown_number = 3

        if not self.active:
            if current_time - self.score_time <= 700:
                countdown_number = 3
            if 700 < current_time - self.score_time <= 1400:
                countdown_number = 2
            if 1400 < current_time - self.score_time <= 2100:
                countdown_number = 1
            if current_time - self.score_time >= 2100:
                self.active = True

        time_counter = small_score_font.render(str(countdown_number), True, light_grey)
        screen.blit(time_counter, (screen_width / 2 - 10, screen_height / 2 - 50))


class Opponent(Block):
    def __init__(self, path, x_pos, y_pos, speed):
        super().__init__(path, x_pos, y_pos)
        self.speed = speed

    # Similar to the opponent_AI_animations
    def update(self, ball_group):
        if self.rect.top < ball_group.sprite.rect.y:
            self.rect.y += self.speed
        if self.rect.bottom > ball_group.sprite.rect.y:
            self.rect.y -= self.speed
        self.screen_constrain()

    def screen_constrain(self):
        if self.rect.top <= 10:
            self.rect.top = 10
        if self.rect.bottom >= screen_height - 170:
            self.rect.bottom = screen_height - 170

    # Resets the opponent object
    def reset_player(self):
        self.rect.x = 20
        self.rect.y = (screen_height - 160) / 2
        self.speed = 5


class GameManager:
    def __init__(self, ball_group, paddle_group, coin_group, button_group):
        self.start_time = 0
        self.paused = False

        self.levelUp_soundEffect_counter = 0
        self.background_counter = 0
        self.last_spawn_time_coin = pygame.time.get_ticks()

        self.current_level = difficulty_level.LEVEL1

        self.player_score = 0
        self.opponent_score = 0
        self.coins_collected = 0
        self.ball_group = ball_group
        self.paddle_group = paddle_group
        self.coin_group = coin_group
        self.button_group = button_group

    def run_game(self):
        # Draws the background and game objects
        self.background_movement()
        self.paddle_group.draw(screen)
        self.ball_group.draw(screen)
        self.ui_draw()

        self.draw_score()
        self.draw_level()
        self.draw_number_of_coins()
        pygame.draw.aaline(screen, light_grey, (screen_width / 2, 0), (screen_width / 2, screen_height - 160))

        # Checks the difficulty level with the timer
        self.timer()
        self.level_checker()
        self.game_over_checker()

        # Updating the game objects
        self.paddle_group.update(self.ball_group)
        self.ball_group.update()
        self.reset_ball()
        self.coin_group.draw(screen)
        self.coin_creator()
        self.button_group.update()

    def ui_draw(self):
        ui = pygame.Rect(0, screen_height - 160, screen_width, 160)
        pygame.draw.rect(screen, light_grey, ui)
        border1 = pygame.Rect(0, screen_height - 160, screen_width, 15)
        pygame.draw.rect(screen, game_over_black, border1)
        border2 = pygame.Rect(0, screen_height - 15, screen_width, 15)
        pygame.draw.rect(screen, game_over_black, border2)
        border3 = pygame.Rect(0, screen_height - 160, 15, 160)
        pygame.draw.rect(screen, game_over_black, border3)
        border4 = pygame.Rect(screen_width - 15, screen_height - 160, 15, 160)
        pygame.draw.rect(screen, game_over_black, border4)

        # Draws the upgrade buttons
        button_group.draw(screen)

        # Draws the cost and level of the buttons
        if speed_button.level != 10:
            speed_button_lvl = button_font.render(str(speed_button.level), True, game_over_black)
            speed_button_lvl_rect = speed_button_lvl.get_rect(center=(716, screen_height - 94))
            screen.blit(speed_button_lvl, speed_button_lvl_rect)
        else:
            speed_button_lvl = button_font.render('MAX', True, game_over_black)
            speed_button_lvl_rect = speed_button_lvl.get_rect(center=(716, screen_height - 94))
            screen.blit(speed_button_lvl, speed_button_lvl_rect)

        speed_button_cost = button_font.render(str(speed_button.cost), True, game_over_black)
        speed_button_cost_rect = speed_button_cost.get_rect(center=(689, screen_height - 60))
        screen.blit(speed_button_cost, speed_button_cost_rect)

        if size_button.level != 10:
            size_button_lvl = button_font.render(str(size_button.level), True, white)
            size_button_lvl_rect = size_button_lvl.get_rect(center=(966, screen_height - 94))
            screen.blit(size_button_lvl, size_button_lvl_rect)
        else:
            speed_button_lvl = button_font.render('MAX', True, game_over_black)
            speed_button_lvl_rect = speed_button_lvl.get_rect(center=(966, screen_height - 94))
            screen.blit(speed_button_lvl, speed_button_lvl_rect)

        size_button_cost = button_font.render(str(size_button.cost), True, white)
        size_button_cost_rect = size_button_cost.get_rect(center=(939, screen_height - 60))
        screen.blit(size_button_cost, size_button_cost_rect)

        command_speed = small_score_font.render('E', True, game_over_black)
        command_speed_rect = command_speed.get_rect(center=(590, screen_height - 83))
        screen.blit(command_speed, command_speed_rect)

        command_size = small_score_font.render('R', True, game_over_black)
        command_size_rect = command_size.get_rect(center=(840, screen_height - 83))
        screen.blit(command_size, command_size_rect)

    def coin_generator(self):
        now = pygame.time.get_ticks()
        if now - self.last_spawn_time_coin > COIN_SPAWN_TIME:
            coin = Coin('Coin.png', 0, random.randint(10, screen_height - 180), 2)
            self.last_spawn_time_coin = now
            return coin
        else:
            coin = 0
            return coin

    def coin_creator(self):
        self.coin_group.update()
        coin = self.coin_generator()
        if coin != 0:
            self.coin_group.add(coin)
        for coin in self.coin_group:
            if coin.collided_with_player(player.rect):
                coin_soundEffect.play()
                self.coins_collected += 1
                coin.kill()

    def decrease_cost_speed(self):
        self.coins_collected -= speed_button.cost

    def decrease_cost_size(self):
        self.coins_collected -= size_button.cost

    def reset_ball(self):
        if self.ball_group.sprite.rect.right >= screen_width:
            self.opponent_score += 1
            screen.blit(theRockMeme, (screen_width / 2 - 430, screen_height / 2 - 430))
            self.ball_group.sprite.reset_ball()
            losePoint_soundEffect.play(0)
        if self.ball_group.sprite.rect.left <= 0:
            self.player_score += 1
            self.ball_group.sprite.reset_ball()
            winPoint_soundEffect.set_volume(1)
            winPoint_soundEffect.play(0)

    def draw_score(self):
        opponent_score_text = small_score_font.render(str(self.opponent_score), True, light_grey)
        screen.blit(opponent_score_text, (screen_width / 2 - 65, (screen_height - 160) / 2))
        player_score_text = small_score_font.render(str(self.player_score), True, light_grey)
        screen.blit(player_score_text, (screen_width / 2 + 45, (screen_height - 160) / 2))

    def draw_level(self):
        current_level_str = "Level 1"
        if self.current_level == difficulty_level.LEVEL1:
            current_level_str = "Level 1"
        elif self.current_level == difficulty_level.LEVEL2:
            current_level_str = "Level 2"
        elif self.current_level == difficulty_level.LEVEL3:
            current_level_str = "Level 3"

        current_level_text = small_score_font.render(current_level_str, True, game_over_black)
        screen.blit(current_level_text, (75, screen_height - 105))

    def draw_number_of_coins(self):
        coin_number_text = small_score_font.render(str(self.coins_collected), True, game_over_black)
        screen.blit(coin_number_text, (450, screen_height - 105))
        coin_text = small_score_font.render("Coins: ", True, game_over_black)
        screen.blit(coin_text, (300, screen_height - 105))

    def timer(self):
        current_time = pygame.time.get_ticks()
        ticks = current_time - self.start_time
        seconds = int(ticks / 1000 % 60)
        minutes = int(ticks / 60000 % 24)
        out = '{minutes:02d}:{seconds:02d}'.format(minutes=minutes, seconds=seconds)
        out_1 = small_score_font.render(out, True, game_over_black)
        screen.blit(out_1, (screen_width - 200, screen_height - 105))

        if minutes == 1 and self.levelUp_soundEffect_counter == 0:
            self.current_level = difficulty_level.LEVEL2
            levelUp_soundEffect.set_volume(0.5)
            levelUp_soundEffect.play(0)
            self.levelUp_soundEffect_counter += 1

        elif minutes == 2 and self.levelUp_soundEffect_counter == 1:
            self.current_level = difficulty_level.LEVEL3
            levelUp_soundEffect.set_volume(0.5)
            levelUp_soundEffect.play(0)
            self.levelUp_soundEffect_counter += 1

    def game_restart(self):
        ball.reset_ball()
        player.reset_player()
        opponent.reset_player()
        self.paddle_group.update(self.ball_group)

        self.player_score = 0
        self.opponent_score = 0
        self.coins_collected = 0

        self.current_level = difficulty_level.LEVEL1

        self.start_time = pygame.time.get_ticks()

        # Reset the Background counter for background movement and levelUp counter
        self.background_counter = 0
        self.levelUp_soundEffect_counter = 0

        self.last_spawn_time_coin = pygame.time.get_ticks()

        pygame.mixer.music.unload()
        pygame.mixer.music.load('game_background_music.wav')
        pygame.mixer.music.set_volume(0.5)
        pygame.mixer.music.play(-1)

    def pause(self):
        game_restart_flag = False
        self.paused = True
        main_menu_flag = False
        before_pause_time = pygame.time.get_ticks()

        # Locks the moving background in place
        screen.blit(bg_img, (self.background_counter, 0))
        screen.blit(bg_img, (self.background_counter - screen_width, 0))
        if self.background_counter == screen_width:
            screen.blit(bg_img, (self.background_counter - screen_width, 0))
            self.background_counter = 0

        while self.paused:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()

                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_c:
                        self.paused = False

                    elif event.key == pygame.K_r:
                        self.game_restart()
                        self.paused = False
                        game_restart_flag = True

                    elif event.key == pygame.K_m:
                        self.paused = False
                        main_menu_flag = True

                    elif event.key == pygame.K_q:
                        pygame.quit()
                        quit()

            paused_text = paused_font.render('Paused', True, light_grey)
            paused_text_rect = paused_text.get_rect(center=(screen_width / 2, 100))
            screen.blit(paused_text, paused_text_rect)

            extra_text = small_paused_font.render('Press C to continue, Q to quit ', True, light_grey)
            extra_text_rect = extra_text.get_rect(center=(screen_width / 2, 250))
            screen.blit(extra_text, extra_text_rect)

            extra_extra_text = small_paused_font.render('R to restart or M to go to the main menu. ', True, light_grey)
            extra_extra_text_rect = extra_extra_text.get_rect(center=(screen_width / 2, 310))
            screen.blit(extra_extra_text, extra_extra_text_rect)

            # Pause rectangles
            p_left = pygame.Rect(screen_width / 2 - 70, screen_height / 2 - 70, 40, 140)
            pygame.draw.rect(screen, light_grey, p_left)
            p_right = pygame.Rect(screen_width / 2 + 20, screen_height / 2 - 70, 40, 140)
            pygame.draw.rect(screen, light_grey, p_right)

            controls_text = small_paused_font.render('UP key to move up, DOWN key to move down, ', True, light_grey)
            controls_rect = controls_text.get_rect(center=(screen_width / 2, screen_height / 2 + 355))
            screen.blit(controls_text, controls_rect)

            controls_text = small_paused_font.render('P to pause and Q to quit. ', True, light_grey)
            controls_rect = controls_text.get_rect(center=(screen_width / 2, screen_height / 2 + 420))
            screen.blit(controls_text, controls_rect)

            # Score
            opponent_score_text1 = small_score_font.render("Opponent ", True, light_grey)
            screen.blit(opponent_score_text1, (30, 35))
            opponent_score_text1 = small_score_font.render("Score ", True, light_grey)
            screen.blit(opponent_score_text1, (60, 80))

            player_score_text1 = small_score_font.render("Player ", True, light_grey)
            screen.blit(player_score_text1, (screen_width - 185, 35))
            player_score_text1 = small_score_font.render("Score ", True, light_grey)
            screen.blit(player_score_text1, (screen_width - 180, 80))

            opponent_score_text2 = paused_font.render(str(self.opponent_score), True, light_grey)
            screen.blit(opponent_score_text2, (100, 130))
            player_score_text2 = paused_font.render(str(self.player_score), True, light_grey)
            screen.blit(player_score_text2, (screen_width - 140, 130))

            pygame.display.flip()

        if not game_restart_flag and not main_menu_flag:
            after_pause = pygame.time.get_ticks()
            paused_time = after_pause - before_pause_time
            self.start_time += paused_time

        if main_menu_flag:
            self.main_menu()
            self.game_restart()

    def level_checker(self):
        # If the difficulty level is 2 then the ball speed and the opponent speed increase
        if self.current_level == difficulty_level.LEVEL2:
            opponent.speed = 7
            if ball.speed_x < 0 < ball.speed_y:
                ball.speed_x = -4
                ball.speed_y = 4
            elif ball.speed_x < 0 and ball.speed_y < 0:
                ball.speed_y = -4
                ball.speed_x = -4
            elif ball.speed_x > 0 > ball.speed_y:
                ball.speed_y = -4
                ball.speed_x = 4
            elif ball.speed_x > 0 and ball.speed_y > 0:
                ball.speed_y = 4
                ball.speed_x = 4

        # If the difficulty level is 2 then the ball speed and the opponent speed increase
        if self.current_level == difficulty_level.LEVEL3:
            opponent.speed = 10
            if ball.speed_x < 0 < ball.speed_y:
                ball.speed_y = 6
                ball.speed_x = -6
            elif ball.speed_x < 0 and ball.speed_y < 0:
                ball.speed_y = -6
                ball.speed_x = -6
            elif ball.speed_x > 0 > ball.speed_y:
                ball.speed_y = -6
                ball.speed_x = 6
            elif ball.speed_x > 0 and ball.speed_y > 0:
                ball.speed_y = 6
                ball.speed_x = 6

    def main_menu(self):
        main_menu = True

        pygame.mixer.music.load(
            'main_menu_music.wav')
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

                        pygame.mixer.music.unload()
                        pygame.mixer.music.load('game_background_music.wav')
                        pygame.mixer.music.set_volume(0.5)
                        pygame.mixer.music.play(-1)

                        main_menu = False

                    elif event.key == pygame.K_q:
                        pygame.mixer.music.stop()
                        pygame.quit()
                        quit()

            main_menu_text = big_main_menu_font.render('Pong-The-Game', True, light_grey)
            main_menu_rect = main_menu_text.get_rect(center=(screen_width / 2, 120))
            screen.blit(main_menu_text, main_menu_rect)

            controls_text = small_paused_font.render('UP key to move up, DOWN key to move down, ', True, light_grey)
            controls_rect = controls_text.get_rect(center=(screen_width / 2, 270))
            screen.blit(controls_text, controls_rect)

            controls_text = small_paused_font.render('P to pause and Q to quit. ', True, light_grey)
            controls_rect = controls_text.get_rect(center=(screen_width / 2, 340))
            screen.blit(controls_text, controls_rect)

            controls_text = small_paused_font.render('Press SPACE to continue', True, light_grey)
            controls_rect = controls_text.get_rect(center=(screen_width / 2, screen_height / 2 + 410))
            screen.blit(controls_text, controls_rect)

            screen.blit(ball_image, (screen_width/2 - 60, screen_height/2 + 20))
            screen.blit(paddle_image, (screen_width/2 - 315, screen_height/2 - 50))
            screen.blit(paddle_image, (screen_width/2 + 315, screen_height/2 - 50))

            pygame.display.flip()

    def background_movement(self):
        # Background movement
        screen.fill((0, 0, 0))
        screen.blit(bg_img, (self.background_counter, 0))
        screen.blit(bg_img, (self.background_counter - screen_width, 0))
        if self.background_counter == screen_width:
            screen.blit(bg_img, (self.background_counter - screen_width, 0))
            self.background_counter = 0
        self.background_counter += 1

    def game_over_checker(self):
        if self.opponent_score == 5:
            # Stops the gameplay music
            pygame.mixer.music.stop()

            i = 0
            while i != 50:
                spriteFade.update()
                spriteFade.draw(screen)
                clock.tick(30)
                pygame.display.flip()
                i += 1

            game_over = True
            game_restart = False
            main_menu_flag = False
            game_over_soundEffect.play()

            while game_over:
                screen.fill(game_over_black)

                for event in pygame.event.get():
                    if event.type == pygame.QUIT:
                        pygame.quit()
                        sys.exit()

                    if event.type == pygame.KEYDOWN:
                        if event.key == pygame.K_r:
                            game_restart = True
                            game_over = False

                        elif event.key == pygame.K_m:
                            main_menu_flag = True
                            game_over = False

                        elif event.key == pygame.K_q:
                            pygame.mixer.music.stop()
                            pygame.quit()
                            quit()

                game_over_text = big_main_menu_font.render('Game Over', True, light_grey)
                game_over_text_rect = game_over_text.get_rect(center=(screen_width / 2, 400))
                screen.blit(game_over_text, game_over_text_rect)

                text = small_paused_font.render('Press R to restart, Q to quit ', True, light_grey)
                text_rect = text.get_rect(center=(screen_width / 2, 600))
                screen.blit(text, text_rect)

                extra_text = small_paused_font.render('or M to go to the main menu ', True, light_grey)
                extra_text_rect = extra_text.get_rect(center=(screen_width / 2, 650))
                screen.blit(extra_text, extra_text_rect)

                pygame.display.flip()

            if game_restart and not game_over:
                clock.tick(120)
                self.game_restart()

            if main_menu_flag and not game_over:
                clock.tick(120)
                self.game_restart()
                self.main_menu()


# General Setup for the window
pygame.mixer.pre_init(44100, -16, 2, 256)
pygame.init()
clock = pygame.time.Clock()

# Setup for the window where the game will be played
screen_width = 1280
screen_height = 960
screen = pygame.display.set_mode((screen_width, screen_height))
pygame.display.set_caption('Pong-The-Game')

color_bg = pygame.Color('grey12')
bg_img = pygame.image.load('game_background.jpg')
ball_image = pygame.image.load('Ball.png')
paddle_image = pygame.image.load('Paddle.png')

ball_image = pygame.transform.scale(ball_image, (120, 120))
paddle_image = pygame.transform.scale(paddle_image, (20, 280))

light_grey = (200, 200, 200)
white = (255, 255, 255)
game_over_black = (0, 0, 0)
COIN_SPAWN_TIME = 3000

# Sound effects
winPoint_soundEffect = pygame.mixer.Sound('point_won_sound_effect.wav')
losePoint_soundEffect = pygame.mixer.Sound('the_rock_sound_effect.wav')
levelUp_soundEffect = pygame.mixer.Sound('level_up_sound_effect.wav')
collision_ball_player_soundEffect = pygame.mixer.Sound('collision_sound_effect.wav')
game_over_soundEffect = pygame.mixer.Sound('game_over_sound_effect.wav')
coin_soundEffect = pygame.mixer.Sound('coin_sound_effect.wav')
error_soundEffect = pygame.mixer.Sound('error_sound_effect.wav')
upgrade_soundEffect = pygame.mixer.Sound('upgrade_level_up.wav')

# The Rock Image
theRockMeme = pygame.image.load('theRock.jpeg')

# Fonts
button_font = pygame.font.Font('PixeloidSans-JR6qo.ttf', 20)
paused_font = pygame.font.Font('PixeloidSans-JR6qo.ttf', 80)
small_paused_font = pygame.font.Font('PixeloidSans-JR6qo.ttf', 40)
small_score_font = pygame.font.Font('PixeloidSans-JR6qo.ttf', 40)
big_main_menu_font = pygame.font.Font('PixeloidSans-JR6qo.ttf', 100)

# Game Objects
coin_group = pygame.sprite.Group()

player = Player('Paddle.png', screen_width - 20, ((screen_height - 160) / 2), 5)
opponent = Opponent('Paddle.png', 20, ((screen_height - 160) / 2), 5)
paddle_group = pygame.sprite.Group()
paddle_group.add(player)
paddle_group.add(opponent)

spriteFade = pygame.sprite.Group(FadeInBlack())

ball = Ball('Ball.png', screen_width / 2, (screen_height - 160) / 2, 3, 3, paddle_group)
ball_sprite = pygame.sprite.GroupSingle()
ball_sprite.add(ball)

button_group = pygame.sprite.Group()

speed_button = UpgradeSpeed('BotaoSpeed.png', 650, screen_height - 112)
size_button = UpgradeSize('BotaoSize.png', 900, screen_height - 112)
button_group.add(speed_button)
button_group.add(size_button)

game_manager = GameManager(ball_sprite, paddle_group, coin_group, button_group)

# First comes the main menu
game_manager.main_menu()

# Clock timer
game_manager.start_time = pygame.time.get_ticks()

# main game loop
while True:
    # Handling inputs
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

        # When a key is pressed
        if event.type == pygame.KEYDOWN:
            # Movement
            if event.key == pygame.K_DOWN:
                # player_speed += 7
                player.movement += player.speed
            elif event.key == pygame.K_UP:
                # player_speed -= 7
                player.movement -= player.speed

            # For the pause button
            elif event.key == pygame.K_p:
                volume = pygame.mixer.music.get_volume()
                pygame.mixer.music.set_volume(0.1)
                game_manager.pause()
                pygame.mixer.music.set_volume(volume)

            # Speed Button
            elif event.key == pygame.K_e:
                speed_button.upgrade_button()

            # Size button
            elif event.key == pygame.K_r:
                size_button.upgrade_button()

            elif event.key == pygame.K_q:
                pygame.quit()
                quit()

        # When a key is released
        if event.type == pygame.KEYUP:
            # Movement
            if event.key == pygame.K_DOWN:
                player.movement -= player.speed
            elif event.key == pygame.K_UP:
                player.movement += player.speed

    # Now to make things easier with classes we just make this
    game_manager.run_game()

    # Updating the window
    pygame.display.flip()
    # Controlling the speed
    clock.tick(120)
