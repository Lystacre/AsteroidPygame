#------------------------------------------------------------------------------------#
#                                                                                    #
#                                   ASTEROIDS:                                       #
#                                  The Original                                      #
#                     (But ReMade based on what I think it is)                       #
#                                                                                    #
#                           Groupe : Camille Decroly                                 #
#                                                                                    #
#                                                                                    #
#                  Jeu "Asteroids" original par Atari, inc (1979)                    #
#       Créé par Lyle Rains (designer) and Ed Logg (designer et programmeur)         #
#                                                                                    #
#          Théorie mathématique derrière le systeme de collision d'après :           #
#              "How 2D Game Collision Works (Separating Axis Theorem)"               #
#                  https://www.youtube.com/watch?v=dn0hUgsok9M                       #
#                                                                                    #
#------------------------------------------------------------------------------------#

import pygame
import math
from random import randint

# region # -- CONSTANTS -- #
# -- Element sizes -- #
X = 0
Y = 1

WINDOW_SIZE = (1280, 1024)
CENTER = (WINDOW_SIZE[X]/2, WINDOW_SIZE[Y]/2)


FPS = 50
PI = math.pi
LINE = 2
FORCE = 0.0005

MAX_HEALTH = 3

# -- Ship constants -- #
SHIP_R = 25
SHIP_W = 1
SHIP_R_SPEED = PI/30
BULLET_R = 1
BULLET_W = 0.0001
BULLET_SPEED = 0.5

# -- Asteroid constants -- #
A_SPEED = 20

BIG_A_R = 50
BIG_A_W = 3
BIG_A_R_SPEED = PI/250

MEDIUM_A_R = 30
MEDIUM_A_W = 2
MEDIUM_A_R_SPEED = PI/100

SMALL_A_R = 15
SMALL_A_W = 1
SMALL_A_R_SPEED = PI/75


# -- Keyboard keys -- #
TURN_LEFT = pygame.K_LEFT
TURN_RIGHT = pygame.K_RIGHT
ACCELERATE = pygame.K_UP
SHOOT = pygame.K_SPACE
PAUSE = pygame.K_p
MENU = pygame.K_ESCAPE

# -- Colours -- #
SPACE_GREY =    ( 20,  20,  20)
LIGHT_BLUE =    (220, 235, 255)
DARK_RED =      (235,  20,  20)
DARKER_BLUE =   (135, 150, 205)

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
        'visible': False,
        'size': 0,
        'rayon': 1,
        'position': [0,0],
        'color': LIGHT_BLUE,
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
        'rotation_speed': 0,
        'lifetime': 0,
        'invulnerable': 0,
        'cooldown': 0,
        'shooting': 0,
        'normalList':[],
        'projected_pointsList': []
    }

# region ---- Entity Methods ---- #

# region - Get/Set methods - #

def setSpecies(entity, species):
    entity['species'] = species

def visible(entity):
    entity['visible'] = True

def invisble(entity):
    entity['visible'] = False

def shooting(entity):
    entity['shooting'] = True

def notShooting(entity):
    entity['shooting'] = False

def setRayon(entity, rayon):
    entity['rayon'] = rayon



def isVisible(entity):
    return entity['visible']

def setAngle(entity, rad):
    entity['angle'] = rad

def setSize(entity, size):
    entity['size'] = size

def setSpeed(entity, speed):
    entity['prev_speed'] = speed
    entity['speed'] = speed

def setPosition(entity, x, y):
    entity['position'][0] = x
    entity['position'][1] = y

def setWeight(entity, w):
    entity['weight'] = w

def setRotationSide(entity):
    entity['rotation_side'] = randint(0,1)

def setRotationSpeed(entity, speed):
    entity['rotation_speed'] = speed

def setLifetime(entity, time):
    entity['lifetime'] = time

def setRandomPos(entity):
    x_pos = CENTER[X]
    y_pos = CENTER[Y]
    while x_pos >= 200 and x_pos <= WINDOW_SIZE[X] - 200:
        x_pos = randint(0,WINDOW_SIZE[X])    

    while y_pos >= 200 and y_pos <= WINDOW_SIZE[Y] - 200:
        y_pos = randint(0,WINDOW_SIZE[Y])

    entity['position'] = [x_pos, y_pos]

def setRandomSpeed(entity, max, min):
    x_speed = 0
    y_speed = 0

    while x_speed >= -min and x_speed <= min:
        x_speed = randint(-max, max) 
    
    while y_speed >= -min and y_speed <= min:
        y_speed = randint(-max, max)
    
    x_speed *= 0.01
    y_speed *= 0.01

    entity['prev_speed'] = [x_speed, y_speed]
    entity['speed'] = [x_speed, y_speed]

def speed(entity, dt):
    entity['speed'][X] = entity['prev_speed'][X] + dt * entity['acceleration'][X]
    entity['speed'][Y] = entity['prev_speed'][Y] + dt * entity['acceleration'][Y]
    entity['prev_speed'] = entity['speed']


def setPointList(entity, species, position, angle, rmod):
    if species == 'ship':
        entity['pointList'] = points_ship(position, entity['rayon'], angle)
    elif species == 'asteroid':
        entity['pointList'] = points_asteroid(position, entity['rayon'], angle, rmod)
    elif species == 'bullet':
        entity['pointList'] = [position]

def setRModList(entity, size):
    i = 0
    mod_list =[]
    while i < size:
        mod_list.append(rand_r(0,10))
        i += 1
    entity['rModList'] = mod_list

# endregion

# region - Moving methods - #

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
    

    if entity['position'][X] < - (entity['rayon'] + 10):
        entity['position'][X] = WINDOW_SIZE[X] + (entity['rayon'] + 10)
    elif entity['position'][X] > WINDOW_SIZE[X] + (entity['rayon'] + 10):
        entity['position'][X] = -(entity['rayon'] + 10)

    if entity['position'][Y] < -(entity['rayon'] + 10):
        entity['position'][Y] = WINDOW_SIZE[Y] + (entity['rayon'] + 10)
    elif entity['position'][Y] > WINDOW_SIZE[Y] + (entity['rayon'] + 10):
        entity['position'][Y] = -(entity['rayon'] + 10)

    
    setPointList(entity, entity['species'], entity['position'], entity['angle'], entity['rModList'])

def rotate(entity, currentTime, key, speed):
    global prev_time
    dt = currentTime - prev_time
    if key == TURN_RIGHT or key == 0:
        entity['angle'] += speed
    elif key == TURN_LEFT or key == 1:
        entity['angle'] -= speed
    
    setPointList(entity, entity['species'], entity['position'], entity['angle'], entity['rModList'])
# endregion

# region - Specific entity creation - #
def newShip():
    global ship
    ship = new_entity()
    setSpecies(ship, 'ship')
    setRayon(ship, SHIP_R)
    setPosition(ship, CENTER[X], CENTER[Y])
    setAngle(ship, -PI/2)
    setPointList(ship, ship['species'], ship['position'], ship['angle'], ship['rModList'])
    setWeight(ship, SHIP_W)
    setRotationSpeed(ship, SHIP_R_SPEED)
    visible(ship)

    addEntity(scene, ship)

def newAsteroid(size, pos):
    asteroid = new_entity()
    setSpecies(asteroid, 'asteroid')
    setSize(asteroid, size)
    if size == 3:
        setRayon(asteroid, BIG_A_R)
        setWeight(asteroid, BIG_A_W)
        setRotationSpeed(asteroid, BIG_A_R_SPEED)
        setRandomSpeed(asteroid, 20, 5)
        setRandomPos(asteroid)
    elif size == 2:
        setRayon(asteroid, MEDIUM_A_R)
        setWeight(asteroid, MEDIUM_A_W)
        setRotationSpeed(asteroid, MEDIUM_A_R_SPEED)
        setRandomSpeed(asteroid, 21, 5)
        setPosition(asteroid, pos[X], pos[Y])
    elif size == 1:
        setRayon(asteroid, SMALL_A_R)
        setWeight(asteroid, SMALL_A_W)
        setRotationSpeed(asteroid, SMALL_A_R_SPEED)
        setRandomSpeed(asteroid, 22, 5)
        setPosition(asteroid, pos[X], pos[Y])
    setAngle(asteroid, PI)
    setRModList(asteroid, 10)
    setPointList(asteroid, asteroid['species'], asteroid['position'], asteroid['angle'], asteroid['rModList'])
    setRotationSide(asteroid)
    visible(asteroid)

    addEntity(scene, asteroid)

def newBullet(position, speed, angle):
    bullet = new_entity()
    x_pos = position[X] + SHIP_R * math.cos(angle)
    y_pos = position[Y] + SHIP_R * math.sin(angle)
    setSpecies(bullet, 'bullet')
    setRayon(bullet, BULLET_R)
    setSpeed(bullet, speed)
    setWeight(bullet, BULLET_W)
    setPosition(bullet, x_pos, y_pos)
    setLifetime(bullet, 50)
    setAngle(bullet, angle)
    visible(bullet)
    setPointList(bullet, bullet['species'], bullet['position'], bullet['angle'], bullet['rModList'])

    addEntity(scene, bullet)

def newAlert(position):
    alert = new_entity()


# endregion

# region - Collision System - Separating Axis Theorem # 


def checkCollision(entityA, entityB):
    normalListA = NormalList(entityA)
    normalListB = NormalList(entityB)
    normalList = []
    for normalA in normalListA:
        normalList.append(normalA)
    for normalB in normalListB:
        normalList.append(normalB)
    
    for normal in normalList:
        amin = None
        amax = None
        bmin = None
        bmax = None
        for point in entityA['pointList']:
            dotProd = dotProduct(point, normal)
            # print(f"dotProdA de {point} et {normal} = {dotProd}")
            if amax == None or dotProd > amax:
                amax = dotProd
            if amin == None or dotProd < amin:
                amin = dotProd
        for point in entityB['pointList']:
            dotProd = dotProduct(point, normal)
            # print(f"dotProdB de {point} et {normal} = {dotProd}")
            if bmax == None or dotProd > bmax:
                bmax = dotProd
            if bmin == None or dotProd < bmin:
                bmin = dotProd
        # print(f"amin = {amin}, amax = {amax}, bmin = {bmin}, bmax = {bmax}")
        if not ((amin < bmax and amin > bmin) or (bmin < amax and bmin > amin)):
            return  False
        
    return True

# region - Collision System - Math Functions - #
def NormalList(entity):
    normalList = []
    point = 0
    if entity['species'] == 'ship':
        for point in range(0, len(entity['pointList'])-1):
            if point == 0:
                normalList.append(calcNormal(entity['pointList'][point], entity['pointList'][point+1]))
                normalList.append(calcNormal(entity['pointList'][point], entity['pointList'][point+2]))
                normalList.append(calcNormal(entity['pointList'][point], entity['pointList'][point+3]))
            else:    
                normalList.append(calcNormal(entity['pointList'][point], entity['pointList'][point+1]))
    elif entity['species'] == 'asteroid':
        for point in range(len(entity['pointList']) - 1):
            normalList.append(calcNormal(entity['position'], entity['pointList'][point]))
            normalList.append(calcNormal(entity['pointList'][point], entity['pointList'][point+1]))

        normalList.append(calcNormal(entity['pointList'][len(entity['pointList'])-1], entity['pointList'][0]))
    return normalList

def dotProduct(point, normal):
    return point[X] * normal[X] + point[Y] * normal[Y]

def calcNormal(p1, p2):
    vector = findEdge(p1,p2)
    return [-vector[Y], vector[X]]

def findEdge(p1, p2):
    vX = p2[X] - p1[X]
    vY = p2[Y] - p1[Y]
    return vX, vY 

# endregion

# endregion

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
    return randint(inf, sup)

def draw(entity):
    if entity['species'] == 'bullet':
        pygame.draw.circle(window, entity['color'], entity['position'], entity['rayon'], LINE)
    else:
        pygame.draw.polygon(window, entity['color'], entity['pointList'], LINE)

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

def shootingTest(entity, dt):
    if entity['shooting'] == True:
            if entity['cooldown'] <= 0.0:
                shoot()
                entity['cooldown'] = 50
            else:
                entity['cooldown'] -= dt

def dtHandeling(entity, dt):
    if entity['lifetime'] > 0 and entity['species'] == 'bullet':
        entity['lifetime'] -= 1
        if entity['lifetime'] == 0:
            removeEntity(scene, entity)
    if entity['invulnerable'] > 0:
        entity['invulnerable'] -= dt
        entity['color'] = DARKER_BLUE
    else:
        entity['color'] = LIGHT_BLUE

def propulsionHandeling(entity):
    if entity['propulsion'] > 0:
        propulsion(entity, FORCE, entity['angle'])
        entity['propulsion'] -= 1
    else:
        entity['propulsion_str'] = [0,0]

def update(scene, currentTime):
    global prev_time, remaining_health, gameOver, score
    dt = currentTime - prev_time
    myScene = actors(scene)
    for entity in myScene:
        
        move(entity, currentTime)
        
        shootingTest(entity, dt)
        
        dtHandeling(entity, dt)
 
        propulsionHandeling(entity)
        
        if entity['species'] == 'asteroid':
        
            rotate(entity, current_time, entity['rotation_side'], entity['rotation_speed'])
            
            for entity2 in myScene:
                if entity2['species'] == 'bullet':
                    if checkCollision(entity, entity2) == True:
                        print("pew pew")
                        if entity['size'] > 1:
                            for _ in range(3):
                                print(f"Asteroid size = {entity['size']}")
                                newAsteroid(entity['size']-1, entity['position'])
                                if entity['size'] == 3:
                                    score += 20
                                elif entity['size'] == 2:
                                    score += 50
                        elif entity['size'] == 1:
                            score += 100
                        removeEntity(scene, entity)
                        removeEntity(scene, entity2)
        if entity['species'] == 'ship':
            for entity2 in myScene:
                if entity2['species'] == 'asteroid':      
                    if checkCollision(entity, entity2) == True:
                        if entity['invulnerable'] > 0:
                            print("YOU HAVE NO POWER OVER ME")
                        else:
                            remaining_health -= 1
                            print("collision")  
                            entity['invulnerable'] = 4000
                            entity['color'] = DARKER_BLUE
                            if remaining_health < 1:
                                removeEntity(scene, entity)
                                gameOver = True


def display(scene):
    global remaining_health
    entities = actors(scene)
    for entity in entities:
        if isVisible(entity):
            draw(entity)
    for life in range(remaining_health - 1):
        pygame.draw.polygon(window, LIGHT_BLUE, points_ship((20 + life * 20, 20), 10, -PI/2), LINE)
# endregion  

# endregion

# region ### GAME MANIPULATIONS -- #
def interactions():
    global gameOver, inGame, current_time, ship, remaining_health
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            remaining_health = 0
            gameOver = True
        elif event.type == pygame.KEYDOWN:
            handling_keys(event.key)
        elif event.type == pygame.KEYUP:
            if event.key == SHOOT:
                notShooting(ship)
                
def handling_keys(key):
    global pause
    if key == TURN_LEFT or key == TURN_RIGHT:
        rotate(ship, current_time, key, ship['rotation_speed'])
    if key == ACCELERATE:
        ship['propulsion'] = 3
    if key == SHOOT:
        shooting(ship)
    if key == PAUSE:
        pause = not pause

def shoot():
    bullet_angle = ship['angle']

    speed_X = math.cos(bullet_angle) * BULLET_SPEED
    speed_Y = math.sin(bullet_angle) * BULLET_SPEED
    newBullet(ship['position'], [speed_X, speed_Y], bullet_angle)

# endregion

# endregion
pygame.init()
pygame.key.set_repeat(100,25)

window = pygame.display.set_mode(WINDOW_SIZE)
pygame.display.set_caption('Asteroids: The Original (But Remade Based on What I Think It Is)')

# region # -- INIT -- #
init_Data()

# Init Scene
scene = newScene()

# Init Ship
newShip()

# Init Asteroid
i = 0
while i < 3:
    newAsteroid(3,[0,0])
    i += 1

# endregion
inGame = True
gameOver = False
time = pygame.time.Clock()

pause = False
playing = True

remaining_health = MAX_HEALTH
score = 0

while remaining_health > 0:
    gameOver = False
    while not gameOver:
        global prev_time

        # --- Traites les interactions --- #
        interactions()
        current_time = pygame.time.get_ticks()
        window.fill(SPACE_GREY)
        
        if not pause:
            update(scene, current_time)

        display(scene)    
        pygame.display.flip()
        time.tick(FPS)
        prev_time = current_time

pygame.display.quit()
pygame.quit()
exit()
