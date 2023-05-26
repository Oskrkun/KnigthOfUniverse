# -*- coding: utf-8 -*-

import pygame
from api.GameConstants import *
from game.NavesPlayer import *

class Assets(object):

    mInstance = None
    mInitialized = False

    mNave1 = []
    mNave2 = []
    mNave3 = []

    def __new__(self, *args, **kargs):
        if (Assets.mInstance is None):
            Assets.mInstance = object.__new__(self, *args, **kargs)
            self.init(Assets.mInstance)
        else:
            print("Cuidado: Assets(): No se debería instanciar más de una vez esta clase. Usar Assets.inst().")
        return Assets.mInstance

    @classmethod
    def inst(cls):
        if (not cls.mInstance):
            return cls()
        return cls.mInstance

    def init(self):
        Assets.mNave1 = NavePlayer(1)
        Assets.mNave2 = NavePlayer(2)
        Assets.mNave3 = NavePlayer(3)

    def GetNave(self,atype):
        if atype == 1:
            return Assets.inst().mNave1
        if atype == 2:
            return Assets.inst().mNave2
        if atype == 3:
            return Assets.inst().mNave3

    def destroy(self):
        Assets.mInstance = None