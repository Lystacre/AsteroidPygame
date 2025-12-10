import math
import pygame
import sys

# Constantes

NOIR =  (  0,   0,   0)
BLEU =  (  0,   0, 255)
VERT =  (  0, 255,   0)
BLANC = (255, 255, 255)

X = 0
Y = 1

PI = math.pi
# Paramètres

dimensions_fenetre = (800, 600)  # en pixels
images_par_seconde = 25

TriangleBleuPos = [200, 200]
TriangleVertPos = [400, 400]
TriangleBleuVis = False
TriangleVertVis = False


# Fonctions

# region - Trouver Norme -
def comparePolygons(pointListA, pointListB):
    normalListA = NormalList(pointListA)
    normalListB = NormalList(pointListB)
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
        for point in pointListA:
            dotProd = dotProduct(point, normal)
            # print(f"dotProdA de {point} et {normal} = {dotProd}")
            if amax == None or dotProd > amax:
                amax = dotProd
            if amin == None or dotProd < amin:
                amin = dotProd
        for point in pointListB:
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

def NormalList(pointList):
    normalList = []
    for i in range(0, len(pointList)-1):
        normalVec = calcNormal(pointList[i], pointList[i+1])
        normalList.append(normalVec)
    
    normalVec = calcNormal(pointList[len(pointList)-1], pointList[0])
    normalList.append(normalVec)
    return normalList


def calcNormal(p1, p2):
    vector = findEdge(p1, p2)
    # normal = [-vector[Y], vector[X]]
    return [-vector[Y], vector[X]]

def findEdge(p1, p2):
    vX = p2[X] - p1[X]
    vY = p2[Y] - p1[Y]
    return vX, vY
# endregion


# region - Dot product -
def dotProduct(vect1, vect2):
    return vect1[X] * vect2[X] + vect1[Y] * vect2[Y]

# endregion


# region - Polygon Creation - #
def move_pol(point, distance, orientation):
    newX = point[0] + distance * math.cos(orientation)
    newY = point[1] + distance * math.sin(orientation)
    return [newX, newY]

def triangleVert(pos):
    global TriangleVertPoints
    p1 = move_pol(pos, 100, PI/4)
    p2 = move_pol(pos, 100, 6*PI/3)
    p3 = move_pol(pos, 100, 7*PI/6)
    TriangleVertPoints = [p1, p2, p3]

def triangleBleu(pos):
    global TriangleBleuPoints
    p1 = move_pol(pos, 100, PI/2)
    p2 = move_pol(pos, 100, PI/3)
    p3 = move_pol(pos, 100, -PI/6)
    TriangleBleuPoints = [p1, p2, p3]

def displayTriangles():
    if TriangleBleuVis == True:
        pygame.draw.polygon(fenetre, BLEU, TriangleBleuPoints)
        normalListB = NormalList(TriangleBleuPoints)
        # for line in normalListB:
        #     xB = line[0]
        #     yB = line[1]
        #     pygame.draw.line(fenetre, BLANC, line, [line[0] - 100, line[1]-100], 2)
    if TriangleVertVis == True:
        pygame.draw.polygon(fenetre, VERT, TriangleVertPoints)
        normalListV = NormalList(TriangleVertPoints)
        # for line in normalListV:
        #     xV = line[0]
        #     yV = line[1]
        #     pygame.draw.line(fenetre, BLANC, line, [line[0] - 100, line[1]-100], 2)

# endregion

def gerer_bouton(evenement):
   global TriangleBleuPos, TriangleBleuVis, TriangleVertPos, TriangleVertVis
   if evenement.button == 3:
      TriangleBleuVis = True
      TriangleBleuPos = evenement.pos
      triangleBleu(TriangleBleuPos)
   elif evenement.button == 1:
      TriangleVertVis = True
      TriangleVertPos = evenement.pos
      triangleVert(TriangleVertPos)


# Initialisation


pygame.init()

fenetre = pygame.display.set_mode(dimensions_fenetre)
pygame.display.set_caption("Programme 7")

horloge = pygame.time.Clock()
couleur_fond = NOIR
while True:

    global TriangleBleuPoints, TriangleVertPoints
    
    for evenement in pygame.event.get():
        if evenement.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        elif evenement.type == pygame.MOUSEBUTTONDOWN:
            gerer_bouton(evenement)
            if TriangleBleuVis == True and TriangleVertVis == True:
                isColliding = comparePolygons(TriangleBleuPoints, TriangleVertPoints)

                if isColliding:
                    print("colliding")
                else:
                    print("not colliding")

    fenetre.fill(couleur_fond)
    displayTriangles()
    
   
    pygame.display.flip()
    horloge.tick(images_par_seconde)