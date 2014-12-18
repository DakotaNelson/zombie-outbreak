import pygame
from model import Grid, Resources, Metadata
from view import View
from controller import Controller

pygame.init()

# Loop until the user clicks the close button.
done = False

# Used to manage how fast the screen updates
clock = pygame.time.Clock()

# initialize the map
data = Grid(50)

# init the view of the map
view = View(750, data)

# init the controller
con = Controller()

# init the global resources count
res = Resources(1) # 1 = easiest difficulty, 5 = hardest

# init the random data class
metadata = Metadata(data)

# max fps at which to run
fps = 10
counter = 0

# -------- Main Program Loop -----------
while not done:
    for event in pygame.event.get(): # User did something

        if event.type == pygame.QUIT: # If user clicked close
            done = True # Flag that we are done so we exit this loop

        if event.type == pygame.MOUSEBUTTONDOWN:
            pos = pygame.mouse.get_pos()
            gridPos = view.getGridLocation(pos)
            if event.button == 1:
                con.airstrike(gridPos, data, res)
            elif event.button == 3:
                con.infantry(gridPos, data, res)

    if counter == 0:
        # only update once per second (n ticks)
        metadata.update()
        data.update() # update the map (steps all of the diff. eqs. forward one)
        view.update(data, metadata, res)

    counter = (counter+1) % (fps/10)

    clock.tick(fps) # max fps

pygame.quit()
