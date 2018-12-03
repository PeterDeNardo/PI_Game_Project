# Pygame template - skeleton for a new pygame project
from help import *
import random
import math

# Power bar Class
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

# Player Class
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
        self.Vo = Vo/2

    def update(self):

        self.rect.x = self.changeX
        self.rect.y = self.changeY

        # Trata moedas
        moeda_hit_list = pygame.sprite.spritecollide(self, self.level.coin_list, True)

        for moeda in moeda_hit_list:
            self.score += 1

        # # Trata vida
        # chances_hit_list = pygame.sprite.spritecollide(self, self.level.chance_list, True)

        results = self.contructAngle()
        sinn = results[0]
        coss = results[1]

        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_RETURN and self.ready:
                self.contact = False
                self.ready = False
                self.portal_state = False
                self.portal_stage = ''
                self.sin = sinn
                self.cos = coss
                self.Voy = 10
                self.teste = 1
                self.direction = (results[2], results[3])
                self.launch(powerBar.height * 2)

        if event.type == pygame.KEYDOWN and self.portal_stage is not '':
            if event.key == pygame.K_0:
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
            if not self.ready:

                if (self.rect.midtop[1] < wall.rect.midtop[1] or self.rect.midtop[1] > wall.rect.midbottom[1]) and \
                        self.rect.midright[0] < wall.rect.midright[0] and \
                        self.rect.midleft[0] > wall.rect.midleft[0]:
                    self.changeY = (wall.rect.y - self.rect.height)

                elif self.rect.midtop[1] > wall.rect.midtop[1] and \
                        self.rect.midright[0] < wall.rect.midright[0] and \
                        self.rect.midleft[0] < wall.rect.midleft[0]:
                    self.changeX = (wall.rect.x - self.rect.width)

                elif self.rect.midtop[1] > wall.rect.midtop[1] and \
                        self.rect.midright[0] > wall.rect.midright[0] and \
                        self.rect.midleft[0] > wall.rect.midleft[0]:
                    self.changeX = (wall.rect.x + wall.width)

                elif self.rect.midtop[1] > wall.rect.midtop[1] and \
                        self.rect.midright[0] < wall.rect.midright[0] and \
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
                    if portal.color == PINK:
                        self.portal_stage = 'PINK'
                    if portal.color == PURPLE:
                        self.portal_stage = 'PURPLE'


                elif self.rect.midtop[1] > portal.rect.midtop[1] and self.rect.midright[0] < portal.rect.midright[0] and \
                        self.rect.midleft[0] < portal.rect.midleft[0]:
                    self.changeX = (portal.rect.x - self.rect.width)
                    if portal.color == BLUE:
                        self.portal_stage = 'BLUE'
                    if portal.color == PINK:
                        self.portal_stage = 'PINK'
                    if portal.color == PURPLE:
                        self.portal_stage = 'PURPLE'


                elif self.rect.midtop[1] > portal.rect.midtop[1] and self.rect.midright[0] > portal.rect.midright[0] and \
                        self.rect.midleft[0] > portal.rect.midleft[0]:
                    self.changeX = (portal.rect.x + portal.width)
                    if portal.color == BLUE:
                        self.portal_stage = 'BLUE'
                    if portal.color == PINK:
                        self.portal_stage = 'PINK'
                    if portal.color == PURPLE:
                        self.portal_stage = 'PURPLE'

                elif self.rect.midtop[1] > portal.rect.midtop[1] and self.rect.midright[0] < portal.rect.midright[0] and \
                        self.rect.midleft[0] > portal.rect.midleft[0]:
                    self.changeY = (portal.rect.y + portal.height)
                    if portal.color == BLUE:
                        self.portal_stage = 'BLUE'
                    if portal.color == PINK:
                        self.portal_stage = 'PINK'
                    if portal.color == PURPLE:
                        self.portal_stage = 'PURPLE'

                self.Xo = self.changeX
                self.Yo = self.changeY
                self.t = 0
                self.sin = 0
                self.cos = 0
                self.Voy = 0
                self.teste = 0
                self.ready = True

        for enemy in enemyCollisionList:
            # Vida

            chances_hit_list = pygame.sprite.spritecollide(self, self.level.chance_list, True)
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

    def resetPlayerStatus(self):
        self.chances = 3
        self.score = 0

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

# Coin Class
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

# Chance Class
class Chances(pygame.sprite.Sprite):
    player = None

    level = None

    def __init__(self, width, height):
        super().__init__()

        self.image = pygame.Surface([width, height])
        self.image.fill(PINK)

        self.rect = self.image.get_rect()

# Levels Class
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
        self.buttonsList = pygame.sprite.Group()
        self.texts_list = []
        self.buttons_list = []
        self.type = ""

        # Background image
        self.background = None

        # How far this world has been scrolled left/right
        # self.world_shift = 0
        # self.level_limit = -1000

    # Update everythign on this level
    def update(self):
        """ Update everything in this level."""
        self.wall_list.update()
        self.enemy_list.update()
        self.chance_list.update()
        self.player.update()
        self.powerBar.update()
        self.portal_list.update()
        if player.ready is True:
            for texts in self.texts_list:
                texto = font.render(texts[0], True, BLACK)
                screen.blit(texto, texts[1])

        if self.type == "normalLevel":
            hud_texts_list = [["{0}".format(powerBar.height), [2, 380]],
                               ["{0}".format(player.score), [500, 5]],
                               ["{0}".format(player.chances), [60, 5]]
                               ]
            for texts in hud_texts_list:
                texto = font.render(texts[0], True, WHITE)
                screen.blit(texto, texts[1])

            self.chances = []
            self.chances.append([40, 7])

            for chance in self.chances:
                chancez = Chances(15, 15)
                chancez.rect.x = chance[0]
                chancez.rect.y = chance[1]
                chancez.player = self.player
                self.chance_list.add(chancez)





    def draw(self, screen):
        """ Draw everything on this level. """
        # Draw all the sprite lists that we have
        self.wall_list.draw(screen)
        self.enemy_list.draw(screen)
        self.coin_list.draw(screen)
        self.chance_list.draw(screen)
        self.portal_list.draw(screen)
        self.player.draw(screen)
        self.powerBar.draw(screen)
        self.buttonsList.draw(screen)

    def setButtons(self, buttons):
        for button in buttons:
            buttonz = Button(button[0], button[1], button[2], button[3])
            self.buttons_list.append(buttonz)
            self.buttonsList.add(buttonz)


    def setWalls(self, walls):
        for wall in walls:
            wallz = Wall(wall[0], wall[1], wall[2], wall[3])
            self.wall_list.add(wallz)

    def setPortals(self, portals):
        for portal in portals:
            portalz = Portal(portal[0], portal[1], portal[2], portal[3], portal[4])
            self.portal_list.add(portalz)

    def setCoins(self, coins):
        for coin in coins:
            moeda = Coin(32, 32)
            moeda.rect.x = coin[0]
            moeda.rect.y = coin[1]
            self.coin_list.add(moeda)

    def setEnemies(self, enemies):
        for enemy in enemies:
            enemiez = Enemy(enemy[0], enemy[1], enemy[2], enemy[3], enemy[4], enemy[5])
            enemiez.player = self.player
            self.enemy_list.add(enemiez)

    def drawText(self, x, y, text, color):
        txt = font.render( str( text ), True, color)
        screen.blit( txt, (x, y))

# Menu Class
class Level_Menu(Level):

    def __init__(self, player):

        # Call the parent constructor
        Level.__init__(self, player)

        walls = [[20, 600, 0, 0], [1000, 20, 0, 0], [1000, 20, 0, 580], [20, 600, 980, 0]]

        self.type = "menu"

        self.buttons = [{"Name" : 'PLAY GAME',
                        "State" : 0},
                        {"Name" : 'HELP',
                        "State" : 0},
                        {"Name" : 'EXIT',
                         "State" : 0}]

        menus = [[120, 20, 200, 360], [120, 20, 200, 398], [120, 20, 200, 435]]

        self.setButtons(menus)

        self.setWalls(walls)

    def update(self):
        xx = WIDTH // 5
        yy = 360

        for i in range(len(self.buttons)):
            color = BLACK if (self.buttons[i]["State"] == 0) else RED
            self.drawText(xx, yy + (i * 38), self.buttons[i]["Name"], color)

        buttonOne = self.buttons_list[0]
        buttonTwo = self.buttons_list[1]
        buttonThree = self.buttons_list[2]

        # When you let go of the left mouse button in the area of a button, the button does something.
        if event.type == pygame.MOUSEBUTTONUP:
            if event.button == 1:
                global current_level_no
                global current_level
                if (buttonOne.rect.left < event.pos[0] < buttonOne.rect.right) and (
                        buttonOne.rect.top < event.pos[1] < buttonOne.rect.bottom):
                    current_level_no = 2  # World Map
                    current_level = level_list[current_level_no]
                    player.level = level_list[current_level_no]
                if (buttonTwo.rect.left < event.pos[0] < buttonTwo.rect.right) and (
                        buttonTwo.rect.top < event.pos[1] < buttonTwo.rect.bottom):
                    current_level_no = 1  # Tutorial Level
                    current_level = level_list[current_level_no]
                if (buttonThree.rect.left < event.pos[0] < buttonThree.rect.right) and (
                        buttonThree.rect.top < event.pos[1] < buttonThree.rect.bottom):
                    pygame.event.post(pygame.event.Event(QUIT))  # Exits the game

        # When you mouse-over a button, the text turns green.

        if event.type == pygame.MOUSEMOTION:
            if (buttonOne.rect.left < event.pos[0] < buttonOne.rect.right) and \
                    (buttonOne.rect.top < event.pos[1] < buttonOne.rect.bottom):
                self.buttons[0]["State"] = 1
            else:
                self.buttons[0]["State"] = 0
            if (buttonTwo.rect.left < event.pos[0] < buttonTwo.rect.right) and \
                    (buttonTwo.rect.top < event.pos[1] < buttonTwo.rect.bottom):
                self.buttons[1]["State"] = 1
            else:
                self.buttons[1]["State"] = 0
            if (buttonThree.rect.left < event.pos[0] < buttonThree.rect.right) and \
                    (buttonThree.rect.top < event.pos[1] < buttonThree.rect.bottom):
                self.buttons[2]["State"] = 1
            else:
                self.buttons[2]["State"] = 0

#Tutorial Class
class Level_Tutorial(Level):

    def __init__(self, player):

        # Call the parent constructor
        Level.__init__(self, player)

        walls = [[20, 600, 0, 0], [1000, 20, 0, 0], [1000, 20, 0, 580], [20, 600, 980, 0], [50, 100, 470, 240]]

        coins = [[250, 200]]

        enemies = [[50, 50, 50, 490, 500, 490]]

        portals = [[50, 50, 650, 350, PURPLE]]
        self.portals = portals
        self.type = "menu"
        self.texts_list = [["Hi, Welcome to Stick and Go!", [350, 100]],
                           ["the golden squares are coins they improve you score", [80, 175]],
                           ["and green squares are your enemies take care", [80, 500]],
                           ["the others colorful squares are portals to transport you", [350, 380]],
                           ["Esc to return!!!", [620, 500]]
                           ]

        self.buttons = [{"Name": 'COME BACK TO MENU!!! ',
                         "State": 0}]

        menus = [[120, 20, 200, 360]]

        self.setButtons(menus)

        self.setWalls(walls)

        self.setPortals(portals)

        self.setCoins(coins)

        self.setEnemies(enemies)

#Gameplay Levels
class Level_World_Map(Level):
    """ Definition for level 1. """

    def __init__(self, player):
        """ Create level 1. """

        # Call the parent constructor
        Level.__init__(self, player)
        # self.level_limit = -1500

        walls = [[40, 600, 0, 0], [1000, 30, 0, 0], [1000, 20, 0, 580], [20, 600, 980, 0], [50, 100, 470, 240]]

        # largura, altura, posicao a direita, posicao cima/baixo (quanto menor mais acima)
        self.portals = []
        portals = [50, 50, 270, 150, BLUE], [50, 50, 270, 350, PINK], [50, 50, 650, 150, YELLOW], [50, 50, 650, 350,
                                                                                                   RED]
        self.type = "normalLevel"
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

class Level_01(Level):
    """ Definition for level 1. """

    def __init__(self, player):
        """ Create level 1. """

        # Call the parent constructor
        Level.__init__(self, player)

        # self.level_limit = -1500

        walls = [[40, 600, 0, 0], [1000, 30, 0, 0], [1000, 20, 0, 580], [20, 600, 980, 0], [50, 100, 470, 240]]

        portals = [[50, 50, 700, 500, PURPLE]]

        enemies = [[50, 50, 500, 500, 500, 600], [50, 50, 400, 400, 400, 500]]

        coins = [[250, 200], [350, 100], [450, 300]]

        self.type = "normalLevel"



        self.player.add(player)
        self.powerBar.add(powerBar)

        self.setWalls(walls)

        self.setPortals(portals)

        self.setCoins(coins)

        self.setEnemies(enemies)

    def popChances(self):

        self.chances.pop(2)

class Level_02(Level):
    """ Definition for level 1. """

    def __init__(self, player):
        """ Create level 1. """

        # Call the parent constructor
        Level.__init__(self, player)

        # self.level_limit = -1500

        walls = [[40, 600, 0, 0], [1000, 30, 0, 0], [1000, 20, 0, 580], [20, 600, 980, 0], [50, 100, 470, 240]]

        portals = [[50, 50, 700, 200, PURPLE]]

        enemies = [[50, 50, 500, 500, 500, 600], [50, 50, 400, 400, 400, 500]]

        coins = [[250, 200], [350, 100], [450, 300]]

        self.type = "normalLevel"
        self.player.add(player)
        self.powerBar.add(powerBar)

        self.setWalls(walls)

        self.setPortals(portals)

        self.setCoins(coins)

        self.setEnemies(enemies)

# Objects Class
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

class Button(pygame.sprite.Sprite):

    def __init__(self, width, height, x, y):
        super().__init__()

        self.image = pygame.Surface([width, height])
        self.image.fill(WHITE)

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

# Farofada do Pygame
pygame.init()
pygame.mixer.init()
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("My Game")
clock = pygame.time.Clock()

player = Player()
powerBar = PowerBar()

allSprites = pygame.sprite.Group()

level_list = []
level_list.append(Level_Menu(player))
level_list.append(Level_Tutorial(player))
level_list.append(Level_World_Map(player))
level_list.append(Level_01(player))
level_list.append(Level_02(player))

current_level_no = 0
current_level = level_list[current_level_no]

player.level = current_level

allSprites.add(powerBar)

font = pygame.font.Font(None, 28)

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
    current_level.draw(screen)
    current_level.update()
    if player.portal_stage == 'BLUE' and player.portal_state is True:
        player.rect.x = 50
        player.rect.y = HEIGHT / 2
        player.changeX = player.rect.x
        player.changeY = player.rect.y
        player.resetPlayerPosition((50), HEIGHT / 2)

        current_level_no = 1
        current_level = level_list[current_level_no]
        player.level = current_level

        player.portal_stage = ''
        player.portal_state = False

    if player.portal_stage == 'PINK' and player.portal_state is True:
        player.rect.x = 50
        player.rect.y = HEIGHT / 2
        player.changeX = player.rect.x
        player.changeY = player.rect.y
        player.resetPlayerPosition((50), HEIGHT / 2)

        current_level_no = 2
        current_level = level_list[current_level_no]
        player.level = current_level

        player.portal_stage = ''
        player.portal_state = False

    if player.portal_stage == 'PURPLE' and player.portal_state is True:
        player.rect.x = 50
        player.rect.y = HEIGHT / 2
        player.changeX = player.rect.x
        player.changeY = player.rect.y
        player.resetPlayerPosition((50), HEIGHT / 2)

        current_level_no = 1
        current_level = level_list[current_level_no]
        player.level = current_level

        player.portal_stage = ''
        player.portal_state = False

    # if current_level_no == 0:
    #     if player.ready is True:
    #         textos = [["Hi, Welcome to Stick and Go!", [267, 130]],
    #                   ["Try to put your mouse curso on top of this Coin", [367, 230]],
    #                   ["{0}".format(powerBar.height), [25, 450]]
    #                   ]
    #         for texts in textos:
    #             texto = font.render(texts[0], True, BLACK)
    #             screen.blit(texto, texts[1])

    if current_level_no == 1:
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    current_level_no = 0
                    current_level = level_list[current_level_no]



    if current_level_no == 2:
        if player.portal_stage == 'BLUE':
            texto = font.render("BLUE", True, BLACK)
            screen.blit(texto, [267, 130])
        # if player.portal_stage == 'PINK':
        #     texto = font.render("PINK", True, BLACK)
        #     screen.blit(texto, [300, 300])
        # if player.portal_stage == 'YELLOW':
        #     texto = font.render("PINK", True, BLUE)
        #     screen.blit(texto, [300, 300])
        # if player.portal_stage == 'RED':
        #     texto = font.render("RED", True, YELLOW)
        #     screen.blit(texto, [300, 300])
        # if player.portal_stage == '':
        #     texto = None
        #     screen.blit(texto, [0, 0])

    # Draw / render

    # *after* drawing everything, flip the display
    pygame.display.flip()

pygame.quit()