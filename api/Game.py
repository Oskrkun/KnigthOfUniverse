# -*- coding: utf-8 -*-

import pygame
from api.Keyboard import *
from api.GameConstants import *
from api.Mouse import *
from game.MousePointer import *
import gc

class Game(object):

    mInstance = None
    mInitialized = False

    mScreen = None
    mImgBackground = None
    mClock = None
    mSalir = False
    mMousePointer = None

    # Pantalla (estado) actual del juego.
    mState = None

    SCREEN_WIDTH = 0
    SCREEN_HEIGHT = 0
    RESOLUTION = 0
    mIsFullscreen = False

    def __new__(self, *args, **kargs):
        if (Game.mInstance is None):
            Game.mInstance = object.__new__(self, *args, **kargs)
            self.init(Game.mInstance)
        else:
            print ("Cuidado: Game(): No se debería instanciar más de una vez esta clase. Usar Game.inst().")
        return self.mInstance

    @classmethod
    def inst(cls):
        if (not cls.mInstance):
            return cls()
        return cls.mInstance
    
    def init(self):
        if (Game.mInitialized):
            return
        Game.mInitialized = True

        Game.SCREEN_WIDTH = GameConstants.inst().SCREEN_WIDTH
        Game.SCREEN_HEIGHT = GameConstants.inst().SCREEN_HEIGHT
        Game.RESOLUTION = (Game.SCREEN_WIDTH, Game.SCREEN_HEIGHT)
        
        pygame.init()
        pygame.mixer.init()

        Game.mScreen = pygame.display.set_mode(Game.RESOLUTION)
        pygame.display.set_caption("Knigth Of Universe")

        Game.mBackground = pygame.Surface(self.mScreen.get_size())
        Game.mBackground = self.mBackground.convert()

        Game.mClock = pygame.time.Clock()
        Game.mSalir = False

        pygame.mouse.set_visible(False)
        Game.mMousePointer = MousePointer()

        Game.mState = None

    # Función para cambiar entre pantallas (estados) del juego.
    def setState(self, aState):
        if (Game.mState != None):
            Game.mState.destroy()
            Game.mState = None
            # Liberar memoria.
            gc.collect()
            
        Game.mState = aState
        Game.mState.init() 

    def gameLoop(self):

        while not self.mSalir:

            Game.mClock.tick(60)

            Keyboard.inst().update()
            Mouse.inst().update()
            Game.mMousePointer.update()
        
            for event in pygame.event.get():

                if event.type == pygame.QUIT:
                    Game.mSalir = True
                            
                if event.type == pygame.KEYUP:
                    if (event.key == pygame.K_ESCAPE):
                        Game.mSalir = True

                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_f:
                        Game.mIsFullscreen = not self.mIsFullscreen
                        if self.mIsFullscreen:
                            Game.mScreen = pygame.display.set_mode(Game.RESOLUTION, pygame.FULLSCREEN)
                        else:
                            Game.mScreen = pygame.display.set_mode(Game.RESOLUTION)
                    
                if event.type == pygame.KEYDOWN:
                    Keyboard.inst().keyDown(event.key)
                if event.type == pygame.KEYUP:
                    Keyboard.inst().keyUp(event.key)

            # Dibujar el fondo.
            Game.mScreen.blit(self.mBackground, (0, 0))

            # Update del estado del juego.
            Game.mState.update()

            # Dibujar el estado del juego.
            Game.mState.render()

            # Dibujar el puntero del mouse.
            Game.mMousePointer.render(self.mScreen)
        
            # Actualizar la pantalla.
            pygame.display.flip()

    def setBackground(self, aBackgroundImage):
        Game.mBackground = None
        Game.mBackground = aBackgroundImage
        self.blitBackground(Game.mBackground)
        
    def blitBackground(self, aBackgroundImage):
        Game.mScreen.blit(aBackgroundImage, (0, 0))

    def getScreen(self):
        return Game.mScreen
        
    def destroy(self):
        if (Game.mState != None):
            Game.mState.destroy()
            Game.mState = None

        Keyboard.inst().destroy()
        Mouse.inst().destroy()

        Game.mMousePointer.destroy()
        Game.mMousePointer = None

        pygame.mouse.set_visible(True)

        Game.mInstance = None

        pygame.quit()