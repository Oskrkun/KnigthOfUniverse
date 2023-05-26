# -*- coding: utf-8 -*-

import pygame
from api.WaveCreator import *

class GameData(object):

    mInstance = None
    mInitialized = False

    mPuntajeJugador = 0
    mVidasJugador = 0
    mShieldJugador = 0

    mContinues = 0

    TimeLapse = 0
    Frame = 0
    enemigos = 0
    enemigosCreados = 0
    tipoBalas = 1

    minibossVivo = 3
    bossVivo = True

    def __new__(self, *args, **kargs):
        if (GameData.mInstance is None):
            GameData.mInstance = object.__new__(self, *args, **kargs)
            self.init(GameData.mInstance)
        else:
            print ("Cuidado: GameData(): No se debería instanciar más de una vez esta clase. Usar GameData.inst().")
        return self.mInstance

    @classmethod
    def inst(cls):
        if (not cls.mInstance):
            return cls()
        return cls.mInstance

    def init(self):
        if (GameData.mInitialized):
            return
        GameData.mInitialized = True

        GameData.mPuntajeJugador = 0
        GameData.mVidasJugador = 0
        GameData.TimeLapse = 0
        GameData.Frame = 0

        GameData.mContinues = 3

        GameData.enemigos = 0
        GameData.enemigosCreados = 0

        GameData.tipoBalas = 1

        GameData.miniboss1Vivo = True
        GameData.miniboss2Vivo = True
        GameData.miniboss3Vivo = True
        GameData.bossVivo = True

    def setPuntajeJugador(self, aScore):
        GameData.mPuntajeJugador = aScore
        self.controlScores()

# ---------------------------------------------------------------------------------------------------------------
    def getLiveBoss(self):
        return GameData.bossVivo
    def getLiveMiniBoss(self):
        return GameData.minibossVivo

    def setMiniBoss(self,aMiniBoss):
        GameData.minibossVivo -= aMiniBoss
# ---------------------------------------------------------------------------------------------------------------

    def addScore(self, aScore):
        GameData.mPuntajeJugador += aScore
        self.controlScores()

    def controlScores(self):
        # Controlar que los scores no sean negativos o muy grandes.
        if (GameData.mPuntajeJugador < 0):
            GameData.mPuntajeJugador = 0
        if (GameData.mPuntajeJugador > 999999):
            GameData.mPuntajeJugador = 999999

    def controlEscudo(self):
        if (GameData.mShieldJugador < 0):
            GameData.mShieldJugador = 0
        if (GameData.mShieldJugador > 100):
            GameData.mShieldJugador = 100

    def getScore(self):
        return GameData.mPuntajeJugador

    def getFrame(self):
        return GameData.Frame

    def setVidasJugador(self, aLives):
        GameData.mVidasJugador = aLives
        self.controlLives()

    def getShieldJugador(self):
        return GameData.mShieldJugador

    def setShieldJugador(self,aEnergia):
        GameData.mShieldJugador = aEnergia
        self.controlEscudo()

    def addShieldJugador(selfs,aShield):
        if GameData.inst().getShieldJugador() + aShield >= 100:
            GameData.inst().setShieldJugador(100)
        else:
            GameData.inst().setShieldJugador(GameData.inst().getShieldJugador() + aShield)
            if GameData.inst().getShieldJugador() + aShield >= 100:
                GameData.inst().setShieldJugador(100)

    def addLives(self, aLives):
        GameData.mVidasJugador += aLives
        self.controlLives()

    def controlLives(self):
        # Controlar que las vidass no sean negativas o muy grandes.
        if (GameData.mVidasJugador < 0):
            GameData.mVidasJugador = 0
        if (GameData.mVidasJugador > 9):
            GameData.mVidasJugador = 9

    def getVidasJugador(self):
        return GameData.mVidasJugador

    def getContinues(self):
        return GameData.mContinues

    def setContinues(self,aContinue):
        GameData.mContinues = aContinue

    def setTipoBala(self, aTipoBala):
        GameData.tipoBalas = aTipoBala

    def getTipoBala(self):
        return GameData.tipoBalas


    def destroy(self):
        GameData.mInstance = None