import pygame
import math
import random
# region # -- CONSTANTS -- #
# -- Element sizes -- #
WINDOW_SIZE = (1280, 1024)

X = 0
Y = 1
FPS = 50
PI = math.pi
LINE = 2

# -- Ship constants --
SHIP_R = 25

# -- Asteroid constants --
BIG_A_R = 40

# -- Keyboard keys -- #
TURN_LEFT = pygame.K_LEFT
TURN_RIGHT = pygame.K_RIGHT
ACCELERATE = pygame.K_UP
SHOOT = pygame.K_SPACE

# -- Colours -- #
SPACE_GREY = ( 20,  20,  20)
LIGHT_BLUE = (220, 235, 255)

# endregion

# region # -- FUNCTIONS -- #

# region ### ENTITY ###

def new_entity():
    return {
        'visible':False,
        'position': [0,0],
        'angle': 0,
        'pointList': [[0,0],[1,1]],
        'rModList': [],
        'speed': [0,0],
        'acceleration': [0,0],
        'propulsion': 0
    }

def visible(entity):
    entity['visible'] = True

def invisble(entity):
    entity['visible'] = False

def isVisible(entity):
    return entity['visible']

def setPosition(entity, x, y):
    entity['position'][0] = x
    entity['position'][1] = y

def speed(entity, vx, vy):
    entity['speed'][0] = vx
    entity['speed'][1] = vy

def acceleration(entity, ax, ay):
    entity['acceleration'][0] = ax
    entity['acceleration'][1] = ay

def move(entity, currentTime):
    return

# endregion 

# region ### DRAWING ###
def createPointList(species, position, angle, rmod):
    if species == 'ship':
        return points_ship(position, SHIP_R, angle)
    elif species == 'asteroid':
        return points_asteroid(position, BIG_A_R, angle, rmod)

def move_pol(point, distance, orientation):
    newX = point[0] + distance * math.cos(orientation)
    newY = point[1] + distance * math.sin(orientation)
    return [newX, newY]

def points_ship(p, r, angle):
    p1 = move_pol(p, r, angle)
    p2 = move_pol(p, r,  angle + (5*PI)/6)
    p3 = move_pol(p, r, angle + (7*PI)/6)
    p4 = move_pol(p, r-r/3, angle + PI)

    return [p1, p2, p4, p3]

def points_asteroid(p, r, angle, modList):
    p1 = move_pol(p, r - modList[0], angle)
    p2 = move_pol(p, r + modList[1], angle + PI/7)
    p3 = move_pol(p, r + modList[2], angle + PI/3)
    p4 = move_pol(p, r + modList[3], angle + PI/2 - PI/10)
    p5 = move_pol(p, r - modList[4], angle + 3*PI/4 - PI/15)
    p6 = move_pol(p, r + modList[5], angle + 3*PI/4 + PI/10)
    p7 = move_pol(p, r - modList[6], angle + 7*PI/6 - PI/15)
    p8 = move_pol(p, r - modList[7], angle + 5*PI/4)
    p9 = move_pol(p, r - modList[8], angle + 3*PI/2 + PI/8)
    p10 = move_pol(p, r + modList[9], angle + 11*PI/6 + PI/15)
    
    return [p1, p2, p3, p4, p5, p6, p7, p8, p9, p10]

def rand_r(inf, sup):
    return random.randint(inf, sup)

def create_r_mod_list(size):
    i = 0
    mod_list =[]
    while i < size:
        mod_list.append(rand_r(0,5))
        i += 1
    return mod_list

def draw(entity):
    pygame.draw.polygon(window, LIGHT_BLUE, entity['pointList'], LINE)

# endregion

# region ### SCENE ###

def newScene():
    return {
        'actors': []
    }
def addEntity(scene, entity):
    scene['actors'].append(entity)

def removeEntity(scene, entity):
    actors = scene['actors']
    if entity in actors:
        actors.remove(entity)

def actors(scene):
    return list(scene['actors'])

def update(scene, currentTime):
    myScene = actors(scene)
    for entity in myScene:
        move(entity, currentTime)

def display(scene):
    entities = actors(scene)
    for entity in entities:
        if isVisible(entity):
            draw(entity)

# endregion

# region ### GAME MANIPULATIONS -- #
def interactions():
    global gameOver, inGame
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            gameOver = True
        elif event.type == pygame.KEYDOWN:
            handling_keys(event.key)
                
def handling_keys(key):
    global shipAngle, propulsion
    if key == TURN_RIGHT:
        shipAngle += PI/40
    elif key == TURN_LEFT:
        shipAngle -= PI/40
    elif key == ACCELERATE:
        propulsion = 3
# endregion

# endregion

pygame.init()
pygame.key.set_repeat(10,10)

window = pygame.display.set_mode(WINDOW_SIZE)
pygame.display.set_caption('Asteroids')

# region # -- INIT -- #

# Init Math
prev_time = 0
prev_speed = [0,0]

# Init Ship
ship = new_entity()
ship['position'] = [WINDOW_SIZE[X]/2, WINDOW_SIZE[Y]/2]
ship['angle'] = -PI/2
ship['propulsion'] = 0
ship['pointList'] = createPointList('ship', ship['position'], ship['angle'], ship['rModList'])
ship['visible'] = True


# Init Asteroid
asteroid = new_entity()
asteroid['position'] = [200, 200]
asteroid['angle'] = PI
asteroid['rModList'] = create_r_mod_list(10)
asteroid['pointList'] = createPointList('asteroid', asteroid['position'], asteroid['angle'], asteroid['rModList'])
asteroid['visible'] = True


# Init Scene
scene = newScene()
addEntity(scene, ship)
addEntity(scene, asteroid)

# endregion

inGame = True
gameOver = False
time = pygame.time.Clock()

while not gameOver:
    interactions()
    current_time = pygame.time.get_ticks()
    window.fill(SPACE_GREY)
    display(scene)

    # shipPosition 
    pygame.display.flip()
    
    time.tick(FPS)

pygame.display.quit()
pygame.quit()
exit()
