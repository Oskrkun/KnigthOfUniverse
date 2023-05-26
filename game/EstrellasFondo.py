# -*- coding: utf-8 -*-

import pygame
import math
from api.GameConstants import *

from random import randint
from api.Keyboard import *

class Star(object):

    def __init__(self):

        self.width = GameConstants.inst().SCREEN_WIDTH
        self.height = GameConstants.inst().SCREEN_HEIGHT

        self.rand_x = lambda: randint(0, self.width)
        self.rand_y = lambda: randint(0, self.height)


        #tamaño de las estrellas random
        self.SizeStar = randint(1,3)

        #color de las astrellas
        self.ColorStar = randint(1, 2)

        self.rect = pygame.Rect(self.rand_x(), self.rand_y(), 1, 1)

        #velocidad de las estrellas
        self.speed = randint(4, 7)

    def magnitude(self,aV):
        """returns the lenght of a vector"""
        return math.sqrt(sum(aV[i] * aV[i] for i in range(len(aV))))

    def normalize(self, aV):
        """normalizes a vector"""
        vmag = self.magnitude(aV)
        return [aV[i] / vmag for i in range(len(aV))]

    def move(self, vec):
        if vec == [0, 0]:
            return

        # move star by applying its speed
        # to the normalized movement vector
        self.rect.move_ip(*[self.speed * a for a in self.normalize(vec)])

        # control de bordes
        if self.rect.x > self.width:
            self.rect.x = 0
            self.rect.y = self.rand_y()
        elif self.rect.x < 0:
            self.rect.x = self.width
            self.rect.y = self.rand_y()
        if self.rect.y > self.height:
            self.rect.y = 0
            self.rect.x = self.rand_x()
        elif self.rect.y < 0:
            self.rect.y = self.height
            self.rect.x = self.rand_x()

    def draw(self, surface):
        if (self.ColorStar == 1):
            pygame.draw.circle(surface, pygame.Color('white'), self.rect.center, self.SizeStar)
        elif(self.ColorStar == 2):
             pygame.draw.circle(surface, pygame.Color('grey'), self.rect.center, self.SizeStar)



    def update2(self):
        return [-1, 0]

    def update(self):
        if (not Keyboard.inst().leftPressed() and not Keyboard.inst().rightPressed() and not Keyboard.inst().upPressed() and not Keyboard.inst().downPressed()):
            return [-1,0]
        elif Keyboard.inst().upPressed():
            return [-1, 1]
        elif Keyboard.inst().downPressed():
            return [-1, -1]
        else:
            return [-1, 0]