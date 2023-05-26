# -*- coding: utf-8 -*-

class GameObject(object):

    # Comportamientos del objeto al llegar a un borde.
    NONE = 0     # No tiene ninguno, el objeto sigue de largo.
    STOP = 1     # El objeto se detiene al alcanzar un borde.
    WRAP = 2     # El objeto aparece por el lado contrario.
    BOUNCE = 3   # El objeto rebota en el borde.
    DIE = 4      # El objeto se marca para ser eliminado.
    
    def __init__(self):
        
        self.mX = 0
        self.mY = 0
        self.mVelX = 0
        self.mVelY = 0
        self.mAccelX = 0
        self.mAccelY = 0
        self.mMinX = -9999
        self.mMaxX = 9999
        self.mMinY = -9999
        self.mMaxY = 9999
        self.mBoundAction = GameObject.NONE
        self.mIsDead = False
        # Estado actual.
        self.mState = 0
        # Control del tiempo en el estado actual.
        self.mTimeState = 0

    def getX(self):
        return self.mX

    def getY(self):
        return self.mY

    def setX(self, aX):
        self.mX = aX

    def setY(self, aY):
        self.mY = aY

    def setXY(self, aX, aY):
        
        self.mX = aX
        self.mY = aY

    def setVelX(self, aVelX):
        
        self.mVelX = aVelX

    def setVelY(self, aVelY):
        
        self.mVelY = aVelY

    def setAccelX(self, aAccelX):
        
        self.mAccelX = aAccelX

    def setAccelY(self, aAccelY):
        
        self.mAccelY = aAccelY
        
    def setBounds(self, aMinX, aMinY, aMaxX, aMaxY):
        
        self.mMinX = aMinX
        self.mMaxX = aMaxX
        self.mMinY = aMinY
        self.mMaxY = aMaxY

    def setBoundAction(self, aBoundAction):

        self.mBoundAction = aBoundAction
        
    def update(self):
        self.mTimeState = self.mTimeState + 1

        self.mVelX += self.mAccelX
        self.mVelY += self.mAccelY

        self.mX += self.mVelX
        self.mY += self.mVelY

        self.checkBounds()

    def checkBounds(self):

        if self.mBoundAction == GameObject.NONE:
            return

        left = (self.mX < self.mMinX)
        right = (self.mX > self.mMaxX)
        up = (self.mY < self.mMinY)
        down = (self.mY > self.mMaxY)

        if not (left or right or up or down):
            return

        if (self.mBoundAction == GameObject.WRAP):
            if (left):
                self.mX = self.mMaxX
            if (right):
                self.mX = self.mMinX
            if (up):
                self.mY = self.mMaxY
            if (down):
                self.mY = self.mMinY
        else:
            if (left):
                self.mX = self.mMinX
            if (right):
                #Cuando llega al borde derecho en vez de rebotar muere
                self.setBoundAction(None)
                self.setBoundAction(GameObject.DIE)
                #self.mX = self.mMaxX
            if (up):
                self.mY = self.mMinY
            if (down):
                self.mY = self.mMaxY

        if (self.mBoundAction == GameObject.STOP or self.mBoundAction == GameObject.DIE):
            self.mVelX = 0
            self.mVelY = 0
        elif (self.mBoundAction == GameObject.BOUNCE):
            if (right or left):
                self.mVelX *= -1
            if (up or down):
                self.mVelY *= -1

        if (self.mBoundAction == GameObject.DIE):
            self.mIsDead = True
            return

    def isDead(self):
        return self.mIsDead

    def die(self):
        self.mIsDead = True

    def stopMove(self):
        self.mVelX = 0
        self.mVelY = 0
        self.mAccelX = 0
        self.mAccelY = 0

    def getState(self):
        return self.mState

    def setState(self, aState):
        self.mState = aState
        self.mTimeState = 0

    def getTimeState(self):
        return self.mTimeState
        
    def destroy(self):
        
        pass     
