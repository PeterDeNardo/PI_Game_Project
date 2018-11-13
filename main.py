# Pygame template - skeleton for a new pygame project
from help import *
import random
import math


# Classe da barra d eforca
class PowerBar(pygame.sprite.Sprite):

    def __init__(self):

        super().__init__()

        # Seta dados iniciais

        self.image = pygame.Surface((10, 1))
        self.image.fill(GREEN)
        self.rect = self.image.get_rect()
        self.rect.x = 10
        self.rect.y = 500
        self.height = 1
        self.weight = 10
        self.addition = 1

    def update(self):
        # Movimenta a barra quando SPACE estiver precionado
        self.rect = pygame.draw.rect(screen, GREEN, (10, 500, self.weight, -self.height))

        press_keys = pygame.key.get_pressed()
        if press_keys[pygame.K_SPACE]:
            self.height += self.addition
            self.image = pygame.Surface((10, self.height))
            if self.height >= 100:
                self.addition = -2
            if self.height <= 0:
                self.addition = 2

            if self.height >= 20:
                self.image.fill(YELLOW)
            if self.height >= 40:
                self.image.fill(BLUE)
            if self.height >= 60:
                self.image.fill(PINK)
            if self.height >= 80:
                self.image.fill(RED)

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
        self.portal_stage = ''
        self.portal_state = False

        self.eixoYA = self.rect.center
        self.eixoYB = (self.rect.center[0], (self.rect.center[1] + 10))

        self.eixoXA = self.rect.center
        self.eixoXB = ((self.rect.center[0] + 10), (self.rect.center[1]))
        self.sin = 0
        self.cos = 0
        self.teste = 0
        self.t = 0

        self.powerBar = PowerBar()

        self.changeX = self.rect.x
        self.changeY = self.rect.y

        # Determina se o jogador esta em contato com algo
        self.contact = False

        self.direction: bool

        # List of sprites we can bump against
        self.level = None

        # HP - Chances
        self.chances = 3

        # Score moeda
        self.score = 0

    def launch(self, Vo):
        self.Vo = Vo

    def update(self):

        self.rect.x = self.changeX
        self.rect.y = self.changeY

        # Trata moedas
        moeda_hit_list = pygame.sprite.spritecollide(self, self.level.coin_list, True)

        for moeda in moeda_hit_list:
            self.score += 1

        # Trata vida
        chances_hit_list = pygame.sprite.spritecollide(self, self.level.chance_list, True)

        # Vida
        for chances in chances_hit_list:
            if self.chances < 3:
                self.chances += 1

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

        if event.type == pygame.KEYDOWN and self.portal_stage is not '':
            if event.key == pygame.K_KP0:
                print('apertei')
                print('portal_stage eh ', player.portal_stage)
                self.portal_state = True

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
            self.changeY = (self.Yo) - (vY * self.t) + (self.teste * (9.8 * (self.t ** 2)) / 2)

            if self.teste == 1:
                self.t += 0.1

        # Colisao

        enemyCollisionList = pygame.sprite.spritecollide(self, self.level.enemy_list, False)
        portalCollisionList = pygame.sprite.spritecollide(self, self.level.portal_list, False)
        wallCollisionList = pygame.sprite.spritecollide(self, self.level.wall_list, False)

        for wall in wallCollisionList:
            # If we are moving right, set our right side to the left side of
            # the item we hit
            if not self.ready:

                if self.rect.midtop[1] < wall.rect.midtop[1] and self.rect.midright[0] < wall.rect.midright[0] and \
                        self.rect.midleft[0] > wall.rect.midleft[0]:
                    self.changeY = (wall.rect.y - self.rect.height)

                elif self.rect.midtop[1] > wall.rect.midtop[1] and self.rect.midright[0] < wall.rect.midright[0] and \
                        self.rect.midleft[0] < wall.rect.midleft[0]:
                    self.changeX = (wall.rect.x - self.rect.width)

                elif self.rect.midtop[1] > wall.rect.midtop[1] and self.rect.midright[0] > wall.rect.midright[0] and \
                        self.rect.midleft[0] > wall.rect.midleft[0]:
                    self.changeX = (wall.rect.x + wall.width)

                elif self.rect.midtop[1] > wall.rect.midtop[1] and self.rect.midright[0] < wall.rect.midright[0] and \
                        self.rect.midleft[0] > wall.rect.midleft[0]:
                    self.changeY = (wall.rect.y + wall.height)


                self.resetPlayerPosition(self.changeX, self.changeY)

        for portal in portalCollisionList:
            # If we are moving right, set our right side to the left side of
            # the item we hit

            print("Nextlevel")

            if not self.ready:

                if self.rect.midtop[1] < portal.rect.midtop[1] and self.rect.midright[0] < portal.rect.midright[0] and \
                        self.rect.midleft[0] > portal.rect.midleft[0]:
                    self.changeY = (portal.rect.y - self.rect.height)
                    if portal.color == BLUE:
                        self.portal_stage = 'BLUE'

                elif self.rect.midtop[1] > portal.rect.midtop[1] and self.rect.midright[0] < portal.rect.midright[0] and \
                        self.rect.midleft[0] < portal.rect.midleft[0]:
                    self.changeX = (portal.rect.x - self.rect.width)
                    if portal.color == BLUE:
                        self.portal_stage = 'BLUE'

                elif self.rect.midtop[1] > portal.rect.midtop[1] and self.rect.midright[0] > portal.rect.midright[0] and \
                        self.rect.midleft[0] > portal.rect.midleft[0]:
                    self.changeX = (portal.rect.x + portal.width)
                    if portal.color == BLUE:
                        self.portal_stage = 'BLUE'

                elif self.rect.midtop[1] > portal.rect.midtop[1] and self.rect.midright[0] < portal.rect.midright[0] and \
                        self.rect.midleft[0] > portal.rect.midleft[0]:
                    self.changeY = (portal.rect.y + portal.height)
                    if portal.color == BLUE:
                        self.portal_stage = 'BLUE'

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
            self.t = 0
            self.ready = True
            self.changeX = 50
            self.changeY = HEIGHT / 2
            self.Xo = self.changeX
            self.Yo = self.changeY
            self.chances -= 1

    def resetPlayerPosition(self, positionX, positionY):

        self.Xo = positionX
        self.Yo = positionY
        self.t = 0
        self.sin = 0
        self.cos = 0
        self.Voy = 0
        self.teste = 0
        self.ready = True

    def calcularDDP(self, pontoA, pontoB):
        distancia = (((pontoB[0] - pontoA[0]) ** 2 + (pontoB[1] - pontoA[1]) ** 2) ** 1 / 2)
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

        results = (distanciaCatOp / distanciaHy, distanciaCatAd / distanciaHy, directionX, directionY)

        return results


class Coin(pygame.sprite.Sprite):
    # Constructor. Pass in the color of the block,
    # and its x and y position
    player = None

    level = None

    def __init__(self, width, height):
        # Call the parent class (Sprite) constructor
        super().__init__()

        # Create an image of the block, and fill it with a color.
        # This could also be an image loaded from the disk.
        self.image = pygame.Surface([width, height])
        self.image.fill(YELLOW)

        # Fetch the rectangle object that has the dimensions of the image
        # image.
        # Update the position of this object by setting the values
        # of rect.x and rect.y
        self.rect = self.image.get_rect()

# Chances
class Chances(pygame.sprite.Sprite):
    player = None

    level = None

    def __init__(self, width, height):
        super().__init__()

        self.image = pygame.Surface([width, height])
        self.image.fill(PINK)

        self.rect = self.image.get_rect()


class Level(object):
    """ This is a generic super-class used to define a level.
        Create a child class for each level with level-specific
        info. """

    def __init__(self, player):
        """ Constructor. Pass in a handle to player. Needed for when moving
            platforms collide with the player. """

        self.wall_list = pygame.sprite.Group()
        self.enemy_list = pygame.sprite.Group()
        self.coin_list = pygame.sprite.Group()
        self.chance_list = pygame.sprite.Group()
        self.portal_list = pygame.sprite.Group()
        self.player = pygame.sprite.Group()
        self.powerBar = pygame.sprite.Group()

        chances = []
        chances.append([30, 30])
        chances.append([50, 30])
        chances.append([70, 30])

        # Background image
        self.background = None

        # How far this world has been scrolled left/right
        # self.world_shift = 0
        # self.level_limit = -1000

        for chance in chances:
            chancez = Chances(15, 15)
            chancez.rect.x = chance[0]
            chancez.rect.y = chance[1]
            chancez.player = self.player
            self.chance_list.add(chancez)

    # Update everythign on this level
    def update(self):
        """ Update everything in this level."""
        self.wall_list.update()
        self.enemy_list.update()
        self.chance_list.update()
        self.player.update()
        self.powerBar.update()

    def draw(self, screen):
        """ Draw everything on this level. """

        # Draw the background

        # Draw all the sprite lists that we have
        self.wall_list.draw(screen)
        self.enemy_list.draw(screen)
        self.coin_list.draw(screen)
        self.chance_list.draw(screen)
        self.portal_list.draw(screen)
        self.player.draw(screen)
        self.powerBar.draw(screen)

        # def shift_world(self, shift_x):
    #     """ When the user moves left/right and we need to scroll everything:
    #     """

    #     # Keep track of the shift amount
    #     self.world_shift += shift_x

    #     # Go through all the sprite lists and shift
    #     for platform in self.platform_list:
    #         platform.rect.x += shift_x

    #     for coin in self.coin_list:
    #         coin.rect.x += shift_x

    #     for life in self.life_list:
    #         life.rect.x += shift_x

    #     for monstro in self.monstro_list:
    #         monstro.rect.x += shift_x

class Level_World_Map(Level):
    """ Definition for level 1. """

    def __init__(self, player):
        """ Create level 1. """

        # Call the parent constructor
        Level.__init__(self, player)
        # self.level_limit = -1500

        walls = [[10, 600, 0, 0], [1000, 10, 0, 0], [1000, 10, 0, 590], [50, 100, 470, 240], [10, 600, 990, 0]]

        # largura, altura, posicao a direita, posicao cima/baixo (quanto menor mais acima)
        self.portals = []
        portals = [50, 50, 270, 150, BLUE], [50, 50, 270, 350, PINK], [50, 50, 650, 150, YELLOW], [50, 50, 650, 350, RED]
        self.portals = portals
        self.player.add(player)
        self.powerBar.add(powerBar)

        for wall in walls:
            wallz = Wall(wall[0], wall[1], wall[2], wall[3])
            wallz.player = self.player
            self.wall_list.add(wallz)

        for portal in portals:
            portalz = Portal(portal[0], portal[1], portal[2], portal[3], portal[4])
            portalz.player = self.player
            self.portal_list.add(portalz)

# Create platforms for the level
class Level_01(Level):
    """ Definition for level 1. """

    def __init__(self, player):
        """ Create level 1. """

        # Call the parent constructor
        Level.__init__(self, player)

        # self.level_limit = -1500

        walls = [[10, 600, 0, 0], [1000, 10, 0, 0], [1000, 10, 0, 590], [50, 100, 300, 300], [10, 600, 990, 0]]

        portals = [[50, 50, 700, 500, BLUE]]

        enemies = [[50, 50, 500, 500, 500, 600], [50, 50, 400, 400, 400, 500]]

        moedas = [[250, 200], [350, 100], [450, 300]]

        self.player.add(player)
        self.powerBar.add(powerBar)

        for coin in moedas:
            moeda = Coin(32, 32)
            moeda.rect.x = coin[0]
            moeda.rect.y = coin[1]
            moeda.player = self.player
            self.coin_list.add(moeda)

        for wall in walls:
            wallz = Wall(wall[0], wall[1], wall[2], wall[3])
            wallz.player = self.player
            self.wall_list.add(wallz)

        for portal in portals:
            portalz = Portal(portal[0], portal[1], portal[2], portal[3], portal[4])
            portalz.player = self.player
            self.portal_list.add(portalz)

        for enemy in enemies:
            enemiez = Enemy(enemy[0], enemy[1], enemy[2], enemy[3], enemy[4], enemy[5])
            enemiez.player = self.player
            self.enemy_list.add(enemiez)

class Wall(pygame.sprite.Sprite):

    def __init__(self, width, height, x, y):
        super().__init__()

        self.image = pygame.Surface([width, height])
        self.image.fill(BLACK)

        self.height = height
        self.width = width
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y

class Enemy(pygame.sprite.Sprite):
    def __init__(self, width, height, x, y, finalX, finalY):
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
        if not (self.rect.x == self.finalX and self.rect.y == self.finalY) and self.go:
            if self.finalX > self.inicialX:
                self.rect.x += 1
            elif self.finalX < self.inicialX:
                self.rect.x -= 1
            if self.finalY > self.inicialY:
                self.rect.y += 1
            elif self.finalY < self.inicialY:
                self.rect.y -= 1
        elif (self.rect.x == self.finalX and self.rect.y == self.finalY) or not self.go:
            self.go = False
            if self.finalX > self.inicialX:
                self.rect.x -= 1
            elif self.finalX < self.inicialX:
                self.rect.x += 1
            if self.finalY > self.inicialY:
                self.rect.y -= 1
            elif self.finalY < self.inicialY:
                self.rect.y += 1
            if self.rect.x == self.inicialX and self.rect.y == self.inicialY:
                self.go = True

class Portal(pygame.sprite.Sprite):
    def __init__(self, width, height, x, y, color):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.Surface([width, height])
        self.image.fill(color)

        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        self.height = height
        self.width = width
        self.color = color


pygame.init()
pygame.mixer.init()
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("My Game")
clock = pygame.time.Clock()


player = Player()
powerBar = PowerBar()

allSprites = pygame.sprite.Group()

# Make the walls. (x_pos, y_pos, width, height)
# wallsList = pygame.sprite.Group()
# enemyList = pygame.sprite.Group()
# portalList = pygame.sprite.Group()

level_list = []
level_list.append(Level_World_Map(player))
level_list.append(Level_01(player))

current_level_no = 0
current_level = level_list[current_level_no]

player.level = current_level

# player.walls = wallsList
# player.enemys = enemyList
# player.portals = portalList

allSprites.add(powerBar)

allSprites.add(player)

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

    # update
    current_level.update()

    if player.portal_stage == 'BLUE' and player.portal_state is True:
        player.resetPlayerPosition((50), HEIGHT/2)
        current_level_no = 1
        current_level = level_list[current_level_no]
        player.level = current_level

    # Draw / render
    current_level.draw(screen)
    # *after* drawing everything, flip the display
    pygame.display.flip()

pygame.quit()