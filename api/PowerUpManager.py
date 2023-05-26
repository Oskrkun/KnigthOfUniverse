# -*- coding: utf-8 -*-

import pygame
from api.ManagerPU import *

class PowerUpManager(ManagerPU):

    mInstance = None
    mInitialized = False

    def __new__(self, *args, **kargs):
        if (PowerUpManager.mInstance is None):
            PowerUpManager.mInstance = object.__new__(self, *args, **kargs)
            self.init(PowerUpManager.mInstance)
        else:
            print ("Cuidado: PowerUpManager(): No se debería instanciar más de una vez esta clase. Usar PowerUpManager.inst().")
        return self.mInstance

    @classmethod
    def inst(cls):
        if (not cls.mInstance):
            return cls()
        return cls.mInstance
    
    def init(self):
        if (PowerUpManager.mInitialized):
            return
            PowerUpManager.mInitialized = True
            ManagerPU.__init__(self)

    def update(self):
        ManagerPU.update(self)

    def render(self, aScreen):
        ManagerPU.render(self, aScreen)

    def addPowerUp(self, aPowerUp):
        ManagerPU.add(self, aPowerUp)
      
    def destroy(self):
        ManagerPU.destroy(self)

        ManagerPU.mInstance = None
