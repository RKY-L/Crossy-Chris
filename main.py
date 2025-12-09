import pygame
from game.crossy_roads import *
game = Crossy_roads()
pygame.init()
pygame.display.set_caption("Crossy Chris")
normal_logo = pygame.image.load("./game/normal_logo.png")
pygame.display.set_icon(normal_logo)
clock = pygame.time.Clock()

running = True
tile_size = 50
while running:
    reward, done = None, None
    reward,done = game.play()
    if reward == None:
        running = False
    

    #game.map.draw_grid(screen)
    game.frames_passed += 1
    clock.tick(30)


pygame.quit()