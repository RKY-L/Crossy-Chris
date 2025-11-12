import pygame

pygame.init()
pygame.display.set_caption("Crossy Chris")
normal_logo = pygame.image.load("./normal_logo.png")
pygame.display.set_icon(normal_logo)
SCREEN_W, SCREEN_H = 600, 900
screen = pygame.display.set_mode((SCREEN_W, SCREEN_H))

screen.fill((255, 255, 255))
clock = pygame.time.Clock()

running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False


    time_delta = clock.tick(30)
    pygame.display.flip()


pygame.quit()