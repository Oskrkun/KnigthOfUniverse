# -*- coding: utf-8 -*-


import pygame

# Importar la clase Sprite.
from api.Sprite import *

class AnimatedSprite(Sprite):

    def __init__(self):

        Sprite.__init__(self)

        # Array con los frames de la animación (las imágenes).
        self.mFrame = None
        # Frame actual de la animación.
        self.mCurrentFrame = 0
        # Control de cuando pasar de frame.
        self.mTimeFrame = 0
        # Cuantos frames deben pasar antes de pasar de imagen.
        self.mDelay = 0
        # Indica si la animación es cíclica (True) o no (False).
        self.mIsLoop = True
        # Indica si la animación no es cíclica y ha terminado.
        self.mEnded = False

    # Inicializa la animación del sprite. Establece el array de imágenes
    # de la animación, el frame actual, el delay de la animación y si la
    # animación es cíclica (al terminar comienza desde el principio), o no.
    def initAnimation(self, aFramesArray, aStartFrame, aDelay, aIsLoop, aWidth, aHeight):
        self.mFrame = aFramesArray
        self.mCurrentFrame = aStartFrame
        self.mTimeFrame = 0
        self.mDelay = aDelay
        self.mIsLoop = aIsLoop
        self.mEnded = False
        self.setImage(self.mFrame[self.mCurrentFrame],aWidth, aHeight)
        
    def update(self, aWidth, aHeight):
        Sprite.update(self)
        self.mTimeFrame = self.mTimeFrame + 1
        if (self.mTimeFrame > self.mDelay):
            self.mTimeFrame = 0
            # Si la animación no ha terminado, actualizar el cuadro de animación.
            if not self.mEnded:
                # Si es loop, se comienza desde el inicio. Sino queda
                # en el último cuadro.
                self.mCurrentFrame = self.mCurrentFrame + 1
                if self.mCurrentFrame >= len(self.mFrame):
                    # Si la animación es cíclica, comienza desde el inicio.
                    if self.mIsLoop:
                        self.mCurrentFrame = 0
                    # Si la animación no es cíclica, queda parado en el
                    # último cuadro y se marca que la animación ha terminado.
                    else:
                        self.mCurrentFrame = len(self.mFrame)-1
                        self.mEnded = True
                self.setImage(self.mFrame[self.mCurrentFrame],aWidth, aHeight)

    def render(self, aScreen):
        Sprite.render(self, aScreen)

    # Indica si la animación no es cíclica y ya ha terminado.
    def isEnded(self):
        return self.mEnded

    # Función para ir a un cuadro determinado de la animación
    # y quedarse en ese cuadro.
    def gotoAndStop(self, aFrame, aWidth, aHeight):
        if aFrame >= 0 and aFrame <= (len(self.mFrame) - 1):
            self.mCurrentFrame = aFrame
        self.setImage(self.mFrame[self.mCurrentFrame], aWidth, aHeight)
        self.mEnded = True

    # Función para ir a un cuadro determinado de la animación
    # y seguir con los cuadros siguientes.
    def gotoAndPlay(self, aFrame,aWidth,aHeight):
        if aFrame >= 0 and aFrame <= (len(self.mFrame)-1):
            self.mCurrentFrame = aFrame
            self.setImage(self.mFrame[self.mCurrentFrame],aWidth,aHeight)
            self.mEnded = False
            self.mTimeFrame = 0

    def destroy(self):
        Sprite.destroy(self)
        i = len(self.mFrame)
        while i > 0:
            self.mFrame[i-1] = None
            self.mFrame.pop(i-1)
            i = i - 1
