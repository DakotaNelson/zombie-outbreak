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

    def update(self, data, metadata, res):
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
        '''day = "Day: " + str(metadata.days)
        day_text = self.font.render(day, 1, (0, 0, 0))
        self.screen.blit(day_text, (sum(padding),self.size+5))
        padding.append(self.font.size(day)[0] + margin)

        totalHumans = "Total humans: " + str(data.totalHumans())
        humans_text = self.font.render(totalHumans, 1, (0, 0, 0))
        self.screen.blit(humans_text, (sum(padding),self.size+5))
        padding.append(self.font.size(totalHumans)[0] + margin)

        totalZombies = "Total zombies: " + str(data.totalZombies())
        zombies_text = self.font.render(totalZombies, 1, (0, 0, 0))
        self.screen.blit(zombies_text, (sum(padding),self.size+5))
        padding.append(self.font.size(totalZombies)[0] + margin)

        totalCasualties = "Total casualties: " + str(data.totalDead())
        casualties_text = self.font.render(totalCasualties, 1, (0, 0, 0))
        self.screen.blit(casualties_text, (sum(padding),self.size+5))
        padding.append(self.font.size(totalCasualties)[0] + margin)'''

        # display row one
        day = "Day: " + str(metadata.days)
        initialHumans = "Starting humans: " + str(metadata.initialHumans)
        totalHumans = "Living: " + str(data.totalHumans())
        totalZombies = "Zombies: " + str(data.totalZombies())
        totalCasualties = "Dead: " + str(data.totalDead())
        row1 = [day, initialHumans, totalHumans, totalZombies, totalCasualties]
        row1_size = self.displayRow(row1, self.size + 5)

        # display row two
        airstrikes = "Airstrikes: " + str(int(res.airstrikes))
        infantry = "Infantry: " + str(int(res.infantry))
        row2_size = self.displayRow([airstrikes, infantry], self.size + row1_size[1])

        # and make a screen refresh happen
        pygame.display.update()

    def displayRow(self, strings, height, left=0, margin=20):
        # strings: to display
        # height: height at which to put top left corner
        # left: left padding before row starts
        # margin: pixels between strings
        padding = []
        padding.append(margin/2 + left)

        for text in strings:
            rendered = self.font.render(text, 1, (0, 0, 0))
            self.screen.blit(rendered, (sum(padding), height))
            padding.append(self.font.size(text)[0] + margin)
        # return width and height to enable placement around it
        return (sum(padding), self.font.size(strings[0])[1] + 8)


    def getGridLocation(self, pos):
        # given x,y in pixels, return x,y in grid location
        x = pos[0]
        y = pos[1]
        column = x // self.squareWidth
        row = y // self.squareHeight
        if column > self.maxH: column = self.maxH
        if row > self.maxW: row = self.maxW
        return [column,row]

