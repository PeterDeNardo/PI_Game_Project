# Pygame template - skeleton for a new pygame project
from help import *
import random
import math

#Classe da barra d eforça
class PowerBar(pygame.sprite.Sprite):
    def __init__(self):
        # Seta dados iniciais
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.Surface((10, 1))
        self.image.fill(BLACK)
        self.rect = self.image.get_rect()
        self.rect.x = 10
        self.rect.y = 500
        self.height = 1
        self.weigth = 10
        self.addition = 1

    def update(self, *args):
        #Movimenta a barra quando SPACE estiver precionado
        pygame.draw.rect(screen, BLACK, ( 10, 500, self.weigth, -self.height))

        pressKeys = pygame.key.get_pressed()
        if pressKeys[pygame.K_SPACE]:
            self.height += self.addition
            if self.height >= 100:
                self.addition = -1
            if self.height <= 0:
                self.addition = 1

class Player(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.Surface((10, 10))
        self.rect = self.image.get_rect()
        self.rect.x = 50
        self.rect.y = HEIGHT / 2
        self.rect.height = 10
        self.rect.width = 10
        self.image.fill(RED)
        self.Xo = self.rect.x
        self.Yo = self.rect.y
        self.Vo = 100
        self.ready = True


        self.eixoYA = self.rect.center
        self.eixoYB = (self.rect.center[0], (self.rect.center[1] + 10))

        self.eixoXA = self.rect.center
        self.eixoXB = ((self.rect.center[0] + 10), (self.rect.center[1]))
        self.sin = 0
        self.cos = 0
        self.teste = 0
        self.t = 0

        self.changeX = self.rect.x
        self.changeY = self.rect.y

        #Determina se o jogador esta em contato com algo
        self.contact = False

        self.direction : bool

        #self.level = None
        self.walls = None
        self.enemys = None
        self.portals = None

    def launch(self, Vo):
        self.Vo = Vo
        print(221)

    def update(self):

        self.rect.x = self.changeX
        self.rect.y = self.changeY

        results = self.contructAngle()
        sinn = results[0]
        coss = results[1]

        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_KP_ENTER and self.ready:
                self.contact = False
                self.ready = False
                self.sin = sinn
                self.cos = coss
                self.Voy = 10
                self.teste = 1
                self.direction = (results[2], results[3])
                self.launch(powerBar.height * 2)
                print("porra")

        if not self.ready:

            if self.direction[0]:
                vX = (self.cos * self.Vo)
            else:
                vX = -(self.cos * self.Vo)

            if self.direction[1]:
                vY = (self.sin * self.Vo)
            else:
                vY = -(self.sin * self.Vo)

            self.changeX = self.Xo + (vX * self.t)
            self.changeY = (self.Yo) -(vY * self.t) + (self.teste * (9.8 * (self.t ** 2)) / 2)

            if self.teste == 1 :
                self.t += 0.1

            #Colisão

        enemyCollisionList = pygame.sprite.spritecollide(self, self.enemys, False)
        portalCollisionList = pygame.sprite.spritecollide(self, self.portals, False)
        wallCollisionList = pygame.sprite.spritecollide(self, self.walls, False)
        for wall in wallCollisionList:
            # If we are moving right, set our right side to the left side of
            # the item we hit
           if not self.ready:

                if self.rect.midtop[1] < wall.rect.midtop[1] and self.rect.midright[0] < wall.rect.midright[0] and self.rect.midleft[0] > wall.rect.midleft[0]:
                    self.changeY = (wall.rect.y - self.rect.height)
                    print(self.rect.midtop[1], wall.rect.midtop[1], self.rect.midright[0], wall.rect.midright[0],
                          self.rect.midleft[0], wall.rect.midleft[0])
                    print(1)
                elif  self.rect.midtop[1] > wall.rect.midtop[1] and self.rect.midright[0] < wall.rect.midright[0] and self.rect.midleft[0] < wall.rect.midleft[0]:
                    self.changeX = (wall.rect.x - self.rect.width)
                    print(self.rect.midtop[1], wall.rect.midtop[1], self.rect.midright[0], wall.rect.midright[0],
                          self.rect.midleft[0], wall.rect.midleft[0])
                    print(wall.width)
                    print(2)
                elif  self.rect.midtop[1] > wall.rect.midtop[1] and self.rect.midright[0] > wall.rect.midright[0] and self.rect.midleft[0] > wall.rect.midleft[0]:
                    self.changeX = (wall.rect.x + wall.width)
                    print(self.rect.midtop[1], wall.rect.midtop[1], self.rect.midright[0], wall.rect.midright[0],
                          self.rect.midleft[0], wall.rect.midleft[0])
                    print(3)
                elif  self.rect.midtop[1] > wall.rect.midtop[1] and self.rect.midright[0] < wall.rect.midright[0] and self.rect.midleft[0] > wall.rect.midleft[0]:
                    self.changeY = (wall.rect.y + wall.height)
                    print(self.rect.midtop[1], wall.rect.midtop[1], self.rect.midright[0], wall.rect.midright[0],
                          self.rect.midleft[0], wall.rect.midleft[0])
                    print(4)

                self.Xo = self.changeX
                self.Yo = self.changeY
                self.t = 0
                self.sin = 0
                self.cos = 0
                self.Voy = 0
                self.teste = 0
                self.ready = True

        for enemy in enemyCollisionList:
            print("GameOver")
        for portal in portalCollisionList:
            print("Nextlevel")





    def calcularDDP(self, pontoA, pontoB):
        distancia = (((pontoB[0] - pontoA[0]) ** 2 + (pontoB[1] - pontoA[1]) ** 2) ** 1/2)
        return distancia

    def contructAngle(self):

        self.eixoYA = self.rect.center
        self.eixoYB = (self.rect.center[0], (self.rect.center[1]))
        self.eixoXA = self.rect.center
        self.eixoXB = ((pygame.mouse.get_pos()[0]), (self.rect.center[1]))
        self.angleLine = ((self.eixoXB[0], pygame.mouse.get_pos()[1]))
        self.catetoOposto = (self.eixoXB, self.angleLine)
        self.catetoAdjacente = (self.eixoXA, self.eixoXB)
        self.hypotenusa = (self.eixoXA, self.angleLine)
        self.rect2 = pygame.draw.line(screen, BLACK, self.eixoYA, self.eixoYB, 1)
        self.rect2 = pygame.draw.line(screen, BLACK, self.eixoXA, self.eixoXB, 1)
        self.rect2 = pygame.draw.line(screen, BLACK, self.eixoXA, self.angleLine, 1)
        self.rect2 = pygame.draw.line(screen, BLACK, self.eixoXB, self.angleLine, 1)
        distanciaCatOp = self.calcularDDP(self.catetoOposto[0], self.catetoOposto[1])
        distanciaCatAd = self.calcularDDP(self.catetoAdjacente[0], self.catetoAdjacente[1])
        distanciaHy = self.calcularDDP(self.hypotenusa[0], self.hypotenusa[1])

        directionX = True
        directionY = True

        if self.eixoXB[0] < self.rect.center[0]:
            directionX = False

        if self.angleLine[1] > self.rect.center[1]:
            directionY = False

        results =  ( distanciaCatOp / distanciaHy, distanciaCatAd / distanciaHy, directionX, directionY)

        return results

class Wall(pygame.sprite.Sprite):
    def __init__(self, x, y, width, height):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.Surface([width, height])
        self.image.fill(BLACK)

        self.height = height
        self.width = width
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y

class Enemy(pygame.sprite.Sprite):
    def __init__(self, x, y, width, height, finalX, finalY):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.Surface([width, height])
        self.image.fill(GREEN)

        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        self.inicialX = x
        self.inicialY = y

        self.finalX = finalX
        self.finalY = finalY
        self.changueX = 0
        self.changueY = 0

        self.go = True

    def update(self, *args):
        if not self.rect.x == self.finalX and self.go:
            if self.finalX > self.inicialX:
                self.rect.x += 1
            else:
                self.rect.x -= 1
            if self.finalY > self.inicialY:
                self.rect.y += 1
            else:
                self.rect.y -= 1
        elif self.rect.x == self.finalX or not self.go:
            self.go = False
            if self.finalX > self.inicialX:
                self.rect.x -= 1
            else:
                self.rect.x += 1
            if self.finalY > self.inicialY:
                self.rect.y -= 1
            else:
                self.rect.y += 1
            if self.rect.x == self.inicialX and self.rect.y == self.inicialY:
                self.go = True

class Portal(pygame.sprite.Sprite):
    def __init__(self, x, y, width, height):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.Surface([width, height])
        self.image.fill(BLUE)

        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y

# class Level(object):
#     def __init__(self, player):
#         self.wallList = pygame.sprite.Group()
#         self.enemyList = pygame.sprite.Group()
#         self.player = player
#
#         self.background = None
#
#     def update(self):
#         self.wallList.update()
#         self.enemyList.update()
#
#     def draw(self, screen):
#         screen.fill(WHITE)
#
#         self.wallList.draw(screen)
#         self.enemyList.draw(screen)
#
# class Level01(Level):
#     def __init__(self, Player):
#
#         Level.__init__(self, Player)
#
#         # Array with width, height, x, and y of platform
#         level = [[WIDTH, 40, 660, 0],
#                  [210, 70, 800, 400],
#                  [210, 70, 1000, 500],
#                  [210, 70, 1120, 280],]
#
#         for wall in level:
#             block = Wall(wall[0], wall[1])
#             block.rect.x = wall[2]
#             block.rect.y = wall[3]
#             block.player = self.player
#             self.wallList.add(block)



pygame.init()
pygame.mixer.init()
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("My Game")
clock = pygame.time.Clock()

player = Player()
powerBar = PowerBar()

allSprites = pygame.sprite.Group()

#     # Create all the levels
# levelList = []
# levelList.append(Level01(player))
#
#     # Set the current level
# currentLevelNo = 0
# currentLevel = levelList[currentLevelNo]

# Make the walls. (x_pos, y_pos, width, height)
wallsList = pygame.sprite.Group()
enemyList = pygame.sprite.Group()
portalList = pygame.sprite.Group()

wall = Wall(0, 0, 10, 600)
wallsList.add(wall)
allSprites.add(wall)

wall = Wall(0, 0, 1000, 10)
wallsList.add(wall)
allSprites.add(wall)

wall = Wall(0, 590, 1000, 10)
wallsList.add(wall)
allSprites.add(wall)

wall = Wall(300, 300, 50, 100)
wallsList.add(wall)
allSprites.add(wall)

enemy = Enemy(500, 500, 50, 50, 600, 400)
enemyList.add(enemy)
allSprites.add(enemy)

portal = Portal(700, 500, 50, 50)
portalList.add(portal)
allSprites.add(portal)


player.walls = wallsList
player.enemys = enemyList
player.portals = portalList

allSprites.add(player)
allSprites.add(powerBar)

# Game loop
running = True
while running:
    # keep loop running at the right speed
    clock.tick(FPS)
    # Process input (events)
    for event in pygame.event.get():
        # check for closing window
        if event.type == pygame.QUIT:
            running = False


    screen.fill(WHITE)
    #update
    allSprites.update()
    # Draw / render
    allSprites.draw(screen)

    # *after* drawing everything, flip the display
    pygame.display.flip()

pygame.quit()