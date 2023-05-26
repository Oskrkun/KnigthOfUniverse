# -*- coding: utf-8 -*-

import pygame
from api.Keyboard import *
from api.Game import *
from api.GameState import *
from game.states.LevelSpace import *
from api.TextSprite import *
from api.GameConstants import *
from game.NavesPlayer import *


class Loading(GameState):
    mImgSpace = None

    mTextTitle = None
    mTextPressFire = None
    mContador = 0
    mContadorTiempo = 0
    mContadorTiempoSec = 0

    def __init__(self):
        GameState.__init__(self)

        self.mImgSpace = None
        self.mTextTitle = None
        self.mTextPressFire = None
        self.mContador = 0
        self.mCLickStart = False
        self.x = 0
        self.contador = 0

        self.mContadorTiempo = 0
        self.mContadorTiempoSec = 0

    def init(self):
        GameState.init(self)

        self.x = 0
        self.contador = 0

        self.mContadorTiempo = 0
        self.mContadorTiempoSec = 0

        # Creo Las Estrellas
        self.stars = [Star() for _ in range(100)]


        # Cargar la imagen del fondo. La imagen es de 800x600 al igual que la pantalla.
        self.mImgSpace = pygame.image.load("assets/images/background/BackgroundStars.jpg")
        self.mImgSpace = pygame.transform.scale(self.mImgSpace, (GameConstants.inst().SCREEN_WIDTH, GameConstants.inst().SCREEN_HEIGHT)).convert_alpha()
        self.mImgSpace2 = self.mImgSpace


        self.VentanaSeleccion = pygame.image.load("assets/images/shipselection/Selected-SpaceSHip.png")
        self.VentanaSeleccion = pygame.transform.scale(self.VentanaSeleccion, (1168, 300)).convert_alpha()


        self.Guia_Teclas = pygame.image.load("assets/images/loading/guiaTeclasPlayer.png")
        self.Guia_Teclas = pygame.transform.scale(self.Guia_Teclas, (700, 80)).convert_alpha()

        self.loading0 = pygame.image.load("assets/images/loading/Loading_0.png")
        self.loading1 = pygame.image.load("assets/images/loading/Loading_1.png")
        self.loading2 = pygame.image.load("assets/images/loading/Loading_2.png")
        self.loading3 = pygame.image.load("assets/images/loading/Loading_3.png")
        self.loading4 = pygame.image.load("assets/images/loading/Loading_4.png")

        self.loading0 = pygame.transform.scale(self.loading0, (180, 20)).convert_alpha()
        self.loading1 = pygame.transform.scale(self.loading1, (180, 20)).convert_alpha()
        self.loading2 = pygame.transform.scale(self.loading2, (180, 20)).convert_alpha()
        self.loading3 = pygame.transform.scale(self.loading3, (180, 20)).convert_alpha()
        self.loading4 = pygame.transform.scale(self.loading4, (180, 20)).convert_alpha()

        self.pocision = (GameConstants.SCREEN_WIDTH - self.loading0.get_width() - 5,GameConstants.SCREEN_HEIGHT - self.loading0.get_height() - 5 )


        # Dibujar la imagen cargada en la imagen de fondo del juego.
        Game.inst().setBackground(self.mImgSpace)

    def update(self):
        GameState.update(self)

        # Mover las estrellas
        for star in self.stars:
            star.move(star.update2())

        # Mover el fondo
        if self.contador == 60:
            self.contador = 0
        elif self.contador <= 59:
            self.contador = self.contador + 1


        # Cronometro de carga del nivel
        if self.mContadorTiempoSec == 60:
            self.mContadorTiempoSec = 0
            self.mContadorTiempo += 1
        elif self.mContadorTiempoSec <= 59:
            self.mContadorTiempoSec = self.contador + 1


        # cuando pasen 4 segundos cambia de nivel
        if self.mContadorTiempo == 4:
            from game.states.LevelSpace import LevelSpace
            nextState = LevelSpace()
            Game.inst().setState(nextState)
            return

        # Esto es para mover el fondo
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
        for star in self.stars:
            star.draw(screen)

        #aca dibujo el loading
        if self.mContadorTiempoSec <= 20:
            screen.blit(self.loading0,self.pocision)
        elif self.mContadorTiempoSec <= 30:
            screen.blit(self.loading1,self.pocision)
        elif self.mContadorTiempoSec <= 40:
            screen.blit(self.loading2,self.pocision)
        elif self.mContadorTiempoSec <= 50:
            screen.blit(self.loading3,self.pocision)
        elif self.mContadorTiempoSec <= 60:
            screen.blit(self.loading4,self.pocision)

        screen.blit(self.VentanaSeleccion,(100,25))
        screen.blit(self.Guia_Teclas, (GameConstants.SCREEN_WIDTH / 2 - self.Guia_Teclas.get_width() / 2, 130))


    def destroy(self):
        GameState.destroy(self)

        self.fondo = None
        self.fondo = None

        self.VentanaSeleccion = None
        self.Guia_Teclas = None

        self.mImgSpace = None