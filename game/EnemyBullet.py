# -*- coding: utf-8 -*-

import pygame

from api.Sprite import *


class EnemyBullet(Sprite):
    def __init__(self):
        Sprite.__init__(self)
        img = pygame.image.load("assets/images/bullets/bullet2.png").convert_alpha()
        #cambio el sentido de la bala enemiga
        img = pygame.transform.flip(img, True, False)
        #al setear la imagen le paso el tamaño que deberia quedar
        self.setImage(img,20,10)
        self.life = 1

    def update(self):
        Sprite.update(self)

    def isStateNormal(self):
        return False

    def render(self, aScreen):

        Sprite.render(self, aScreen)
    # Invocada desde Bullet cuando la bala enemiga es alcanzada por una bala del jugador.
    def hit(self,aDamage):
        if self.life - aDamage < 0:
            self.die()

    def destroy(self):
        Sprite.destroy(self)
