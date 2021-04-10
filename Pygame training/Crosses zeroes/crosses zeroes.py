import pygame
import sys

def check_win(mas, sign):
    zeroes = 0
    for row in mas:
        if row.count(sign) == 3:
            return 'The winner is {}'.format(sign)

    for col in range(3):
        if mas[0][col] == sign and mas[1][col] == sign and mas[2][col] == sign:
            return 'The winner is {}'.format(sign)
    
    if mas[0][0] == sign and mas[1][1] == sign and mas[2][2] == sign:
        return 'The winner is {}'.format(sign)

    if mas[2][0] == sign and mas[1][1] == sign and mas[0][2] == sign:
        return 'The winner is {}'.format(sign)

    for row in range(3):
        for col in range(3):
            if mas[row][col] == 0:
                zeroes += 1

    if zeroes == 0:
        return 'Ooops is Draw'

    return False


pygame.init()
pygame.display.set_caption('Crosses and Zeroes')
ICON = pygame.image.load('Pygame training\Crosses zeroes\index.png')
pygame.display.set_icon(ICON)

SIZE_BLOCK = 200
MARGIN = 15
WIDTH = HIGHT = SIZE_BLOCK*3 + MARGIN*4
SCREEN = pygame.display.set_mode((WIDTH, HIGHT))

RED = (255,0,0)
GREEN = (0,255,0)
WHITE = (255,255,255)
BLACK = (0,0,0)

mas = [[0]*3 for i in range(3)]
QUERY = 0
GAME_OVER = False

while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit(0)
        elif event.type == pygame.MOUSEBUTTONDOWN and not GAME_OVER:
            x_mouse, y_mouse = pygame.mouse.get_pos()
            row = x_mouse // (MARGIN + SIZE_BLOCK)
            col = y_mouse // (MARGIN + SIZE_BLOCK)

            if mas[row][col] == 0:
                if QUERY %2 == 0:
                    mas[row][col] = 'X'
                else:
                    mas[row][col] = 'O'
                QUERY += 1
        elif event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
            SCREEN.fill(BLACK)
            mas = [[0]*3 for i in range(3)]
            QUERY = 0
            GAME_OVER = False
    
    if not GAME_OVER:
        for row in range(3):
            for col in range(3):
                if mas[row][col] == 'X':
                    color = RED
                elif mas[row][col] == 'O':
                    color = GREEN
                else:
                    color = WHITE

                x = row * SIZE_BLOCK + (row + 1) * MARGIN
                y = col * SIZE_BLOCK + (col + 1) * MARGIN
                pygame.draw.rect(SCREEN,color, (x,y,SIZE_BLOCK,SIZE_BLOCK))

                if color == RED:
                    pygame.draw.line(SCREEN, WHITE, (x+5, y+5), (x+SIZE_BLOCK-5, y+SIZE_BLOCK-5), 3)
                    pygame.draw.line(SCREEN, WHITE, (x+SIZE_BLOCK-5, y+5), (x+5, y+SIZE_BLOCK-5), 3)
                elif color == GREEN:
                    pygame.draw.circle(SCREEN,WHITE, (x+SIZE_BLOCK//2, y+SIZE_BLOCK//2), SIZE_BLOCK//2-5, 3)

    if (QUERY-1) % 2 == 0:
        GAME_OVER = check_win(mas, 'X')
    else:
        GAME_OVER = check_win(mas, 'O')

    if GAME_OVER:
        SCREEN.fill(BLACK)
        font = pygame.font.SysFont('stxginkai', 80)
        text = font.render(GAME_OVER, True, WHITE)
        text_rect = text.get_rect()
        text_x = SCREEN.get_width()/2 - text_rect.width / 2
        text_y = SCREEN.get_height()/2 - text_rect.height / 2
        SCREEN.blit(text, [text_x, text_y])

    pygame.display.update()
