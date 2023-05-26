# -*- coding: utf-8 -*-

import pygame
from api.Keyboard import *
from api.Game import *
from api.GameState import *
from game.states.LevelSpace import *
from game.states.Loading import *
from api.TextSprite import *
from api.GameConstants import *
from game.NavesPlayer import *
from game.Assets import *

class ShipSelection(GameState):

    mImgSpace = None

    mTextTitle = None
    mTextPressFire = None
    mContador = 0

    def __init__(self):
        GameState.__init__(self)

        self.mImgSpace = None
        self.mTextTitle = None
        self.mTextPressFire = None
        self.mContador = 0
        self.mCLickStart = False
        self.x = 0
        self.contador = 0
        self.CirclePositionX = 0
        self.CirclePositionY = 0

        self.contadorFrames = 0
        self.Frame = 0
    
    def init(self):
        GameState.init(self)

        self.x = 0
        self.contador = 0

        self.contadorFrames = 0
        self.Frame = 0

        #Creo Las Estrellas
        self.stars = [Star() for _ in range(100)]

        self.CirclePositionX = 0
        self.CirclePositionY = 0

        self.nave_3D1 = Assets.inst().GetNave(1)
        self.frame3DNave = self.nave_3D1.getFrame(0)

        self.nave_3D2 = Assets.inst().GetNave(2)
        self.frame3DNave2 = self.nave_3D2.getFrame(0)

        self.nave_3D3 = Assets.inst().GetNave(3)
        self.frame3DNave3 = self.nave_3D3.getFrame(0)


        # Cargar la imagen del fondo. La imagen es de 800x600 al igual que la pantalla.
        self.mImgSpace = pygame.image.load("assets/images/background/BackgroundStars.jpg")
        self.mImgSpace = pygame.transform.scale(self.mImgSpace, (GameConstants.inst().SCREEN_WIDTH, GameConstants.inst().SCREEN_HEIGHT)).convert_alpha()

        self.mImgSpace2 = self.mImgSpace

        self.Nave1 = pygame.image.load("assets/images/shipselection/nave-1-seleccion.png")
        self.nave1_Stats = pygame.image.load("assets/images/shipselection/Ares_Stats.png")
        self.Nave1 = pygame.transform.scale(self.Nave1, (250, 250)).convert_alpha()
        self.nave1_Stats = pygame.transform.scale(self.nave1_Stats, (471, 270)).convert_alpha()

        self.Nave2 = pygame.image.load("assets/images/shipselection/nave-2-seleccion.png")
        self.nave2_Stats = pygame.image.load("assets/images/shipselection/Hercules_Stats.png")
        self.Nave2 = pygame.transform.scale(self.Nave2, (250, 250)).convert_alpha()
        self.nave2_Stats = pygame.transform.scale(self.nave2_Stats, (490, 270)).convert_alpha()

        self.Nave3 = pygame.image.load("assets/images/shipselection/nave-3-seleccion.png")
        self.nave3_Stats = pygame.image.load("assets/images/shipselection/Hermes_Stats.png")
        self.Nave3 = pygame.transform.scale(self.Nave3, (250, 250)).convert_alpha()
        self.nave3_Stats = pygame.transform.scale(self.nave3_Stats, (471, 270)).convert_alpha()


        self.VentanaSeleccion = pygame.image.load("assets/images/shipselection/Selected-SpaceSHip.png")
        self.VentanaSeleccion = pygame.transform.scale(self.VentanaSeleccion, (1168, 300)).convert_alpha()

        self.CircleSeleccion = pygame.image.load("assets/images/shipselection/Selected-SpaceShipCircle.png")
        self.CircleSeleccion = pygame.transform.scale(self.CircleSeleccion, (250, 250)).convert_alpha()

        self.Guia_Teclas = pygame.image.load("assets/images/shipselection/guia.png")
        self.Guia_Teclas = pygame.transform.scale(self.Guia_Teclas, (700, 45)).convert_alpha()


        # Dibujar la imagen cargada en la imagen de fondo del juego.
        Game.inst().setBackground(self.mImgSpace)

    def update(self):
        GameState.update(self)

        # if (self.CirclePositionX != 0 and self.CirclePositionY != 0):
        #     if Keyboard.inst().fire():
        #         from game.states.BossLevel import BossLevel
        #         nextState = BossLevel()
        #         Game.inst().setState(nextState)
        #         return

        if (self.CirclePositionX != 0 and self.CirclePositionY != 0):
            if Keyboard.inst().fire():
                from game.states.Loading import Loading
                nextState = Loading()
                Game.inst().setState(nextState)
                return

        #esta bien hacerlo aca? si porque solo lo hace cuando se preciona el boton
        #al cambiar el circulo de lugar cambio el modelo 3D de la nave3D
        if Keyboard.inst().OnePressed():
            GameConstants.inst().PLAYERSHIP = 1
            self.CirclePositionX = (GameConstants.SCREEN_WIDTH / 2 - self.Nave2.get_width() / 2 - 50 - self.Nave1.get_width())
            self.CirclePositionY = 450
        if Keyboard.inst().TwoPressed():
            GameConstants.inst().PLAYERSHIP = 2
            self.CirclePositionX = (GameConstants.SCREEN_WIDTH / 2 - self.Nave2.get_width() / 2)
            self.CirclePositionY = 450
        if Keyboard.inst().ThreePressed():
            GameConstants.inst().PLAYERSHIP = 3
            self.CirclePositionX = (GameConstants.SCREEN_WIDTH / 2 - self.Nave2.get_width() / 2 + 50 + self.Nave1.get_width())
            self.CirclePositionY = 450

        # Mover las estrellas
        for star in self.stars:
            star.move(star.update2())

        #Mover el fondo
        if self.contador == 60:
            self.contador = 0
        elif self.contador <= 59:
            self.contador  = self.contador + 1

        #animaciond de los modelos 3D de las naves
        if self.contadorFrames == 60:
            self.contadorFrames = 0
        else:
            if GameConstants.inst().PLAYERSHIP == 1:
                if self.Frame <= self.nave_3D1.getLength() - 1:
                    self.frame3DNave = self.nave_3D1.getFrame(self.Frame)
                else:
                    self.Frame = 0
            elif GameConstants.inst().PLAYERSHIP == 2:
                if self.Frame <= self.nave_3D2.getLength() - 1:
                    self.frame3DNave2 = self.nave_3D2.getFrame(self.Frame)
                else:
                    self.Frame = 0
            elif GameConstants.inst().PLAYERSHIP == 3:
                if self.Frame <= self.nave_3D3.getLength() - 1:
                    self.frame3DNave3 = self.nave_3D3.getFrame(self.Frame)
                else:
                    self.Frame = 0
            self.contadorFrames += 1
            if self.contadorFrames % 2 == 0:
                self.Frame += 1

        #Esto es para mover el fondo
        self.x = self.x - 1
        if self.x == -GameConstants.inst().SCREEN_WIDTH:
            self.x = 0


    def render(self):

        GameState.render(self)
        screen = Game.inst().getScreen()

        # dibujo el fondo
        screen.blit(self.mImgSpace, (self.x, 0))
        screen.blit(self.mImgSpace2, (self.x + GameConstants.inst().SCREEN_WIDTH, 0))

        # dibujo las estrellas
        for star in  self.stars:
            star.draw(screen)

        screen.blit(self.VentanaSeleccion,(100,25))

        #si el circulo eligio nave dibujo la nave correspondiente
        if (self.CirclePositionX != 0 and self.CirclePositionY != 0):
            if GameConstants.inst().PLAYERSHIP == 1:
                screen.blit(self.frame3DNave, (900, 100))
                screen.blit(self.nave3_Stats,(110,35))
            if GameConstants.inst().PLAYERSHIP == 2:
                screen.blit(self.frame3DNave2, (900, 100))
                screen.blit(self.nave2_Stats, (110,35))
            if GameConstants.inst().PLAYERSHIP == 3:
                screen.blit(self.frame3DNave3, (900, 100))
                screen.blit(self.nave1_Stats, (110,35))
        else:
            screen.blit(self.Guia_Teclas,(GameConstants.SCREEN_WIDTH / 2 - self.Guia_Teclas.get_width() / 2,130))

        if (self.CirclePositionX != 0 and self.CirclePositionY != 0):
            screen.blit(self.CircleSeleccion, (self.CirclePositionX, self.CirclePositionY))

        screen.blit(self.Nave1, (GameConstants.SCREEN_WIDTH / 2 - self.Nave2.get_width() / 2 - 50 - self.Nave1.get_width(), 450))
        screen.blit(self.Nave2, (GameConstants.SCREEN_WIDTH / 2 - self.Nave2.get_width() / 2, 450))
        screen.blit(self.Nave3, (GameConstants.SCREEN_WIDTH / 2 - self.Nave2.get_width() / 2 + 50 + self.Nave1.get_width(), 450))

    def destroy(self):
        GameState.destroy(self)
        self.Nave1 = None
        self.nave1_Stats = None
        self.Nave2 = None
        self.nave2_Stats = None
        self.Nave3 = None
        self.nave3_Stats = None

        self.Guia_Teclas = None

        self.nave_3D1 = None
        self.frame3DNave = None
        self.nave_3D2 = None
        self.frame3DNave2 = None
        self.nave_3D31 = None
        self.frame3DNave3 = None

        self.VentanaSeleccion = None
        self.CircleSeleccion = None
        self.fondo = None
        self.fondo = None

        self.mImgSpace = None