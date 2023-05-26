# -*- coding: utf-8 -*-


from api.AnimatedSprite import *
from pygame import *
from api.Keyboard import *
from api.BulletManager import *
from game.Bullet import *
from api.GameConstants import *
from api.EnemyManager import *
from api.AudioManager import *
from game.GameData import *


class NavePlayer(AnimatedSprite):
    def __init__(self,aType):

        Sprite.__init__(self)

        self.SCREEN_WIDTH = GameConstants.inst().SCREEN_WIDTH
        self.SCREEN_HEIGHT = GameConstants.inst().SCREEN_HEIGHT

        #tamaño de la nave
        ancho = 250
        alto = 150

        self.type = aType

        #tipo nave
        name = None
        if self.type == 1:
            #Imagen Nave1
            name  = "assets/images/spaceships/Nave1/3D_Model/Hermes_ ("
            ancho, alto = 200,150
        elif self.type == 2:
            name = "assets/images/spaceships/Nave2/3D_Model/Hercules_ ("
        elif self.type == 3:
            name = "assets/images/spaceships/Nave3/3D_Model/Ares_ ("

        #cargo el array con la animacion mientras encuentre fotos
        bandera = True
        self.mFrames = []
        i = 1
        while (bandera):
            try:
                tmpImg = pygame.image.load(name + str(i) + ").png")
                # aca controlar el tamaño de las imagenes
                tmpImg = pygame.transform.scale(tmpImg, (ancho, alto)).convert_alpha()
                self.mFrames.append(tmpImg)
                i = i + 1
            except:
                #si da error es porque no bhay mas fotos para cargar :D
                bandera = False

        #tamaño de las naves
        self.mWidth = ancho
        self.mHeight = alto

    def getAnimation(self):
        return self.mFrames

    def getFrame(self, aFrame):
        return self.mFrames[aFrame]

    def destroy(self):
        AnimatedSprite.destroy(self)
        i = len(self.mFrames)
        while i > 0:
            self.mFrames[i - 1] = None
            self.mFrames.pop(i - 1)
            i = i - 1

    #devuelve el largo del array
    def getLength(self):
        return len(self.mFrames)
