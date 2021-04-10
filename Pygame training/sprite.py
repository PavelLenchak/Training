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

# Использоваение sprite в группе объектов
balls = pygame.sprite.Group()
balls.add(Ball(SCREEN_WEIGHT//2, 2, 'Pygame training\\images\\ball.png'))
balls.add(Ball(SCREEN_WEIGHT//2+250, 2, 'Pygame training\\images\\ball.png'),
          Ball(SCREEN_WEIGHT//2-500, 2, 'Pygame training\\images\\ball.png'))
# ball1 = Ball(SCREEN_WEIGHT//2, 2, 'Pygame training\\images\\ball.png')
# ball2 = Ball(SCREEN_WEIGHT//2+250, 2, 'Pygame training\\images\\ball.png')
# ball3 = Ball(SCREEN_WEIGHT//2-500, 2, 'Pygame training\\images\\ball.png')

while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit(0)

    SCREEN.blit(BG, (0,0))

    # Прорисовываем группу мячиков
    balls.draw(SCREEN)
    # SCREEN.blit(ball1.image, ball1.rect)
    # SCREEN.blit(ball2.image, ball2.rect)
    # SCREEN.blit(ball3.image, ball3.rect)
    pygame.display.update()

    CLOCK.tick(FPS)

    balls.update(SCREEN_HIGHT)
    # ball1.update(SCREEN_HIGHT)
    # ball2.update(SCREEN_HIGHT)
    # ball3.update(SCREEN_HIGHT)