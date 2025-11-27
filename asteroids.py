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

FORCE = 0.001

# -- Ship constants --
SHIP_R = 25
SHIP_W = 1
SHIP_R_SPEED = PI/30

# -- Asteroid constants --
A_SPEED = 20

BIG_A_R = 50
BIG_A_W = 2.5
BIG_A_R_SPEED = PI/250

MEDIUM_A_R = 30
MEDIUM_A_W = 1
MEDIUM_A_R_SPEED = PI/100


SMALL_A_R = 15
SMALL_A_W = 0.8
SMALL_A_R_SPEED = PI/75


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

# Init Maths

def init_Data():
    global prev_time
    prev_time = 0


# region ### ENTITY ###

def new_entity():
    return {
        'species': None,
        'visible':False,
        'size': 0,
        'position': [0,0],
        'angle': 0,
        'weight': 0,
        'pointList': [],
        'rModList': [0],
        'speed': [0,0],
        'prev_speed': [0,0],
        'acceleration': [0,0],
        'propulsion': 0,
        'propulsion_str': [0,0],
        'rotation_side': 0,
        'rotation_speed': 0
    }

# region ---- Entity Methods ---- #
def setSpecies(entity, species):
    entity['species'] = species

def visible(entity):
    entity['visible'] = True

def invisble(entity):
    entity['visible'] = False

def setSize(entity, size):
    entity['size'] = size

def isVisible(entity):
    return entity['visible']

def setAngle(entity, rad):
    entity['angle'] = rad

def setPosition(entity, x, y):
    entity['position'][0] = x
    entity['position'][1] = y

def setWeight(entity, w):
    entity['weight'] = w

def setRotationSide(entity):
    entity['rotation_side'] = random.randint(0,1)

def setRotationSpeed(entity, speed):
    entity['rotation_speed'] = speed

def speed(entity, dt):
    entity['speed'][X] = entity['prev_speed'][X] + dt * entity['acceleration'][X]
    entity['speed'][Y] = entity['prev_speed'][Y] + dt * entity['acceleration'][Y]
    entity['prev_speed'] = entity['speed']

def acceleration(entity, w):
    entity['acceleration'][X] = entity['propulsion_str'][X]/w
    entity['acceleration'][Y] = entity['propulsion_str'][Y]/w

def propulsion(entity, F, angle):
    entity['propulsion_str'][X] = F * math.cos(angle)
    entity['propulsion_str'][Y] = F * math.sin(angle)

def move(entity, currentTime):
    global prev_time
    dt = currentTime - prev_time
    acceleration(entity, entity['weight'])
    speed(entity, dt)
    entity['position'][X] += dt * entity['speed'][X]
    entity['position'][Y] += dt * entity['speed'][Y]
    
    if entity['position'][X] < -25:
        entity['position'][X] = WINDOW_SIZE[X] + 25
    elif entity['position'][X] > WINDOW_SIZE[X] + 25:
        entity['position'][X] = -25
    if entity['position'][Y] < -25:
        entity['position'][Y] = WINDOW_SIZE[Y] + 25
    elif entity['position'][Y] > WINDOW_SIZE[Y] + 25:
        entity['position'][Y] = -25

    setPointList(entity, entity['species'], entity['position'], entity['angle'], entity['rModList'])

def rotate(entity, currentTime, key, speed):
    global prev_time
    dt = currentTime - prev_time
    if key == TURN_RIGHT or key == 0:
        entity['angle'] += speed
    elif key == TURN_LEFT or key == 1:
        entity['angle'] -= speed
    print(entity['angle'])
    setPointList(entity, entity['species'], entity['position'], entity['angle'], entity['rModList'])

def setPointList(entity, species, position, angle, rmod):
    if species == 'ship':
        entity['pointList'] = points_ship(position, entity['size'], angle)
    elif species == 'asteroid':
        entity['pointList'] = points_asteroid(position, entity['size'], angle, rmod)

def setRModList(entity, size):
    i = 0
    mod_list =[]
    while i < size:
        mod_list.append(rand_r(0,10))
        i += 1
    entity['rModList'] = mod_list

# endregion

# endregion 

# region ### DRAWING ###


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

def draw(entity):
    pygame.draw.polygon(window, LIGHT_BLUE, entity['pointList'], LINE)

# endregion

# region ### SCENE ###

def newScene():
    return {
        'actors': []
    }

# region ---- Scene Methods ---- #

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

# endregion

# region ### GAME MANIPULATIONS -- #
def interactions():
    global gameOver, inGame, current_time
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            gameOver = True
        elif event.type == pygame.KEYDOWN:
            handling_keys(event.key)
                
def handling_keys(key):
    if key == TURN_LEFT or key == TURN_RIGHT:
        rotate(ship, current_time, key, ship['rotation_speed'])
    if key == ACCELERATE:
        ship['propulsion'] = 3
# endregion

# endregion

pygame.init()
pygame.key.set_repeat(10,10)

window = pygame.display.set_mode(WINDOW_SIZE)
pygame.display.set_caption('Asteroids: The Original (But Remade)')

# region # -- INIT -- #
init_Data()

# Init Ship
ship = new_entity()
setSpecies(ship, 'ship')
setSize(ship, SHIP_R)
setPosition(ship, WINDOW_SIZE[X]/2, WINDOW_SIZE[Y]/2)
setAngle(ship, -PI/2)
setPointList(ship, ship['species'], ship['position'], ship['angle'], ship['rModList'])
setWeight(ship, SHIP_W)
setRotationSpeed(ship, SHIP_R_SPEED)
visible(ship)


# Init Asteroid
asteroidBig = new_entity()
setSpecies(asteroidBig, 'asteroid')
setSize(asteroidBig, BIG_A_R)
setPosition(asteroidBig, 200, 200)
setAngle(asteroidBig, PI)
setRModList(asteroidBig, 10)
setPointList(asteroidBig, asteroidBig['species'], asteroidBig['position'], asteroidBig['angle'], asteroidBig['rModList'])
setWeight(asteroidBig, BIG_A_W)
setRotationSide(asteroidBig)
setRotationSpeed(asteroidBig, BIG_A_R_SPEED)
visible(asteroidBig)

asteroidMed = new_entity()
setSpecies(asteroidMed, 'asteroid')
setSize(asteroidMed, MEDIUM_A_R)
setPosition(asteroidMed, 500, 500)
setAngle(asteroidMed, PI)
setRModList(asteroidMed, 10)
setPointList(asteroidMed, asteroidMed['species'], asteroidMed['position'], asteroidMed['angle'], asteroidMed['rModList'])
setWeight(asteroidMed, MEDIUM_A_W)
setRotationSpeed(asteroidMed, MEDIUM_A_R_SPEED)
setRotationSide(asteroidMed)
visible(asteroidMed)


# Init Scene
scene = newScene()
addEntity(scene, ship)
addEntity(scene, asteroidBig)
addEntity(scene, asteroidMed)

# endregion

inGame = True
gameOver = False
time = pygame.time.Clock()

while not gameOver:
    global prev_time
    interactions()
    current_time = pygame.time.get_ticks()
    window.fill(SPACE_GREY)

    rotate(asteroidBig, current_time, asteroidBig['rotation_side'], asteroidBig['rotation_speed'])
    rotate(asteroidMed, current_time, asteroidMed['rotation_side'], asteroidMed['rotation_speed'])
    # ship Propulsion
    if ship['propulsion'] > 0:
        propulsion(ship, FORCE, ship['angle'])
        ship['propulsion'] -= 1
    else:
        ship['propulsion_str'] = [0,0]
    update(scene, current_time)
    display(scene)    
    pygame.display.flip()
    
    time.tick(FPS)
    prev_time = current_time

pygame.display.quit()
pygame.quit()
exit()
