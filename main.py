import pygame
from crossy_roads import Crossy_roads
from agent import Agent
game = Crossy_roads()
pygame.init()
pygame.display.set_caption("Crossy Chris")
normal_logo = pygame.image.load("./normal_logo.png")
pygame.display.set_icon(normal_logo)
clock = pygame.time.Clock()

running = True
tile_size = 50

agent = Agent(game)

while running:
    if not game.play():
        running = False

    #game.map.draw_grid(screen)
    game.frames_passed += 1
    clock.tick(30)


pygame.quit()