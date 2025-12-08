import pygame
from crossy_roads import Crossy_roads
game = Crossy_roads()
pygame.init()
pygame.display.set_caption("Crossy Chris")
normal_logo = pygame.image.load("./normal_logo.png")
pygame.display.set_icon(normal_logo)
clock = pygame.time.Clock()

running = True
tile_size = 50


while running:
    if game.play() == None:
        print("telling game to quit")
        running = False

    #game.map.draw_grid(screen)
    game.frames_passed += 1
    clock.tick(30)


pygame.quit()