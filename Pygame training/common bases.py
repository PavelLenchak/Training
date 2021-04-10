import pygame

pygame.init()

SCREEN_W, SCREEN_H = 400,400
WINDOW = (SCREEN_W, SCREEN_H)
ICON = pygame.image.load('Pygame training\Crosses zeroes\index.png')

SCREEN = pygame.display.set_mode(WINDOW, pygame.RESIZABLE)
pygame.display.set_icon(ICON)
pygame.display.set_caption('Basics')

clock = pygame.time.Clock()
FPS = 60

WHITE = (255, 255, 255)
RED = (255,0,0)
BLUE = (0,0,255)
GREEN = (0,255,0)
BLACK = (0,0,0)

pygame.draw.rect(SCREEN, WHITE, (50,50,100,100))
pygame.draw.rect(SCREEN, WHITE, (10,10,40,40), 2)

done = False
while not done:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            done = True

    pygame.display.update()
    clock.tick(FPS)

pygame.quit