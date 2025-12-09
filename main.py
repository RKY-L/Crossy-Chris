import pygame
from crossy_roads import *
from agent import *
game = Crossy_roads()
pygame.init()
pygame.display.set_caption("Crossy Chris")
normal_logo = pygame.image.load("./normal_logo.png")
pygame.display.set_icon(normal_logo)
clock = pygame.time.Clock()

running = True
tile_size = 50
train()

pygame.quit()