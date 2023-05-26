# -*- coding: utf-8 -*-

import pygame
from game.PowerUp import *
from api.PowerUpManager import *
from api.GameConstants import *

SCREEN_WIDTH = GameConstants.inst().SCREEN_WIDTH
SCREEN_HEIGHT = GameConstants.inst().SCREEN_HEIGHT

class PowersUpCreator(object):

    mInstance = None
    mInitialized = False

    TimeLapse = 0
    Frame = 0
    PowerUps = 0
    PowerUpsCreados = 0

    def __new__(self, *args, **kargs):
        if (PowersUpCreator.mInstance is None):
            PowersUpCreator.mInstance = object.__new__(self, *args, **kargs)
            self.init(PowersUpCreator.mInstance)
        else:
            print ("Cuidado: PowersUpCreator(): No se debería instanciar más de una vez esta clase. Usar PowersUpCreator.inst().")
        return self.mInstance

    @classmethod
    def inst(cls):
        if (not cls.mInstance):
            return cls()
        return cls.mInstance

    def init(self):
        if (PowersUpCreator.mInitialized):
            return
            PowersUpCreator.mInitialized = True

        PowersUpCreator.PowersUp = 0
        PowersUpCreator.PowersUpCreados = 0

    def getFrame(self):
        return PowersUpCreator.Frame

    def setFrame(self):

        if (int(PowersUpCreator.Frame) <= 60):
            PowersUpCreator.Frame += 1
        else:
            PowersUpCreator.Frame = 0
            PowersUpCreator.TimeLapse += 1

    def getTimeLapse(self):
        return PowersUpCreator.TimeLapse

    def getEnemigos(self):
        return PowersUpCreator.enemigos

    def getPowerUpsCreados(self):
        return PowersUpCreator.PowerUpsCreados

    def setEnemigos(self, aCantEnemigos):
        PowersUpCreator.enemigos = aCantEnemigos

    def actualizarPowersUp(self,aTiempoMax ):

        #subo el frame cada vez q entra al lopp del juego en el update
        PowersUpCreator.inst().setFrame()

        #tiempo max hasta que no salga ninguna wave mas

        tiempoMax = PowersUpCreator.inst().getTimeLapse() > aTiempoMax

        #random elige cuando va a aparecer entre 1 y x segundos
        poweruprandom = random.randrange(1, 2)

        #cada cuanto tiempo quiero que aparescan las Waves tiempoWaves = 6
        tiempoWaves = poweruprandom

        #el tiempo transcurrido desde que empeso el juego
        tiempo = PowersUpCreator.inst().getTimeLapse()

        #Bandera para saber si estoy en el primer frame del update para no crear la oleada 60 veces xD
        frame = PowersUpCreator.inst().getFrame() == 1

        if ( not tiempoMax and tiempo % tiempoWaves == 0  and frame ):
            PowersUpCreator.inst().PowersUpCreator(1)

    def PowersUpCreator(self,aCantidad):

        PowerUps = [PowerUp(SCREEN_WIDTH, SCREEN_HEIGHT) for _ in range(aCantidad)]

        # creo PowerUps
        i = 1
        for aPowerUps in PowerUps:
            aPowerUps.setBounds(0, 0, SCREEN_WIDTH, SCREEN_HEIGHT)

            # altura maxima de la pantalla donde va a aparecer el enemigo
            # compruebo que si la altura es 1080 le resto la altura de la nave
            # para que no quede dibujada afuera
            alturaRandom = random.randrange(0,SCREEN_HEIGHT - aPowerUps.getHeight())

            #distancia a la que van a aparecer
            distanciaRandom = random.randrange(SCREEN_WIDTH, SCREEN_WIDTH + 700)

            aPowerUps.setXY(distanciaRandom, alturaRandom)
            aPowerUps.setBounds(0, 0, SCREEN_WIDTH, SCREEN_HEIGHT)
            aPowerUps.setBoundAction(GameObject.NONE)

            #agrego al enemigo al manager de enemigos
            PowerUpManager.inst().addPowerUp(aPowerUps)
            print(i)
            i +1