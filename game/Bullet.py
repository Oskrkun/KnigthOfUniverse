
import pygame

from api.Sprite import *
from api.EnemyManager import *
from game.GameData import *


class Bullet(Sprite):

    def __init__(self,aType):
        Sprite.__init__(self)

        self.type = aType
        self.damage = 0

        self.alto = 0
        self.ancho = 0

        img = None
        if self.type == 1:
            img = pygame.image.load("assets/images/bullets/bullet1.png")
            self.damage = 10
            self.alto = 25
            self.ancho = 15
        elif self.type == 2:
            img = pygame.image.load("assets/images/bullets/bullet2.png")
            self.damage = 20
            self.alto = 25
            self.ancho = 15
        elif self.type == 3:
            img = pygame.image.load("assets/images/bullets/bullet3.png")
            self.damage = 30
            self.alto = 45
            self.ancho = 10
        elif self.type == 4:
            img = pygame.image.load("assets/images/bullets/bullet4.png")
            self.damage = 40
            self.alto = 35
            self.ancho = 20
        elif self.type == 5:
            img = pygame.image.load("assets/images/bullets/bullet5.png")
            self.damage = 50
            self.alto = 35
            self.ancho = 20
        elif self.type == 6:
            img = pygame.image.load("assets/images/bullets/bullet6.png")
            self.damage = 60
            self.alto = 35
            self.ancho = 20

        self.setImage(img, self.alto, self.ancho)

    def update(self):
        Sprite.update(self)
        enemy = EnemyManager.inst().collides(self)
        if enemy != None:
            if enemy.isStateNormal():
                enemy.hit(self.damage)
                self.die()

    def render(self, aScreen):
        Sprite.render(self, aScreen)

    def destroy(self):
        Sprite.destroy(self)

    def setType(self, aType):
        self.type = aType
