# Pygame template - skeleton for a new pygame project
from help import *


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

        self.collideSound = pygame.mixer.Sound("poin.wav")
        self.portedSound = pygame.mixer.Sound("rururu.wav")
        self.dieSound = pygame.mixer.Sound("plush.wav")

        self.powerBar = PowerBar()

        self.changeX = self.rect.x
        self.changeY = self.rect.y

        # Determina se o jogador esta em contato com algo
        self.contact = False

        self.direction: bool

        # List of sprites we can bump against
        self.level = None
        self.level_no = 4

        # HP - Chances
        self.chances = 3

        # Score moeda
        self.score = 0

    def launch(self, Vo):
        self.Vo = Vo / 2

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

                self.collideSoundAction()
                self.resetPlayerPosition(self.changeX, self.changeY)

        for portal in portalCollisionList:

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
                    if portal.color == YELLOW:
                        self.portal_stage = 'YELLOW'


                elif self.rect.midtop[1] > portal.rect.midtop[1] and self.rect.midright[0] < portal.rect.midright[0] and \
                        self.rect.midleft[0] < portal.rect.midleft[0]:
                    self.changeX = (portal.rect.x - self.rect.width)
                    if portal.color == BLUE:
                        self.portal_stage = 'BLUE'
                    if portal.color == PINK:
                        self.portal_stage = 'PINK'
                    if portal.color == PURPLE:
                        self.portal_stage = 'PURPLE'
                    if portal.color == YELLOW:
                        self.portal_stage = 'YELLOW'

                elif self.rect.midtop[1] > portal.rect.midtop[1] and self.rect.midright[0] > portal.rect.midright[0] and \
                        self.rect.midleft[0] > portal.rect.midleft[0]:
                    self.changeX = (portal.rect.x + portal.width)
                    if portal.color == BLUE:
                        self.portal_stage = 'BLUE'
                    if portal.color == PINK:
                        self.portal_stage = 'PINK'
                    if portal.color == PURPLE:
                        self.portal_stage = 'PURPLE'
                    if portal.color == YELLOW:
                        self.portal_stage = 'YELLOW'

                elif self.rect.midtop[1] > portal.rect.midtop[1] and self.rect.midright[0] < portal.rect.midright[0] and \
                        self.rect.midleft[0] > portal.rect.midleft[0]:
                    self.changeY = (portal.rect.y + portal.height)
                    if portal.color == BLUE:
                        self.portal_stage = 'BLUE'
                    if portal.color == PINK:
                        self.portal_stage = 'PINK'
                    if portal.color == PURPLE:
                        self.portal_stage = 'PURPLE'
                    if portal.color == YELLOW:
                        self.portal_stage = 'YELLOW'

                self.Xo = self.changeX
                self.Yo = self.changeY
                self.t = 0
                self.sin = 0
                self.cos = 0
                self.Voy = 0
                self.teste = 0
                self.ready = True

                self.teleportedSoundAction()

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

            if self.chances == 0:
                global current_level_no
                global current_level
                current_level_no = 2
                current_level = level_list[current_level_no]
                self.resetPlayerStatus()

            self.dieSoundAction()



    def collideSoundAction(self):
        pygame.mixer.Sound.play(self.collideSound)

    def teleportedSoundAction(self):
        pygame.mixer.Sound.play(self.portedSound)

    def dieSoundAction(self):
        pygame.mixer.Sound.play(self.dieSound)


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

    def __init__(self, width, height, color):
        # Call the parent class (Sprite) constructor
        super().__init__()

        # Create an image of the block, and fill it with a color.
        # This could also be an image loaded from the disk.
        self.image = pygame.Surface([width, height])
        self.color = color
        self.image.fill(self.color)

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

        global current_level_no
        global current_level


        for texts in self.texts_list:
            texto = font.render(texts[0], True, BLACK)
            screen.blit(texto, texts[1])

        if current_level_no == 1 :
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    current_level_no = 0
                    current_level = level_list[current_level_no]

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

            if event.type == pygame.KEYDOWN:

                if event.key == pygame.K_r:
                    self.resetCoins()
                    player.rect.x = 50
                    player.rect.y = HEIGHT / 2
                    player.changeX = player.rect.x
                    player.changeY = player.rect.y
                    player.resetPlayerPosition((50), HEIGHT / 2)


                global levelPaused

                if event.key == pygame.K_ESCAPE:
                    levelPaused = current_level
                    current_level_no = 7
                    current_level = level_list[current_level_no]

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
            moeda = Coin(32, 32, coin[0])
            moeda.rect.x = coin[1]
            moeda.rect.y = coin[2]
            self.coin_list.add(moeda)

    def setEnemies(self, enemies):
        for enemy in enemies:
            enemiez = Enemy(enemy[0], enemy[1], enemy[2], enemy[3], enemy[4], enemy[5], enemy[6])
            enemiez.player = self.player
            self.enemy_list.add(enemiez)

    def drawText(self, x, y, text, color):
        txt = font.render(str(text), True, color)
        screen.blit(txt, (x, y))

    def waitToMenu(self):
        pygame.time.wait(500)

    def resetCoins(self):
        self.coin_list.draw(screen)

# Menu Class
class Level_Menu(Level):

    def __init__(self, player):

        # Call the parent constructor
        Level.__init__(self, player)

        walls = [[20, 600, 0, 0], [1000, 20, 0, 0], [1000, 20, 0, 580], [20, 600, 980, 0]]

        self.type = "menu"
        self.isActive = False

        self.texts_list = [["Stick and GO", [200, 300]]]

        self.buttons = [{"Name": 'PLAY GAME',
                         "State": 0},
                        {"Name": 'HELP',
                         "State": 0},
                        {"Name": 'EXIT',
                         "State": 0}]

        menus = [[120, 20, 200, 360], [120, 20, 200, 398], [120, 20, 200, 435]]

        self.setButtons(menus)

        self.setWalls(walls)

    def update(self):
        xx = WIDTH // 5
        yy = 360

        for texts in self.texts_list:
            texto = font.render(texts[0], True, BLACK)
            screen.blit(texto, texts[1])

        for i in range(len(self.buttons)):
            color = BLACK if (self.buttons[i]["State"] == 0) else RED
            self.drawText(xx, yy + (i * 38), self.buttons[i]["Name"], color)

        buttonOne = self.buttons_list[0]
        buttonTwo = self.buttons_list[1]
        buttonThree = self.buttons_list[2]

        # When you let go of the left mouse button in the area of a button, the button does something.
        if event.type == pygame.MOUSEBUTTONUP and self.isActive:
            if event.button == 1:
                global current_level_no
                global current_level
                if (buttonOne.rect.left < event.pos[0] < buttonOne.rect.right) and (
                        buttonOne.rect.top < event.pos[1] < buttonOne.rect.bottom):
                    current_level_no = 3  # World Map
                    current_level = level_list[current_level_no]
                    player.level = level_list[current_level_no]
                    player.level_no = current_level_no
                    print(22)
                if (buttonTwo.rect.left < event.pos[0] < buttonTwo.rect.right) and (
                        buttonTwo.rect.top < event.pos[1] < buttonTwo.rect.bottom) and current_level_no != 1:
                    current_level_no = 1  # Tutorial Level
                    current_level = level_list[current_level_no]
                if (buttonThree.rect.left < event.pos[0] < buttonThree.rect.right) and (
                        buttonThree.rect.top < event.pos[1] < buttonThree.rect.bottom):
                    pygame.event.post(pygame.event.Event(QUIT))  # Exits the game

        # When you mouse-over a button, the text turns green.

        if event.type == pygame.MOUSEMOTION and self.isActive :
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

class Level_GameOver(Level):
    def __init__(self, player):

        # Call the parent constructor
        Level.__init__(self, player)

        walls = [[20, 600, 0, 0], [1000, 20, 0, 0], [1000, 20, 0, 580], [20, 600, 980, 0]]

        self.type = "menu"
        self.isActive = False
        self.buttons = [{"Name": 'PLAY AGAIN',
                         "State": 0},
                        {"Name": 'MENU',
                         "State": 0}]

        menus = [[120, 20, 200, 360], [120, 20, 200, 398]]

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

        # When you let go of the left mouse button in the area of a button, the button does something.
        if event.type == pygame.MOUSEBUTTONUP and self.isActive:
            if event.button == 1:
                global current_level_no
                global current_level
                if (buttonOne.rect.left < event.pos[0] < buttonOne.rect.right) and (
                        buttonOne.rect.top < event.pos[1] < buttonOne.rect.bottom):
                    current_level_no = player.level_no  # World Map
                    current_level = level_list[current_level_no]
                    player.level = level_list[current_level_no]
                if (buttonTwo.rect.left < event.pos[0] < buttonTwo.rect.right) and (
                        buttonTwo.rect.top < event.pos[1] < buttonTwo.rect.bottom):
                    current_level = level_list[0] # Exits the game
                    current_level_no = 0
                    self.waitToMenu()
        # When you mouse-over a button, the text turns green.

        if event.type == pygame.MOUSEMOTION and self.isActive:
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

class Level_pause(Level):
    def __init__(self, player):

        # Call the parent constructor
        Level.__init__(self, player)

        walls = [[20, 600, 0, 0], [1000, 20, 0, 0], [1000, 20, 0, 580], [20, 600, 980, 0]]

        self.type = "menu"
        self.isActive = False
        self.buttons = [{"Name": 'CONTINUE',
                         "State": 0},
                        {"Name": 'MENU',
                         "State": 0}]

        menus = [[120, 20, 200, 360], [120, 20, 200, 398]]

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

        # When you let go of the left mouse button in the area of a button, the button does something.
        if event.type == pygame.MOUSEBUTTONUP and self.isActive:
            if event.button == 1:
                global current_level_no
                global current_level
                global levelPaused
                if (buttonOne.rect.left < event.pos[0] < buttonOne.rect.right) and (
                        buttonOne.rect.top < event.pos[1] < buttonOne.rect.bottom):
                    current_level = levelPaused
                if (buttonTwo.rect.left < event.pos[0] < buttonTwo.rect.right) and (
                        buttonTwo.rect.top < event.pos[1] < buttonTwo.rect.bottom):
                    current_level = level_list[0] # Exits the game
                    current_level_no = 0
                    self.waitToMenu()
        # When you mouse-over a button, the text turns green.

        if event.type == pygame.MOUSEMOTION and self.isActive:
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

class Level_Win(Level):
    def __init__(self, player):
        # Call the parent constructor
        Level.__init__(self, player)

        walls = [
            [20, 600, 0, 0],
            [1000, 20, 0, 0],
            [1000, 20, 0, 580],
            [20, 600, 980, 0],
            [50, 100, 470, 240]
        ]

        coins = [[YELLOW, 250, 200]]

        enemies = [[50, 50, 50, 490, 500, 490, GREEN]]

        self.first = 0
        self.second = 0
        self.secondText = ""

        portals = [[50, 50, 650, 350, PURPLE]]
        self.portals = portals
        self.type = "menu"

    def update(self):
        self.texts_list = [["YOU WIN", [445, 200]],
                           ["{0} / 50000".format(self.first), [420, 250]],
                           ["{0}".format(self.secondText), [422, 300]]]

        for texts in self.texts_list:
            texto = font.render(texts[0], True, BLACK)
            screen.blit(texto, texts[1])


        if self.first >= 50000 :
            self.first = 50000
            self.second = pygame.time.get_ticks()
            self.secondText = "congratulations"
            if self.second >= 20000:
                self.second = 20000
                self.theEnd()
        else :
            self.first = pygame.time.get_ticks()

    def theEnd(self):
        pygame.event.post(pygame.event.Event(QUIT))

# Tutorial Class
class Level_Tutorial(Level):

    def __init__(self, player):
        # Call the parent constructor
        Level.__init__(self, player)

        walls = [
            [20, 600, 0, 0],
            [1000, 20, 0, 0],
            [1000, 20, 0, 580],
            [20, 600, 980, 0],
            [50, 100, 470, 240]
        ]

        coins = [[YELLOW, 250, 200]]

        enemies = [[50, 50, 50, 490, 500, 490, GREEN]]

        portals = [[50, 50, 650, 350, PURPLE]]
        self.portals = portals
        self.type = "menu"
        self.texts_list = [["Hi, Welcome to Stick and Go!", [350, 40]],
                           ["your main goal is to collect all coins", [310, 70]],
                           ["but you'll soon realize that it's hard as heck", [280, 100]],
                           ["these little squares are coins, they improve your score", [80, 175]],
                           ["the black edges are walls", [200, 275]],
                           ["you should stick to them (literally)", [550, 275]],
                           ["and moving squares are your enemies, take care as they'll reposition you", [80, 500]],
                           ["they'll also take your HP away, but you'll probably not care", [80, 550]],
                           ["the others colorful squares are portals to transport you between stages", [250, 400]],
                           ["Press [Esc] to return", [750, 550]]
                           ]

        self.buttons = [{"Name": 'COME BACK TO MENU!!! ',
                         "State": 0}]

        menus = [[120, 20, 200, 360]]

        self.setButtons(menus)

        self.setWalls(walls)

        self.setPortals(portals)

        self.setCoins(coins)

        self.setEnemies(enemies)

# Gameplay Levels
class Level_World_Map(Level):
    """ Definition for level 1. """

    def __init__(self, player):
        """ Create level 1. """

        # Call the parent constructor
        Level.__init__(self, player)
        # self.level_limit = -1500

        walls = [
            [40, 600, 0, 0],
            [1000, 30, 0, 0],
            [1000, 20, 0, 580],
            [20, 600, 980, 0],
            [50, 50, 470, 275]]

        # largura, altura, posicao a direita, posicao cima/baixo (quanto menor mais acima)

        self.portals = []
        portals = [
            [50, 50, 470, 120, BLUE],
            [50, 50, 270, 350, PINK],
            [50, 50, 650, 350, YELLOW]
        ]

        self.type = "normalLevel"
        self.portals = portals
        self.player.add(player)
        self.powerBar.add(powerBar)

        self.setWalls(walls)

        self.setPortals(portals)

class Level_01(Level):
    """ Definition for level 1. """

    def __init__(self, player):
        """ Create level 1. """

        # Call the parent constructor
        Level.__init__(self, player)

        # self.level_limit = -1500

        walls = [
            [40, 600, 0, 0],  # paredes de contencao
            [1000, 30, 0, 0],  # paredes de contencao
            [1000, 20, 0, 590],  # paredes de contencao
            [20, 600, 980, 0],  # paredes de contencao
            [70, 50, 150, 400],
            [50, 200, 700, 400],
            [50, 200, 700, 10]
        ]

        portals = [[50, 50, 900, 125, PURPLE]]

        enemies = [
            [50, 50, 500, 500, 500, 600, BROWN],
            [50, 50, 400, 400, 400, 500, BROWN]
        ]

        coins = [
            [YELLOW, 175, 350],
            [YELLOW, 650, 75],
            [YELLOW, 450, 550]
        ]

        self.player.add(player)
        self.powerBar.add(powerBar)

        self.setWalls(walls)

        self.setPortals(portals)

        self.setCoins(coins)

        self.setEnemies(enemies)

        self.type = "normalLevel"

class Level_02(Level):
    """ Definition for level 1. """

    def __init__(self, player):
        """ Create level 1. """

        # Call the parent constructor
        Level.__init__(self, player)

        # self.level_limit = -1500

        walls = [
            [40, 600, 0, 0],  # paredes de contencao
            [1000, 30, 0, 0],  # paredes de contencao
            [1000, 20, 0, 590],  # paredes de contencao
            [20, 600, 980, 0],  # paredes de contencao
            [50, 200, 650, 200]
        ]

        portals = [[50, 50, 400, 225, PURPLE]]

        enemies = [
            [50, 50, 150, 100, 150, 350, BLUE],
            [50, 50, 350, 350, 500, 500, BLUE]
        ]

        coins = [
            [GREEN, 300, 20],
            [GREEN, 600, 275],
            [GREEN, 450, 550]
        ]

        self.player.add(player)
        self.powerBar.add(powerBar)

        self.setWalls(walls)

        self.setPortals(portals)

        self.setCoins(coins)

        self.setEnemies(enemies)

        self.type = "normalLevel"

class Level_03(Level):
    """ Definition for level 1. """

    def __init__(self, player):
        """ Create level 1. """

        # Call the parent constructor
        Level.__init__(self, player)

        # self.level_limit = -1500

        walls = [
            [40, 600, 0, 0],  # paredes de contencao
            [1000, 30, 0, 0],  # paredes de contencao
            [1000, 20, 0, 590],  # paredes de contencao
            [20, 600, 980, 0],  # paredes de contencao
        ]

        portals = [[50, 50, 850, 450, PURPLE]]

        enemies = [
            [50, 50, 150, 100, 150, 350, RED],
            [50, 50, 100, 400, 400, 100, RED]
        ]

        coins = [
            [BLUE, 150, 400],
            [BLUE, 475, 200],
            [BLUE, 800, 400]
        ]

        self.player.add(player)
        self.powerBar.add(powerBar)

        self.setWalls(walls)

        self.setPortals(portals)

        self.setCoins(coins)

        self.setEnemies(enemies)

        self.type = "normalLevel"

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
    def __init__(self, width, height, x, y, finalX, finalY, color):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.Surface([width, height])
        self.color = color
        self.image.fill(self.color)

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

menu = Level_Menu(player)
gameOver =  Level_GameOver(player)
pause = Level_pause(player)
win = Level_Win(player)

levelPaused = None

level_list = []
level_list.append(menu)
level_list.append(Level_Tutorial(player))
level_list.append(gameOver)
level_list.append(Level_World_Map(player))
level_list.append(Level_01(player))
level_list.append(Level_02(player))
level_list.append(Level_03(player))
level_list.append(pause)
level_list.append(win)

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
    if current_level_no == 0:
        menu.isActive = True
    else:
        menu.isActive = False
    if current_level_no == 2:
        gameOver.isActive = True
    else:
        gameOver.isActive = False
    if current_level_no == 7:
        pause.isActive = True
    else:
        pause.isActive = False

    if player.score >= 5 :
        current_level = win

    print(current_level_no)

    if player.portal_stage == 'BLUE' and player.portal_state is True:
        player.rect.x = 50
        player.rect.y = HEIGHT / 2
        player.changeX = player.rect.x
        player.changeY = player.rect.y
        player.resetPlayerPosition((50), HEIGHT / 2)

        current_level_no = 4
        current_level = level_list[current_level_no]
        player.level = current_level
        player.level_no = current_level_no

        player.portal_stage = ''
        player.portal_state = False

    if player.portal_stage == 'PINK' and player.portal_state is True:
        player.rect.x = 50
        player.rect.y = HEIGHT / 2
        player.changeX = player.rect.x
        player.changeY = player.rect.y
        player.resetPlayerPosition((50), HEIGHT / 2)

        current_level_no = 5
        current_level = level_list[current_level_no]
        player.level = current_level
        player.level_no = current_level_no
        print(player.level_no)
        player.portal_stage = ''
        player.portal_state = False

    if player.portal_stage == 'YELLOW' and player.portal_state is True:
        player.rect.x = 7
        player.rect.y = HEIGHT / 2
        player.changeX = player.rect.x
        player.changeY = player.rect.y
        player.resetPlayerPosition((50), HEIGHT / 2)

        current_level_no = 6
        current_level = level_list[current_level_no]
        player.level = current_level
        player.level_no = current_level_no

        player.portal_stage = ''
        player.portal_state = False

    if player.portal_stage == 'PURPLE' and player.portal_state is True:
        player.rect.x = 50
        player.rect.y = HEIGHT / 2
        player.changeX = player.rect.x
        player.changeY = player.rect.y
        player.resetPlayerPosition((50), HEIGHT / 2)

        current_level_no = 3
        current_level = level_list[current_level_no]
        player.level = current_level
        player.level_no = current_level_no

        player.portal_stage = ''
        player.portal_state = False




    # Draw / render

    # *after* drawing everything, flip the display
    pygame.display.flip()

pygame.quit()