import pygame
import tiles

class View:
    def __init__(self, size, grid):
        h = size
        w = size
        self.screen = pygame.display.set_mode((w,h))
        pygame.display.set_caption("Zombie Outbreak Simulation")
        self.squareHeight = h / grid.h # how big to make each square on the map
        self.squareWidth = w / grid.w
        self.update(grid)

    def update(self, data):
        self.screen.fill((255,255,255))
        for row in data.grid:
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
        column = y // self.squareWidth
        row = x // self.squareHeight
        return [row,column]

