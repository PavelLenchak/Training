import sys
import pygame
import time
import random

class Game():
    def __init__(self):
        # basic colors
        self.WHITE = (255,255,255)
        self.BLACK = (0,0,0)
        self.RED = (255,0,0)
        self.GREEN = (0,255,0)
        self.BLUE =(0,244,204)

        self.size_block = 15
        self.margin = 1
        self.count_block = 30
        self.captiom = 'Snake'
        self.board_color = self.BLACK

        self.screen_w = self.screen_h = self.size_block*self.count_block + self.margin*(self.count_block+1)
        self.window = (self.screen_w, self.screen_h)

        self.fps_controller = pygame.time.Clock()
        self.FPS = 30

        # count food
        self.score = 0

    def init_and_check_errors(self):
        check_errors = pygame.init()
        if check_errors[1] > 0:
            sys.exit(0)
        else:
            print('OK')

    def set_surface_and_title(self):
        self.screen = pygame.display.set_mode(self.window)
        pygame.display.set_caption(self.captiom)
        self.screen.fill(self.board_color)

    def event_loop(self, change_to):
        """ Отслеживание нажатий клавиш """

        for event in pygame.event.get():
            if event.type == pygame.K_UP:
                change_to = 'UP'
            elif event.type == pygame.K_DOWN:
                change_to = 'DOWN'
            elif event.type == pygame.K_RIGHT:
                change_to = 'RIGHT'
            elif event.type == pygame.K_LEFT:
                change_to = 'LEFT'
            elif event.type == pygame.K_ESCAPE:
                pygame.quit()
                sys.exit(0)

        return change_to

    def refresh_screen(self):
        pygame.display.update()
        self.fps_controller.tick(self.FPS)

    def show_score(self, status = 1):
        score_font = pygame.font.SysFont('monaco', 24)
        score_surf = score_font.render(
            'Score: {}'.format(self.score), True, self.BLACK
        )
        score_rect = score_surf.get_rect()

        if status == 1:
            score_rect.midtop = (10,10)
        else:
            score_rect.midtop = (self.screen_w//2, self.screen_h//2)

        self.screen.blit(score_surf, score_rect)


    def game_over(self):
        game_over_font = pygame.font.SysFont('monaco', 30)
        game_over_surf = game_over_font.render(
            'GAME OVER', True, self.BLACK
        )
        game_over_rect = game_over_surf.get_rect()
        game_over_rect.midtop = ((self.screen_w//2, self.screen_h//2 - 50))
        self.screen.blit(game_over_surf, game_over_rect)

        self.show_score(0)
        pygame.display.update()
        time.sleep(4)
        pygame.quit()
        sys.exit(0)


class Snake():
    def __init__(self, snake_color):
        self.snake_color = snake_color

        self.snake_head_pos = [100, 50]
        self.snake_body = [[100,50], [90,50], [80,50]]
        self.direction = 'RIGHT'

        self.change_to = self.direction

    def check_direction_and_change(self):
        if any(
            self.change_to == 'UP' and not self.direction == 'DOWN',
            self.change_to == 'DOWN' and not self.direction == 'UP',
            self.change_to == 'RIGHT' and not self.direction == 'LEFT',
            self.change_to == 'LEFT' and not self.direction == 'RIGHT',):

            self.direction = self.change_to

    def change_head_postion(self):
        if self.direction == 'UP':
            self.snake_head_pos[1] -= 10
        elif self.direction == 'DOWN':
            self.snake_head_pos[1] += 10
        elif self.direction == 'LEFT':
            self.snake_head_pos[0] -= 10 
        elif self.direction == 'RIGHT':
            self.snake_head_pos[0] += 10 


    def snake_body_mechnism(self, score, food_pos, screen_width, screen_hight):

        self.snake_body = (0, list(self.snake_head_pos))

        if self.snake_head_pos[0] == food_pos[0] and self.snake_head_pos[1] == food_pos[1]:
            
            food_pos = [
                random.randrange(1, screen_width/10)*10,
                random.randrange(1, screen_hight/10)*10
            ]
            score += 1
        else:
            self.snake_body.pop()

        return score, food_pos

    
    def draw_snake(self, play_surface, surface_color):
        play_surface.fill(surface_color)

        for pos in self.snake_body:
            pygame.draw.rect(
                play_surface, self.snake_color, pygame.Rect(
                    pos[0], pos[1], 10, 10)
            )

    def check_for_bounderies(self, game_over, screen_width, screen_height):
        if any((
                self.snake_head_pos[0] > screen_width-10 or self.snake_head_pos[0] < 0,
                self.snake_head_pos[1] > screen_height-10 or self.snake_head_pos[1] < 0
                    )):
                game_over()
        for block in self.snake_body[1:]:
            # проверка на то, что первый элемент(голова) врезался в
            # любой другой элемент змеи (закольцевались)
            if (block[0] == self.snake_head_pos[0] and
                    block[1] == self.snake_head_pos[1]):
                game_over()


class Food():
        def __init__(self, food_color, screen_width, screen_height):
            """Инит еды"""
            self.food_color = food_color
            self.food_size_x = 10
            self.food_size_y = 10
            self.food_pos = [random.randrange(1, screen_width/10)*10,
                            random.randrange(1, screen_height/10)*10]
            
            print('OOOOOOOOOOOOOO {}'.format(self.food_pos))

        def draw_food(self, play_surface):
            """Отображение еды"""
            pygame.draw.rect(
                play_surface, self.food_color, pygame.Rect(
                    self.food_pos[0], self.food_pos[1],
                    self.food_size_x, self.food_size_y))


game = Game()
snake = Snake(game.GREEN)
food = Food(game.RED, game.screen_w, game.screen_h)

game.init_and_check_errors()
game.set_surface_and_title()

done = False
while not done:
    snake.change_to = game.event_loop(snake.change_to)

    snake.validate_direction_and_change()
    snake.change_head_position()
    game.score, food.food_pos = snake.snake_body_mechanism(
        game.score, food.food_pos, game.screen_width, game.screen_height)
    snake.draw_snake(game.play_surface, game.white)

    food.draw_food(game.play_surface)

    snake.check_for_boundaries(
        game.game_over, game.screen_width, game.screen_height)

    game.show_score()
    game.refresh_screen()
