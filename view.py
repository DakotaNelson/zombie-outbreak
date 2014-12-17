import pygame
import tiles

class View:
    def __init__(self, size, grid):
        self.size = size
        h = size
        w = size
        # space to leave on bottom for text
        bottom_margin = 50
        self.squareHeight = h / grid.h # how big to make each square on the map
        self.squareWidth = w / grid.w
        self.maxH = grid.h - 1
        self.maxW = grid.w - 1
        self.screen = pygame.display.set_mode((w,h+bottom_margin))
        pygame.display.set_caption("Zombie Outbreak Simulation")
        self.font = pygame.font.SysFont("monospace", 24)

    def update(self, data, res):
        self.screen.fill((255,255,255))

        #draw tiles for map
        for row in data.grid:
            for tile in row:
                rect = (tile.x * self.squareWidth,
                        tile.y * self.squareHeight,
                        self.squareWidth,
                        self.squareHeight)
                pygame.draw.rect(self.screen, tile.color(), rect, 0)

        # now draw text
        airstrikes = "Airstrikes: " + str(int(res.airstrikes))
        label = self.font.render(airstrikes, 1, (0, 0, 0))
        self.screen.blit(label, (5,self.size+5))

        totalHumans = "Total humans: " + str(data.totalHumans())
        label = self.font.render(totalHumans, 1, (0, 0, 0))
        self.screen.blit(label, (150,self.size+5))

        # and make a screen refresh happen
        pygame.display.update()

    def getGridLocation(self, pos):
        # given x,y in pixels, return x,y in grid location
        x = pos[0]
        y = pos[1]
        column = x // self.squareWidth
        row = y // self.squareHeight
        if column > self.maxH: column = self.maxH
        if row > self.maxW: row = self.maxW
        return [column,row]

