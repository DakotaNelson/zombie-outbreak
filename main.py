import pygame
from model import Grid
from view import View

pygame.init()

# Loop until the user clicks the close button.
done = False

# Used to manage how fast the screen updates
clock = pygame.time.Clock()

# initialize the map
land = Grid(100,100)

# init the view of the map
display = View(800, 800, land)

# -------- Main Program Loop -----------
while not done:
    for event in pygame.event.get(): # User did something
        if event.type == pygame.QUIT: # If user clicked close
            done = True # Flag that we are done so we exit this loop

    #land.update() # update the map (steps all of the diff. eqs. forward one)
    display.update()


    clock.tick(20) # 20 fps

pygame.quit()
