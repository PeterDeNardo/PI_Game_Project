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


class PowerBar(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.Surface((10, 1))
        self.image.fill(WHITE)
        self.rect = self.image.get_rect()
        self.rect.x = 10
        self.rect.y = 500
        self.height = 1
        self.weigth = 10
        self.addition = 1

    def update(self, *args):
        pygame.draw.rect(screen, WHITE, ( 10, 500, self.weigth, -self.height))

        pressKeys = pygame.key.get_pressed()
        if pressKeys[pygame.K_SPACE]:
            self.height += self.addition
            if self.height >= 100:
                self.addition = -1
            if self.height <= 0:
                self.addition = 1

        if event.type == pygame.KEYUP:
            if event.key == pygame.K_SPACE:
                player.launch(self.height)





class Player(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.Surface((10, 10))
        self.image.fill(RED)
        self.rect = self.image.get_rect()
        self.rect.x = 10
        self.rect.y = HEIGHT / 2
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

    def launch(self, Vo):
        self.Vo = Vo
        print(self.Vo)

    def update(self):
        self.eixoYA = self.rect.center
        self.eixoYB = (self.rect.center[0], (self.rect.center[1] + -10))
        self.eixoXA = self.rect.center
        self.eixoXB = ((self.rect.center[0] + 10), (self.rect.center[1]))
        self.angleLine = ((self.eixoXB[0], pygame.mouse.get_pos()[1]))
        self.catetoOposto = (self.eixoXB, self.angleLine)
        self.catetoAdjacente = (self.eixoXA, self.eixoXB)
        self.hypotenusa =  (self.eixoXA, self.angleLine)
        self.rect2 = pygame.draw.line(screen, WHITE, self.eixoYA, self.eixoYB, 1)
        self.rect2 = pygame.draw.line(screen, WHITE, self.eixoXA, self.eixoXB, 1)
        self.rect2 = pygame.draw.line(screen, WHITE, self.eixoXA, self.angleLine, 1)
        self.rect2 = pygame.draw.line(screen, WHITE, self.eixoXB, self.angleLine, 1)
        distanciaCatOp = self.calcularDDP(self.catetoOposto[0], self.catetoOposto[1])
        distanciaCatAd = self.calcularDDP(self.catetoAdjacente[0], self.catetoAdjacente[1])
        distanciaHy = self.calcularDDP(self.hypotenusa[0], self.hypotenusa[1])

        sinn = distanciaCatOp / distanciaHy
        coss = distanciaCatAd / distanciaHy

        if event.type == pygame.KEYUP:
            if event.key == pygame.K_SPACE and self.ready:
                self.sin = sinn
                self.cos = coss
                self.Voy = 10
                self.teste = 1
                self.ready = False

        vX = self.cos * self.Vo
        vY = self.sin * self.Vo

        self.rect.x = self.Xo + (vX * self.t)
        self.rect.y = (self.Yo) -(vY * self.t) + (self.teste * (9.8 * (self.t ** 2)) / 2)

        if self.teste == 1 :
            self.t += 0.1

    def calcularDDP(self, pontoA, pontoB):
        distancia = (((pontoB[0] - pontoA[0]) ** 2 + (pontoB[1] - pontoA[1]) ** 2) ** 1/2)
        return distancia




pygame.init()
pygame.mixer.init()
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("My Game")
clock = pygame.time.Clock()
allSprites = pygame.sprite.Group()
player = Player()
allSprites.add(player)
powerBar = PowerBar()
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


    screen.fill(BLACK)
    #update
    allSprites.update()
    # Draw / render
    allSprites.draw(screen)
    # *after* drawing everything, flip the display
    pygame.display.flip()

pygame.quit()




pygame.quit()
