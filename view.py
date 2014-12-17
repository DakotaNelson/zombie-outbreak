import pygame
import tiles

class View:
    def __init__(self, size, grid):
        h = size
        w = size
        self.screen = pygame.display.set_mode((w,h))
        self.grid = grid
        pygame.display.set_caption("Zombie Outbreak Simulation")
        self.squareHeight = h / grid.h # how big to make each square on the map
        self.squareWidth = w / grid.w
        pygame.display.update()

    def update(self):
        self.screen.fill((255,255,255))
        for row in self.grid.grid:
            for tile in row:
                rect = (tile.x * self.squareWidth,
                        tile.y * self.squareHeight,
                        self.squareWidth,
                        self.squareHeight)
                pygame.draw.rect(self.screen, tile.color(), rect, 0)
        pygame.display.update()

    def getGridLocation(self, pos):
        # given x,y in pixels, return x,y in grid location
        x = pos[0]
        y = pos[1]
        column = x // self.squareWidth
        row = y // self.squareHeight
        return [row,column]

