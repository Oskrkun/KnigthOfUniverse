# -*- coding: utf-8 -*-

import pygame
import random
from game.EnemyBullet import *
from api.GameConstants import *
from api.EnemyManager import *
from api.AnimatedSprite import *
import sys, pygame, math
from game.GameData import *

class PowerUp(AnimatedSprite):

    NORMAL = 0
    EXPLODING = 1

    def __init__(self, aSCREEN_WIDTH,aSCREEN_HEIGHT):
        Sprite.__init__(self)

        tipoPowerUp = random.randrange(1, 7)

        # #esto es para que salgan pocas vidas
        # if tipoPowerUp == 6:
        #     #si es 6 vida extra tiro denuevo a ver si sale en un rango mas alto
        #     tipoPowerUp = random.randrange(1, 20)
        #     if tipoPowerUp != 6:
        #         #si no salio 6 pongo un power up entre los otros 5
        #         tipoPowerUp = random.randrange(1, 6)


        self.velPowerUp = 6

        self.mType = tipoPowerUp

        self.VidaPowerUp = 0


        self.step = 0
        self.Amplitud = 100
        self.Ondas = 0.05


        self.SCREEN_WIDTH = aSCREEN_WIDTH
        self.SCREEN_HEIGHT = aSCREEN_HEIGHT

        name = None
        ancho,alto = 70,70

        self.VidaPowerUp = 1

        self.alturaRandom = random.randint(100,668)

        #cadatipo de enemigo setea su propio tamaño
        if self.mType == 1:
            name = "assets/images/powerup/powerup1_"
            self.setScore(5)
        elif self.mType == 2:
            name = "assets/images/powerup/powerup2_"
            self.setScore(10)
        elif self.mType == 3:
            name = "assets/images/powerup/powerup3_"
            self.setScore(20)
        elif self.mType == 4:
            name = "assets/images/powerup/powerup4_"
            self.setScore(15)
        elif self.mType == 5:
            name = "assets/images/powerup/powerup5_"
            self.setScore(25)
        elif self.mType == 6:
            name = "assets/images/powerup/powerup6_"
            self.setScore(50)

        #cargo el array con la animacion mientras encuentre fotos
        bandera = True
        self.mFramesNormal = []
        i = 0
        while (bandera):
            try:
                tmpImg = pygame.image.load(name + str(i) + ".png")
                # aca controlar el tamaño de las imagenes
                tmpImg = pygame.transform.scale(tmpImg, (ancho, alto)).convert_alpha()
                self.mFramesNormal.append(tmpImg)
                i = i + 1
            except:
                #si da error es porque no bhay mas fotos para cargar :D
                bandera = False


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
        self.mState = (PowerUp.NORMAL)
        self.setState(PowerUp.NORMAL)
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
            if self.mState == PowerUp.NORMAL:
                self.setVelX(-self.velPowerUp)
                #movimiento sinusoidal coseno
                self.setY((-1 * math.cos(self.step) * self.Amplitud) + self.alturaRandom )

            elif self.mState == PowerUp.EXPLODING:
                if self.isEnded():
                    self.die()
                    return

        self.step += self.Ondas
        AnimatedSprite.update(self,self.mWidth,self.mHeight)

    def render(self, aScreen):
        AnimatedSprite.render(self, aScreen)

    def setState(self, aState):
        AnimatedSprite.setState(self, aState)
        self.mTimeState = 0
        if self.getState() == PowerUp.NORMAL:
            self.initAnimation(self.mFramesNormal, 0, 8, True,self.mWidth,self.mHeight)
            #frames es el array, 0 es el frame en el que empiza, 8 el delay,animacion ciclica o no, tamaño del sprite
        elif self.getState() == PowerUp.EXPLODING:
            self.initAnimation(self.mframesExplosion, 0, 2, False,self.mWidth,self.mHeight)
            # frames es el array, 0 es el frame en el que empiza, 8 el delay,animacion ciclica o no, tamaño del sprite

            self.soundExplosion.play()
            self.stopMove()

    # Invocada desde Bullet cuando la Nave es alcanzada por una bala.
    def hit(self,aDamage):
        if self.mState == PowerUp.NORMAL:
            self.VidaPowerUp = self.VidaPowerUp - aDamage
            if self.VidaPowerUp <= 0:
                self.setState(PowerUp.EXPLODING)
                #antes de explotar cambio el tipo de arma del jugador
                if self.mType == 1:
                    GameData.inst().setTipoBala(1)
                elif self.mType == 2:
                    GameData.inst().setTipoBala(2)
                elif self.mType == 3:
                    GameData.inst().setTipoBala(3)
                elif self.mType == 4:
                    GameData.inst().setTipoBala(4)
                elif self.mType == 5:
                    GameData.inst().setTipoBala(5)
                elif self.mType == 6:
                    GameData.inst().addShieldJugador(30)
            else:
                self.VidaPowerUp = self.VidaPowerUp - aDamage

    def isStateNormal(self):
        return self.mState == PowerUp.NORMAL

    def getType(self):
        return self.mType

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