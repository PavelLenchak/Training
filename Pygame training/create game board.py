import pygame
import sys

pygame.init()

SIZE = (510, 510)
SCREEN = pygame.display.set_mode(SIZE)
IMG = pygame.image.load('Pygame training\Crosses zeroes\index.png')
pygame.display.set_icon(IMG)
pygame.display.set_caption('Game board')

RED = (255, 0, 0)
WHITE = (255, 255, 255)
MARGIN = 10
WIDTH = HIGHT = 40

mas = [[0]*10 for i in range(10)]

while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            quit()
            sys.exit(0)
        elif event.type == pygame.MOUSEBUTTONDOWN:
            x_mouse, y_mouse = pygame.mouse.get_pos()
            print('X pos = {}, Y pos = {}'.format(x_mouse,y_mouse))
            column = x_mouse // (MARGIN + WIDTH)
            row = y_mouse // (MARGIN + HIGHT)
            mas[row][column] ^= 1

    for row in range(10):
        for col in range(10):
            if mas[row][col] == 1:
                color = RED
            else:
                color = WHITE
            x = col * WIDTH + (col+1) * MARGIN
            y = row * HIGHT + (row+1) * MARGIN
            pygame.draw.rect(SCREEN, color, (x, y, WIDTH, HIGHT))
    pygame.display.update()