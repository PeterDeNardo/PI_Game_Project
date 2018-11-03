# Pygame template - skeleton for a new pygame project
import pygame
import random
import math

WIDTH = 1000
HEIGHT = 600
FPS = 30

# define colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)

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

        if event.type == pygame.KEYUP:
            if event.key == pygame.K_SPACE and player.ready:
                #Envia a força em que a barra estiver para o lançamento do projétil
                player.launch(self.height * 2)
                self.height = 1

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

    def launch(self, Vo):
        self.Vo = Vo

    def update(self):

        self.rect.x = self.changeX
        self.rect.y = self.changeY

        results = self.contructAngle()
        sinn = results[0]
        coss = results[1]

        if event.type == pygame.KEYUP:
            if event.key == pygame.K_SPACE and self.ready:
                self.contact = False
                self.ready = False
                self.sin = sinn
                self.cos = coss
                self.Voy = 10
                self.teste = 1
                self.direction = (results[2], results[3])

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

        block_hit_list = pygame.sprite.spritecollide(self, self.walls, False)
        for block in block_hit_list:
            # If we are moving right, set our right side to the left side of
            # the item we hit
            if self.changeX > 0:
                print(self.rect.midtop[1], block.rect.midtop[1], self.rect.midright[0],block.rect.midright[0], self.rect.midleft[0] ,  block.rect.midleft[0])
                if self.rect.midtop[1] < block.rect.midtop[1] and self.rect.midright[0] < block.rect.midright[0] and self.rect.midleft[0] > block.rect.midleft[0]:
                    self.changeY = (block.rect.y - 10)
                    print(1)
                elif  self.rect.midtop[1] > block.rect.midtop[1] and self.rect.midright[0] < block.rect.midright[0] and self.rect.midleft[0] < block.rect.midleft[0]:
                    self.changeX = (block.rect.x - 10)
                    print(2)
                elif  self.rect.midtop[1] > block.rect.midtop[1] and self.rect.midright[0] > block.rect.midright[0] and self.rect.midleft[0] > block.rect.midleft[0]:
                    self.changeX = (block.rect.x + 10)
                    print(3)
                elif  self.rect.midtop[1] > block.rect.midtop[1] and self.rect.midright[0] < block.rect.midright[0] and self.rect.midleft[0] > block.rect.midleft[0]:
                    self.changeY = (block.rect.y + 10)
                    print(4)

                self.Xo = self.changeX
                self.Yo = self.changeY
                self.t = 0
                self.sin = 0
                self.cos = 0
                self.Voy = 0
                self.teste = 0

                self.ready = True

            else:
                # Otherwise if we are moving left, do the opposite.
                self.rect.left = block.rect.right

        # Move up/down
        # self.rect.y += self.changeY

        # Check and see if we hit anything
        block_hit_list = pygame.sprite.spritecollide(self, self.walls, False)
        for block in block_hit_list:
            # Reset our position based on the top/bottom of the object.
            if self.changeY > 0:
                self.rect.bottom = block.rect.top
            else:
                self.rect.top = block.rect.bottom

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

player.walls = wallsList

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
