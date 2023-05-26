# -*- coding: utf-8 -*-

import pygame
from api.Sprite import *
from api.Mouse import *

class MousePointer(Sprite):

    def __init__(self):
        Sprite.__init__(self)

        img = pygame.image.load("assets/images/cursor/cursor.png")
        img = img.convert_alpha()
        self.setImage(img,50,50)

    def update(self):
        Sprite.update(self)
        self.setXY(Mouse.inst().getX(), Mouse.inst().getY())

    def render(self, aScreen):
        Sprite.render(self, aScreen)

    def destroy(self):
        Sprite.destroy(self)        
