import pygame
import sys

pygame.init()
pygame.display.set_caption('Cross Zeros')
ICON = pygame.image.load('Pygame trainnig\index.png')
pygame.display.set_icon(ICON)

SIZE_BLOCK = 100
MARGIN = 15
WIDTH = HIGHT = SIZE_BLOCK*3 + MARGIN*4
SCREEN = pygame.display.set_mode((WIDTH, HIGHT))

RED = (255,0,0)
GREEN = (0,255,0)
WHITE = (255,255,255)

mas = [[0]*3 for i in range(3)]
QUERY = 0

while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit(0)
        if event.type == pygame.MOUSEBUTTONDOWN:
            x_mouse, y_mouse = pygame.mouse.get_pos()
            row = x_mouse // (MARGIN + SIZE_BLOCK)
            col = y_mouse // (MARGIN + SIZE_BLOCK)

            if mas[row][col] == 0:
                if QUERY %2:
                    mas[row][col] = 'x'
                else:
                    mas[row][col] = 'o'
                QUERY += 1
    
    for row in range(3):
        for col in range(3):
            if mas[row][col] == 'x':
                color = RED
            elif mas[row][col] == 'o':
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

    pygame.display.update()
