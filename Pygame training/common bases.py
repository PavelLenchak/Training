import pygame

pygame.init()

SCREEN_W, SCREEN_H = 400,400
WINDOW = (SCREEN_W, SCREEN_H)
ICON = pygame.image.load('Pygame training\Crosses zeroes\index.png')

pygame.display.set_mode(WINDOW, pygame.RESIZABLE)
pygame.display.set_icon(ICON)
pygame.display.set_caption('Basics')

clock = pygame.time.Clock()
FPS = 60

done = False
while not done:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            done = True

    clock.tick(FPS)

pygame.quit