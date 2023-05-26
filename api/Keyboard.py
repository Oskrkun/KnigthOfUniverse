# -*- coding: utf-8 -*-

import pygame

class Keyboard(object):

    mInstance = None
    mInitialized = False

    mLeftPressed = False
    mRightPressed = False
    mUpPressed = False
    mDownPressed = False
    m1Pressed = False
    m2Pressed = False
    m3Pressed = False

    mSpacePressedPreviousFrame = False
    mSpacePressed = False


    def __new__(self, *args, **kargs):
        if (Keyboard.mInstance is None):
            Keyboard.mInstance = object.__new__(self, *args, **kargs)
            self.init(Keyboard.mInstance)
        else:
            print ("Cuidado: Keyboard(): No se debería instanciar más de una vez esta clase. Usar Keyboard.inst().")
        return Keyboard.mInstance

    @classmethod
    def inst(cls):
        if (not cls.mInstance):
            return cls()
        return cls.mInstance
    
    def init(self):
        if (Keyboard.mInitialized):
            return
        Keyboard.mInitialized = True

        Keyboard.mLeftPressed = False
        Keyboard.mRightPressed = False
        Keyboard.mUpPressed = False
        Keyboard.mDownPressed = False
        Keyboard.m1Pressed = False
        Keyboard.m2Pressed = False
        Keyboard.m3Pressed = False

        Keyboard.mSpacePressedPreviousFrame = False
        Keyboard.mSpacePressed = False
        
    def keyDown(self, key):
        if (key == pygame.K_LEFT):
            Keyboard.mLeftPressed = True
        if (key == pygame.K_RIGHT):
            Keyboard.mRightPressed = True
        if (key == pygame.K_UP):
            Keyboard.mUpPressed = True
        if (key == pygame.K_DOWN):
            Keyboard.mDownPressed = True
        if (key == pygame.K_SPACE):
            Keyboard.mSpacePressed = True
        if (key == pygame.K_1):
            Keyboard.m1Pressed = True
        if (key == pygame.K_2):
            Keyboard.m2Pressed = True
        if (key == pygame.K_3):
            Keyboard.m3Pressed = True


    def keyUp(self, key):
        if (key == pygame.K_LEFT):
            Keyboard.mLeftPressed = False
        if (key == pygame.K_RIGHT):
            Keyboard.mRightPressed = False
        if (key == pygame.K_UP):
            Keyboard.mUpPressed = False
        if (key == pygame.K_DOWN):
            Keyboard.mDownPressed = False
        if (key == pygame.K_SPACE):
            Keyboard.mSpacePressed = False
        # cambiar de player
        if (key == pygame.K_1):
            Keyboard.m1Pressed = False
        if (key == pygame.K_2):
            Keyboard.m2Pressed = False
        if (key == pygame.K_3):
            Keyboard.m3Pressed = False

    def update(self):
        Keyboard.mSpacePressedPreviousFrame = Keyboard.mSpacePressed

    def leftPressed(self):
        return Keyboard.mLeftPressed

    def rightPressed(self):
        return Keyboard.mRightPressed

    def upPressed(self):
        return Keyboard.mUpPressed

    def OnePressed(self):
        return Keyboard.m1Pressed

    def TwoPressed(self):
        return Keyboard.m2Pressed

    def ThreePressed(self):
        return Keyboard.m3Pressed

    def downPressed(self):
        return Keyboard.mDownPressed

    def fire(self):
        return Keyboard.mSpacePressed == True and Keyboard.mSpacePressedPreviousFrame == False

    def destroy(self):
        Keyboard.mInstance = None
