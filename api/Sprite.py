# -*- coding: utf-8 -*-


import pygame
from api.GameObject import *

class Sprite(GameObject):

    def __init__(self):

        GameObject.__init__(self)

        # Imagen del sprite.
        # Usar setImage() en la clase superior para establecer una imagen.
        self.mImg = None

        # Indica si el sprite es visible o no.
        self.mVisible = True

        # Ancho y alto de la imagen. La función setImage() los actualiza.
        self.mWidth = 0
        self.mHeight = 0

        # Score del sprite.
        self.mScore = 0

    # Establecer la imagen del sprite.
    def setImage(self, aImg, aWidth, aHeight):

        if aWidth == 0 and aHeight == 0:
            self.mImg = aImg.convert_alpha()
            self.mWidth = self.mImg.get_width()
            self.mHeight = self.mImg.get_height()
        else:
            self.mImg = pygame.transform.scale(aImg, (aWidth, aHeight)).convert_alpha()
            self.mWidth = self.mImg.get_width()
            self.mHeight = self.mImg.get_height()
        
    def update(self):
        GameObject.update(self)

    def render(self, aScreen):
        if (self.mImg != None):
            if self.mVisible:
                aScreen.blit(self.mImg, (self.getX(), self.getY()))

    def getWidth(self):

        return self.mWidth

    def getHeight(self):

        return self.mHeight

    def collides(self, aSprite):
        #yo
        x1 = self.getX()
        y1 = self.getY()
        w1 = self.getWidth()
        h1 = self.getHeight()

        #el sprite a comparar
        x2 = aSprite.getX()
        y2 = aSprite.getY()
        w2 = aSprite.getWidth()
        h2 = aSprite.getHeight()
        
        if ((((x1 + w1) > x2) and (x1 < (x2 + w2))) and (((y1 + h1) > y2) and (y1 < (y2 + h2)))):
            #choca devuelve true
            return True
        else:
            #No Choca devuelve False
            return False

    # Establece si el sprite es visible o no.
    # Parámetro: True para que se dibuje, False para que no se dibuje.
    def setVisible(self, aVisible):
        self.mVisible = aVisible

    # Retorna True si el sprite es visible y False si no lo es.
    def isVisible(self):
        return self.mVisible

    # Establecer el score del sprite.
    def setScore(self, aScore):
        self.mScore = aScore

    # Obtener el score del sprite.
    def getScore(self):
        return self.mScore

    def destroy(self):
        GameObject.destroy(self)
        self.mImg = None
