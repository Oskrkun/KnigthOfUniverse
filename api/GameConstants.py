# -*- coding: utf-8 -*-

class GameConstants(object):

    mInstance = None
    mInitialized = False

    SCREEN_WIDTH = 1368
    SCREEN_HEIGHT = 768

    PLAYERSHIP = 1




     #Tratando de obtener la resolucion de pantalla
     # infoObject = pygame.display.Info()
     # pygame.display.set_mode((infoObject.current_w, infoObject.current_h))
     #
     # SCREEN_WIDTHF = infoObject.current_w
     # SCREEN_HEIGHTF = infoObject.current_h

    def __new__(self, *args, **kargs):
        if (GameConstants.mInstance is None):
            GameConstants.mInstance = object.__new__(self, *args, **kargs)
            self.init(GameConstants.mInstance)
        else:
            print ("Cuidado: GameConstants(): No se debería instanciar más de una vez esta clase. Usar GameConstants.inst().")
        return self.mInstance

    @classmethod
    def inst(cls):
        if (not cls.mInstance):
            return cls()
        return cls.mInstance
    
    def init(self):
        if (GameConstants.mInitialized):
            return
        GameConstants.mInitialized = True
        
    def destroy(self):
        GameConstants.mInstance = None
