import pygame
import sys

class Ball(pygame.sprite.Sprite):
    def __init__(self, x, speed, file_name):
        print(file_name)
        super().__init__()
        self.image = pygame.image.load(file_name).convert_alpha()
        self.rect = self.image.get_rect(center=(x,0))
        self.speed = speed

    def update(self, *args):
        if self.rect.y < args[0] - 20:
            self.rect.y += self.speed
        else:
            self.rect.y = 0

pygame.init()

BLACK = (0,0,0)
SCREEN_WEIGHT, SCREEN_HIGHT = 1200, 600
WINDOW = (SCREEN_WEIGHT, SCREEN_HIGHT)

SCREEN = pygame.display.set_mode(WINDOW)
BG = pygame.image.load('Pygame training\\images\\bg.jpg').convert()

CLOCK = pygame.time.Clock()
FPS = 60

ball = Ball(SCREEN_WEIGHT//2, 2, 'Pygame training\\images\\ball.png')

while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit(0)

    SCREEN.blit(BG, (0,0))
    SCREEN.blit(ball.image, ball.rect)
    pygame.display.update()

    CLOCK.tick(FPS)

    ball.update(SCREEN_HIGHT)