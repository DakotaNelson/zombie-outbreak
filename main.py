import pygame
from model import Grid, Resources
from view import View
from controller import Controller

pygame.init()

# Loop until the user clicks the close button.
done = False

# Used to manage how fast the screen updates
clock = pygame.time.Clock()

# initialize the map
data = Grid(100)

# init the view of the map
view = View(800, data)

# init the controller
con = Controller()

# init the global resources count
res = Resources(1) # 1 = easiest difficulty, 5 = hardest

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
            con.airstrike(gridPos, data, res)

    if counter == 0:
        # only update once per second (n ticks)
        data.update() # update the map (steps all of the diff. eqs. forward one)
        view.update(data, res)

    counter = (counter+1) % fps

    clock.tick(fps) # max fps

pygame.quit()
