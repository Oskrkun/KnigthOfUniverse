# -*- coding: utf-8 -*-

import pygame
import random
from game.EnemyBullet import *
from api.GameConstants import *
from api.EnemyManager import *
from api.AnimatedSprite import *
from game.GameData import *
import math

class MiniBoss(AnimatedSprite):

    NORMAL = 0
    EXPLODING = 1
    HIT = 2

    def __init__(self, aSCREEN_WIDTH,aSCREEN_HEIGHT):
        Sprite.__init__(self)

        self.mType = 1

# ---------------------------------------------------------------------------------------------------------------
        #giro en circulos

        # Radio aleatorio, desde 10 a 200
        self.radio = 200

        self.angulo = 0
        # Ángulo de inicio aleatorio, desde 0 a 2pi
        #self.angulo = random.random() * 2 * math.pi

        # radianes por fotograma.
        self.velocidad = 0.01

        # Este es el "centro" que el sprite orbitará
        self.centrar_x = 0
        self.centrar_y = 0

        self.SCREEN_WIDTH = aSCREEN_WIDTH
        self.SCREEN_HEIGHT = aSCREEN_HEIGHT

        ancho, alto = 120, 120
        self.setScore(1500)
        self.VidaEnemigo = 600


#---------------------------------------------------------------------------------------------------------------
        bandera = True
        self.mFramesNormal = []
        i = 0
        while (bandera):
            try:
                tmpImg = pygame.image.load("assets/images/enemy/miniBoss/Normal/miniBoss1_" + str(i) + ".png")
                # aca controlar el tamaño de las imagenes
                tmpImg = pygame.transform.scale(tmpImg, (ancho, alto)).convert_alpha()
                self.mFramesNormal.append(tmpImg)
                i = i + 1
            except:
                #si da error es porque no bhay mas fotos para cargar :D
                bandera = False

        self.mWidth = self.mFramesNormal[0].get_width()
        self.mHeight = self.mFramesNormal[0].get_height()

#---------------------------------------------------------------------------------------------------------------
        # Cargar la secuencia de imágenes del HIT
        self.mframesHit = []
        bandera = True
        i = 0
        while (bandera):
            try:
                tmpImg = pygame.image.load("assets/images/enemy/miniBoss/Hit/miniBoss1_" + str(i) + ".png")
                # aca controlar el tamaño de las imagenes
                tmpImg = pygame.transform.scale(tmpImg, (ancho, alto)).convert_alpha()
                self.mframesHit.append(tmpImg)
                i = i + 1
            except:
                # si da error es porque no bhay mas fotos para cargar :D
                bandera = False

#---------------------------------------------------------------------------------------------------------------
        # Cargar la secuencia de imágenes de la explosion.
        self.mframesExplosion = []
        bandera = True
        i = 0
        while (bandera):
            try:
                tmpImg = pygame.image.load("assets/images/enemy/miniBoss/Exploding/miniBoss1_" + str(i) + ".png")
                # aca controlar el tamaño de las imagenes
                tmpImg = pygame.transform.scale(tmpImg, (ancho, alto)).convert_alpha()
                self.mframesExplosion.append(tmpImg)
                i = i + 1
            except:
                # si da error es porque no bhay mas fotos para cargar :D
                bandera = False
#---------------------------------------------------------------------------------------------------------------
        # Estado inicial.
        self.mState = (MiniBoss.NORMAL)
        self.setState(MiniBoss.NORMAL)
        # Crear el sonido de disparo.
        self.soundShoot = pygame.mixer.Sound("assets/sounds/enemy_shoot.wav")
        # Sonido de explosión.
        self.soundExplosion = pygame.mixer.Sound("assets/sounds/enemy_explosion.wav")

    def setResolution(self, aSCREEN_WIDTH, aSCREEN_HEIGHT):
        self.SCREEN_WIDTH = aSCREEN_WIDTH
        self.SCREEN_HEIGHT = aSCREEN_HEIGHT

    def update(self):
        if self.getX() < 0 - self.getWidth():
            self.die()
        else:
            if self.mState == MiniBoss.NORMAL:
                self.controlFire()
                self.girarEnCirculos()
            elif self.mState == MiniBoss.HIT:
                self.controlFire()
                self.girarEnCirculos()
                if self.isEnded():
                    self.setState(MiniBoss.NORMAL)
            elif self.mState == MiniBoss.EXPLODING:
                if self.isEnded():
                    GameData.inst().setMiniBoss(1)
                    GameData.inst().addScore(self.getScore())
                    self.die()
                    return

        AnimatedSprite.update(self,self.mWidth,self.mHeight)

    def girarEnCirculos(self):
        self.setX(self.radio * math.sin(self.angulo) + self.centrar_x)
        self.setY(self.radio * math.cos(self.angulo) + self.centrar_y)

        # Incrementamos el ángulo para la siguiente ronda.
        self.angulo += self.velocidad

    def centerSpriteXY(self, aCentrar_x, aCentrar_y):
        self.centrar_x = aCentrar_x
        self.centrar_y = aCentrar_y

    def setRadio(self, aRadio):
        self.radio = aRadio

    def getType(self):
        return self.mType

    def controlFire(self):
        # Ver si la nave dispara.
        if random.randrange(1, 250) == 1:
            b = EnemyBullet()
            #de donde sale la bala
            b.setXY(self.getX() + 40 , self.getY() + self.getHeight()/2)
            #Direccion y Velocidad de la Bala
            b.setVelX(-25)
            b.setVelY(0)
            #BORDES DE LA BALA
            b.setBounds(0, 0, GameConstants.inst().SCREEN_WIDTH, GameConstants.inst().SCREEN_HEIGHT)
            b.setBoundAction(GameObject.DIE)
            EnemyManager.inst().addEnemy(b)
            self.soundShoot.play()

    def render(self, aScreen):
        AnimatedSprite.render(self, aScreen)

    def setState(self, aState):
        AnimatedSprite.setState(self, aState)
        self.mTimeState = 0
        if self.getState() == MiniBoss.NORMAL:
            self.initAnimation(self.mFramesNormal, 0, 8, True,self.mWidth,self.mHeight)
            #frames es el array, 0 es el frame en el que empiza, 8 el delay,animacion ciclica o no, tamaño del sprite
        elif self.getState() == MiniBoss.HIT:
            self.initAnimation(self.mframesHit,0,8,False,self.mWidth,self.mHeight)
            # frames es el array, 0 es el frame en el que empiza, 8 el delay,animacion ciclica o no, tamaño del sprite
        elif self.getState() == MiniBoss.EXPLODING:
            self.initAnimation(self.mframesExplosion, 0, 2, False,self.mWidth,self.mHeight)
            # frames es el array, 0 es el frame en el que empiza, 8 el delay,animacion ciclica o no, tamaño del sprite
            self.soundExplosion.play()
            self.stopMove()

    # Invocada desde Bullet cuando la Nave es alcanzada por una bala.
    def hit(self,aDamage):
        if self.mState == MiniBoss.NORMAL:
            self.VidaEnemigo = self.VidaEnemigo - aDamage
            if self.VidaEnemigo <= 0:
                self.setState(MiniBoss.EXPLODING)
            else:
                self.VidaEnemigo = self.VidaEnemigo - aDamage
                self.setState(MiniBoss.HIT)

    def isStateNormal(self):
        return self.mState == MiniBoss.NORMAL

    def setAngleStart(self, aAngle):
        self.angulo = aAngle


    def destroy(self):

        AnimatedSprite.destroy(self)

        #destrulle el array de frames dela nave
        i = len(self.mFrame)
        while i > 0:
            self.mFrame[i-1] = None
            self.mFrame.pop(i-1)
            i = i - 1

        # destrulle el array de frames del HIT
        i = len(self.mframesHit)
        while i > 0:
            self.mframesHit[i-1] = None
            self.mframesHit.pop(i-1)
            i = i - 1

        # destrulle el array de frames de la explocion
        i = len(self.mframesExplosion)
        while i > 0:
            self.mframesExplosion[i-1] = None
            self.mframesExplosion.pop(i-1)
            i = i - 1
