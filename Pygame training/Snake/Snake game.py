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

        self.size_block = 30
        self.margin = 1
        self.under_margin = 25
        self.count_block = 20
        self.captiom = 'Snake'
        self.board_color = self.BLACK

        self.screen_w = self.screen_h = self.size_block*self.count_block + self.margin*(self.count_block+1)
        self.window = (self.screen_w, self.screen_h + self.under_margin)

        self.fps_controller = pygame.time.Clock()
        self.FPS = 5

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


    def draw_the_blocks(self, color, row, column):
        x = self.size_block * row + self.margin * (row + 1)
        y = self.size_block * column + self.margin * (column + 1)
        pygame.draw.rect(self.screen, color, (x, y, self.size_block, self.size_block))


    def draw_the_game_board(self):
        for row in range(self.count_block):
            for column in range(self.count_block):
                if (row + column) % 2 == 0:
                    self.color = self.WHITE
                else:
                    self.color = self.BLUE

                game.draw_the_blocks(self.color, row, column)
                

    def event_loop(self, change_to):
        """ Отслеживание нажатий клавиш """

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit(0)
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_UP or event.key == ord('w'):
                    change_to = 'UP'
                elif event.key == pygame.K_DOWN or event.key == ord('s'):
                    change_to = 'DOWN'
                elif event.key == pygame.K_RIGHT or event.key == ord('d'):
                    change_to = 'RIGHT'
                elif event.key == pygame.K_LEFT or event.key == ord('a'):
                    change_to = 'LEFT'
                elif event.key == pygame.K_ESCAPE:
                    pygame.quit()
                    sys.exit(0)

        return change_to

    def refresh_screen(self):
        pygame.display.flip()
        self.fps_controller.tick(self.FPS)

    def show_score(self, status = 1):
        score_font = pygame.font.SysFont('monaco', 36)
        score_surf = score_font.render(
            'Score: {0}'.format(self.score), True, self.WHITE, self.BLACK)
        score_rect = score_surf.get_rect()

        if status == 1:
            score_rect.midtop = (self.screen_w//2, self.screen_h * 0.999)
        else:
            score_rect.midtop = (self.screen_w//2, self.screen_h//2)

        self.screen.blit(score_surf, score_rect)


    def game_over(self):
        self.screen.fill(self.BLACK)
        game_over_font = pygame.font.SysFont('KOYSAN', 30)
        game_over_surf = game_over_font.render(
            'GAME OVER', True, self.BLUE
        )
        game_over_rect = game_over_surf.get_rect()
        game_over_rect.midtop = ((self.screen_w//2, self.screen_h//2 - 50))
        self.screen.blit(game_over_surf, game_over_rect)

        self.show_score(0)
        pygame.display.update()
        time.sleep(1)
        pygame.quit()
        sys.exit(0)


class Snake():
    def __init__(self, snake_color):
        self.snake_color = snake_color
        self.direction = 'RIGHT'
        self.snake_speed = 1
        self.x = 10
        self.y = 10
        self.snake_pos = [
            [self.x, self.y],
        ]

        self.chanched_to = self.direction
    

    def check_crash(self):

        # Столкновение со стенкой
        if not -1 <= self.x <= game.count_block or not -1 <= self.y <= game.count_block:
            game.game_over()

        # Столкновение с телом
        for block in self.snake_pos[1:]:
            if (block[0] == self.snake_pos[0][0] and 
                block[1] == self.snake_pos[0][1]):
                game.game_over()

        
    def check_eat(self):
        if self.snake_pos[0][0] == food.food_pos[0] and self.snake_pos[0][1] == food.food_pos[1]:
            game.score += 1
            snake.snake_pos.append(food.food_pos)
            food.food_pos = [random.randint(1, game.count_block-1),
                            random.randint(1, game.count_block-1)]
            print('YUMMY')
            

    def move_on(self):
        if any((self.direction == 'UP' and not self.chanched_to == 'DOWN',
                self.direction == 'DOWN' and not self.chanched_to == 'UP',
                self.direction == 'RIGHT' and not self.chanched_to == 'LEFT',
                self.direction == 'LEFT' and not self.chanched_to == 'RIGHT')):
            self.direction = self.chanched_to

        # Двигаемся в сторону
        if self.direction == 'UP':
            self.y -= self.snake_speed
        elif self.direction == 'DOWN':
            self.y += self.snake_speed
        elif self.direction == 'RIGHT':
            self.x += self.snake_speed
        elif self.direction == 'LEFT':
            self.x -= self.snake_speed

        for block in self.snake_pos:
            x, y = block
            game.draw_the_blocks(self.snake_color, x, y)

        self.snake_pos.append([self.x, self.y])
        self.snake_pos = self.snake_pos[1:]

        # Проверяем столкновение со стенкой или с телом змейки
        self.check_crash()
        self.check_eat()
        

class Food():
    def __init__(self, food_color):
        self.food_color = food_color
        self.food_pos = [random.randint(1, game.count_block-1),
                        random.randint(1, game.count_block-1)]

    def draw_food(self):
        game.draw_the_blocks(self.food_color, self.food_pos[0], self.food_pos[1])


game = Game()
snake = Snake(game.GREEN)
food = Food(game.RED)

game.init_and_check_errors()
game.set_surface_and_title()


while True:
    game.draw_the_game_board()
    
    snake.chanched_to = game.event_loop(snake.chanched_to)
    snake.move_on()
    print(snake.snake_pos)

    food.draw_food()

    game.show_score()
    game.refresh_screen()

    
