# -*- coding: utf-8 -*-

import pygame
import random
from game.EnemyBullet import *
from api.GameConstants import *
from api.EnemyManager import *
from api.AnimatedSprite import *
from game.GameData import *

class Enemy(AnimatedSprite):

    NORMAL = 0
    EXPLODING = 1

    def __init__(self, aSCREEN_WIDTH,aSCREEN_HEIGHT):
        Sprite.__init__(self)

        tipoNave = random.randrange(1, 6)
        self.velNave = random.randrange(4, 10)

        self.mType = tipoNave

        self.VidaEnemigo = 0
        self.score = 0


        self.SCREEN_WIDTH = aSCREEN_WIDTH
        self.SCREEN_HEIGHT = aSCREEN_HEIGHT

        name = None
        ancho,alto = 0,0

        #cadatipo de enemigo setea su propio tamaño
        if self.mType == 1:
            name = "assets/images/enemy/enemy1_"
            ancho, alto = 135, 65
            self.setScore(5)
            self.VidaEnemigo = 10
        elif self.mType == 2:
            name = "assets/images/enemy/enemy2_"
            ancho, alto = 215, 65
            self.setScore(10)
            self.VidaEnemigo = 10
        elif self.mType == 3:
            name = "assets/images/enemy/enemy3_"
            ancho, alto = 360, 75
            self.setScore(20)
            self.VidaEnemigo = 10
        elif self.mType == 4:
            name = "assets/images/enemy/enemy4_"
            ancho, alto = 250, 185
            self.setScore(15)
            self.VidaEnemigo = 20
        elif self.mType == 5:
            name = "assets/images/enemy/enemy5_"
            ancho, alto = 380,265
            self.setScore(25)
            self.VidaEnemigo = 20

        # Cargar la secuencia de imágenes.
        self.mFramesNormal = []
        i = 0

        #while va hasta el largo de la animacion del enemigo cambiar segun la animacion
        while (i <= 0):
            tmpImg = pygame.image.load(name + str(i) + ".png")
            tmpImg = pygame.transform.scale(tmpImg, (ancho, alto)).convert_alpha()
            self.mFramesNormal.append(tmpImg)
            i = i + 1

        self.mWidth = self.mFramesNormal[0].get_width()
        self.mHeight = self.mFramesNormal[0].get_height()

        # Cargar la secuencia de imágenes de la explosion.
        self.mframesExplosion = []
        i = 1
        while (i <= 7):
            tmpImg = pygame.image.load("assets/images/explosion/Frame" + str(i) + ".png")
            tmpImg = pygame.transform.scale(tmpImg, (ancho, alto)).convert_alpha()
            self.mframesExplosion.append(tmpImg)
            i = i + 1

        # Estado inicial.
        self.mState = (Enemy.NORMAL)
        self.setState(Enemy.NORMAL)
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
            if self.mState == Enemy.NORMAL:
                self.controlFire()
                self.setVelX(-self.velNave)
            elif self.mState == Enemy.EXPLODING:
                if self.isEnded():
                    #GameData.inst().addScore(self.score)
                    self.die()
                    return
        AnimatedSprite.update(self,self.mWidth,self.mHeight)

    def getType(self):
        return self.mType

    def controlFire(self):
        # Ver si la nave dispara.
        if random.randrange(1, 70) == 1:
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
        if self.getState() == Enemy.NORMAL:
            self.initAnimation(self.mFramesNormal, 0, 8, True,self.mWidth,self.mHeight)
            #frames es el array, 0 es el frame en el que empiza, 8 el delay,animacion ciclica o no, tamaño del sprite
        elif self.getState() == Enemy.EXPLODING:
            self.initAnimation(self.mframesExplosion, 0, 2, False,self.mWidth,self.mHeight)
            # frames es el array, 0 es el frame en el que empiza, 8 el delay,animacion ciclica o no, tamaño del sprite

            self.soundExplosion.play()
            self.stopMove()

    # Invocada desde Bullet cuando la Nave es alcanzada por una bala.
    def hit(self,aDamage):
        if self.mState == Enemy.NORMAL:
            self.VidaEnemigo = self.VidaEnemigo - aDamage
            if self.VidaEnemigo <= 0:
                self.setState(Enemy.EXPLODING)
            else:
                self.VidaEnemigo = self.VidaEnemigo - aDamage

    def isStateNormal(self):
        return self.mState == Enemy.NORMAL

    def setScore(self, aScore):
        self.score= aScore

    def destroy(self):

        AnimatedSprite.destroy(self)

        #destrulle el array de frames dela nave
        i = len(self.mFrame)
        while i > 0:
            self.mFrame[i-1] = None
            self.mFrame.pop(i-1)
            i = i - 1
        # destrulle el array de frames de la explocion
        i = len(self.mframesExplosion)
        while i > 0:
            self.mframesExplosion[i-1] = None
            self.mframesExplosion.pop(i-1)
            i = i - 1
