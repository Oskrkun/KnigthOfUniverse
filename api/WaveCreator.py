# -*- coding: utf-8 -*-

import pygame
from game.Enemy import *
from api.GameConstants import *

SCREEN_WIDTH = GameConstants.inst().SCREEN_WIDTH
SCREEN_HEIGHT = GameConstants.inst().SCREEN_HEIGHT

class WaveCreator(object):

    mInstance = None
    mInitialized = False

    TimeLapse = 0
    Frame = 0
    enemigos = 0
    enemigosCreados = 0

    def __new__(self, *args, **kargs):
        if (WaveCreator.mInstance is None):
            WaveCreator.mInstance = object.__new__(self, *args, **kargs)
            self.init(WaveCreator.mInstance)
        else:
            print ("Cuidado: WaveCreator(): No se debería instanciar más de una vez esta clase. Usar WaveCreator.inst().")
        return self.mInstance

    @classmethod
    def inst(cls):
        if (not cls.mInstance):
            return cls()
        return cls.mInstance

    def init(self):
        if (WaveCreator.mInitialized):
            return
            WaveCreator.mInitialized = True

        WaveCreator.enemigos = 0
        WaveCreator.enemigosCreados = 0

    def getFrame(self):
        return WaveCreator.Frame

    def setFrame(self):

        if (int(WaveCreator.Frame) <= 60):
            WaveCreator.Frame += 1
        else:
            WaveCreator.Frame = 0
            WaveCreator.TimeLapse += 1

    def getTimeLapse(self):
        return WaveCreator.TimeLapse

    def getEnemigos(self):
        return WaveCreator.enemigos

    def getEnemigosCreados(self):
        return WaveCreator.enemigosCreados

    def setEnemigos(self, aCantEnemigos):
        WaveCreator.enemigos = aCantEnemigos


    def multiplo7(n):

        if n % 7 == 0:
            return True
        else:
            return False

    def actualizarEnemigos(self,aTiempoMax ):

        #subo el frame cada vez q entra al lopp del juego en el update
        WaveCreator.inst().setFrame()

        #tiempo max hasta que no salga ninguna wave mas

        tiempoMax = WaveCreator.inst().getTimeLapse() > aTiempoMax

        #cada cuanto tiempo quiero que aparescan las Waves
        tiempoWaves = 6

        #el tiempo transcurrido desde que empeso el juego
        tiempo = WaveCreator.inst().getTimeLapse()

        #Bandera para saber si estoy en el primer frame del update para no crear la oleada 60 veces xD
        frame = WaveCreator.inst().getFrame() == 1


        if ( not tiempoMax and tiempo % tiempoWaves == 0  and frame ):
            WaveCreator.inst().WaveCreator(8)


    def WaveCreator(self,aCantidad):

        enemies = [Enemy(SCREEN_WIDTH, SCREEN_HEIGHT) for _ in range(aCantidad)]

        # creo enemigos
        for aEnemies in enemies:

            if aEnemies.getType() == 1:
                subeOBaja = random.randint(1,2)

                subo = 0
                if subeOBaja == 1:
                    subo = 1
                else:
                    subo = -1

                # altura maxima de la pantalla donde va a aparecer el enemigo
                # compruebo que si la altura es 1080 le resto la altura de la nave
                # para que no quede dibujada afuera
                alturaRandom = random.randrange(0, SCREEN_HEIGHT - aEnemies.getHeight())

                aEnemies.setXY(SCREEN_WIDTH, alturaRandom)
                aEnemies.setVelX(10)
                aEnemies.setVelY(subo)
                aEnemies.setBounds(0, 0, SCREEN_WIDTH, SCREEN_HEIGHT)
                aEnemies.setBoundAction(GameObject.NONE)

                # agrego al enemigo al manager de enemigos
                EnemyManager.inst().addEnemy(aEnemies)

            else:
                # altura maxima de la pantalla donde va a aparecer el enemigo
                # compruebo que si la altura es 1080 le resto la altura de la nave
                # para que no quede dibujada afuera
                alturaRandom = random.randrange(0,SCREEN_HEIGHT - aEnemies.getHeight())

                #distancia a la que van a aparecer
                distanciaRandom = random.randrange(SCREEN_WIDTH, SCREEN_WIDTH + 700)

                aEnemies.setXY(distanciaRandom, alturaRandom)
                aEnemies.setBounds(0, 0, SCREEN_WIDTH, SCREEN_HEIGHT)
                aEnemies.setBoundAction(GameObject.NONE)

                #agrego al enemigo al manager de enemigos
                EnemyManager.inst().addEnemy(aEnemies)
