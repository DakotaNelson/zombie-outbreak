import pygame
import tiles

class View:
    def __init__(self, w, h, grid):
        self.screen = pygame.display.set_mode((w,h))
        pygame.display.set_caption("Zombie Outbreak Simulation")
        self.squareHeight = h / grid.h # how big to make each square on the map
        self.squareWidth = w / grid.w
        self.screen.fill((255,255,255))
        for row in grid.grid:
            for tile in row:
                rect = (tile.x * self.squareHeight,
                        tile.y * self.squareHeight,
                        self.squareHeight,
                        self.squareWidth)
                pygame.draw.rect(self.screen, tile.color(), rect, 0)
                print rect
        pygame.display.update()

    def update(self):
        pygame.display.update()
