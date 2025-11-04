import pygame

# -- CONSTANTS -- #

# -- Element sizes -- #
WINDOW_WIDTH = 1280
WINDOW_HEIGHT = 1024

SPACESHIP_HEIGHT = 100
SPACESHIP_WIDTH = 100

# -- Colours -- #
SPACE_GREY = ( 25,  25,  25)

pygame.init()

window_size = (WINDOW_WIDTH, WINDOW_HEIGHT)
window = pygame.display.set_mode(window_size)
pygame.display.set_caption('Asteroids')

spaceship = pygame.image.load('images/ship.png').convert_alpha(window)
spaceship = pygame.transform.scale(spaceship, (SPACESHIP_WIDTH, SPACESHIP_HEIGHT))

gameOver = False
time = pygame.time.Clock()

while not gameOver:

    # -- Traitement entrées joueur -- #
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            gameOver = True
    
    window.fill(SPACE_GREY)
    window.blit(spaceship, (WINDOW_WIDTH//2, WINDOW_HEIGHT//2))

    pygame.display.flip()
    
    time.tick(10)

pygame.display.quit()
pygame.quit()
exit()
