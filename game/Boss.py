# -*- coding: utf-8 -*-

import pygame
import random
from game.EnemyBullet import *
from api.GameConstants import *
from api.EnemyManager import *
from api.AnimatedSprite import *
from game.GameData import *

class Boss(AnimatedSprite):

    NORMAL = 0
    EXPLODING = 1
    HIT = 2

    def __init__(self, aSCREEN_WIDTH,aSCREEN_HEIGHT):
        Sprite.__init__(self)


        self.velNave =  0  #random.randrange(4, 10)

        self.mType = 1


        self.SCREEN_WIDTH = aSCREEN_WIDTH
        self.SCREEN_HEIGHT = aSCREEN_HEIGHT

        ancho, alto = 300, 300
        self.setScore(1500)
        self.VidaEnemigo = 1200
#---------------------------------------------------------------------------------------------------------------
        bandera = True
        self.mFramesNormal = []
        i = 0
        while (bandera):
            try:
                tmpImg = pygame.image.load("assets/images/enemy/boss/Normal/boss1_" + str(i) + ".png")
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
                tmpImg = pygame.image.load("assets/images/enemy/boss/Hit/boss1_" + str(i) + ".png")
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
                tmpImg = pygame.image.load("assets/images/enemy/boss/Exploding/boss1_" + str(i) + ".png")
                # aca controlar el tamaño de las imagenes
                tmpImg = pygame.transform.scale(tmpImg, (ancho, alto)).convert_alpha()
                self.mframesExplosion.append(tmpImg)
                i = i + 1
            except:
                # si da error es porque no bhay mas fotos para cargar :D
                bandera = False
#---------------------------------------------------------------------------------------------------------------

        # Estado inicial.
        self.mState = (Boss.NORMAL)
        self.setState(Boss.NORMAL)
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
            if self.mState == Boss.NORMAL:
                self.controlFire()
                self.setVelX(-self.velNave)
            elif self.mState == Boss.HIT:
                self.controlFire()
                self.setVelX(-self.velNave)
                if self.isEnded():
                    self.setState(Boss.NORMAL)
            elif self.mState == Boss.EXPLODING:
                if self.isEnded():
                    GameData.inst().addScore(self.getScore())
                    GameData.inst().bossVivo = False
                    self.die()
                    return

        AnimatedSprite.update(self,self.mWidth,self.mHeight)

    def getType(self):
        return self.mType

    def controlFire(self):
        # Ver si la nave dispara.
        pocisionX = self.getX() + self.getWidth() / 2
        pocisionY = self.getY() + random.randint(20 ,self.getHeight() / 2)
        velBala = 10

        if random.randrange(1, 2) == 1:
            if random.randrange(1, 30) == 1:
                # BALA 1
                # setear el tipo de bala
                self.soundShoot.play()
                b = EnemyBullet()
                b.setXY(pocisionX,pocisionY)
                b.setVelX(-velBala)
                b.setVelY(0)
                b.setBounds(0, 0, GameConstants.inst().SCREEN_WIDTH, GameConstants.inst().SCREEN_HEIGHT)
                b.setBoundAction(GameObject.DIE)
                EnemyManager.inst().addEnemy(b)
                self.soundShoot.play()

                # BALA 2
                # setear el tipo de bala
                self.soundShoot.play()
                b = EnemyBullet()
                b.setXY(pocisionX,pocisionY)
                b.setVelX(-velBala)
                b.setVelY(4)
                b.setBounds(0, 0, GameConstants.inst().SCREEN_WIDTH, GameConstants.inst().SCREEN_HEIGHT)
                b.setBoundAction(GameObject.DIE)
                EnemyManager.inst().addEnemy(b)
                self.soundShoot.play()

                # BALA 3
                # setear el tipo de bala
                self.soundShoot.play()
                b = EnemyBullet()
                b.setXY(pocisionX,pocisionY)
                b.setVelX(-velBala)
                b.setVelY(-4)
                b.setBounds(0, 0, GameConstants.inst().SCREEN_WIDTH, GameConstants.inst().SCREEN_HEIGHT)
                b.setBoundAction(GameObject.DIE)
                EnemyManager.inst().addEnemy(b)
                self.soundShoot.play()

    def render(self, aScreen):
        AnimatedSprite.render(self, aScreen)

    def setState(self, aState):
        AnimatedSprite.setState(self, aState)
        self.mTimeState = 0
        if self.getState() == Boss.NORMAL:
            self.initAnimation(self.mFramesNormal, 0, 8, True,self.mWidth,self.mHeight)
            #frames es el array, 0 es el frame en el que empiza, 8 el delay,animacion ciclica o no, tamaño del sprite
        elif self.getState() == Boss.HIT:
            self.initAnimation(self.mframesHit,0,8,False,self.mWidth,self.mHeight)
            # frames es el array, 0 es el frame en el que empiza, 8 el delay,animacion ciclica o no, tamaño del sprite
        elif self.getState() == Boss.EXPLODING:
            self.initAnimation(self.mframesExplosion, 0, 2, False,self.mWidth,self.mHeight)
            # frames es el array, 0 es el frame en el que empiza, 8 el delay,animacion ciclica o no, tamaño del sprite
            self.soundExplosion.play()
            self.stopMove()

    # Invocada desde Bullet cuando la Nave es alcanzada por una bala.
    def hit(self,aDamage):
        #si hay miniboss no me afecta nada
        minibossVivo = GameData.inst().getLiveMiniBoss()
        if minibossVivo == 0:
            if self.mState == Boss.NORMAL:
                self.VidaEnemigo = self.VidaEnemigo - aDamage
                if self.VidaEnemigo <= 0:
                    self.setState(Boss.EXPLODING)
                else:
                    self.VidaEnemigo = self.VidaEnemigo - aDamage
                    self.setState(Boss.HIT)

    def isStateNormal(self):
        return self.mState == Boss.NORMAL

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
