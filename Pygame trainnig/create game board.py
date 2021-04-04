import pygame
import sys

pygame.init()

SCREEN = (510, 510)
IMG = pygame.image.load('Pygame trainnig\index.png')
RED = (255, 0, 0)
WHITE = (255, 255, 255)
WIDTH = HIGHT = 40

pygame.display.set_mode(SCREEN)
pygame.display.set_icon(IMG)
pygame.display.set_caption('Cross zero')


while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            quit()
            sys.exit()
        elif event.type == pygame.MOUSEBUTTONDOWN:
            x_mouse, y_mouse = pygame.mouse.get_pos()
            print('X pos = {}, Y pos = {}'.format(x_mouse,y_mouse))

