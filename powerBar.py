from help import *
from main import *
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