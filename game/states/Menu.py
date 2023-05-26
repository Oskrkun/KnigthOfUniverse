# -*- coding: utf-8 -*-

import pygame
from api.Keyboard import *
from api.Game import *
from api.GameState import *
from game.states.ShipSelection import *
from api.TextSprite import *
from game.EstrellasFondo import *
from game.states.BossLevel import *

class Menu(GameState):

    mImgSpace = None

    mTextTitle = None
    mTextPressFire = None
    mContador = 0

    mCLickStart = False

    def __init__(self):
        GameState.__init__(self)

        self.mImgSpace = None
        self.mTextTitle = None
        self.mTextPressFire = None
        self.mContador = 0
        self.mCLickStart = False
        self.x = 0
        self.contador = 0
    
    def init(self):
        GameState.init(self)

        GameData.bossVivo = True
        GameData.minibossVivo = 3
        GameData.tipoBalas = 1
        GameData.TimeLapse = 0
        GameData.mContinues = 0
        GameData.mPuntajeJugador = 0
        GameData.mVidasJugador = 3
        GameData.mShieldJugador = 100

        self.x = 0
        self.contador = 0

        #Creo Las Estrellas
        self.stars = [Star() for _ in range(100)]

        self.Titulo1 = pygame.image.load("assets/images/menu/Titulo_01.png")
        self.Titulo1 = pygame.transform.scale(self.Titulo1, (500, 100)).convert_alpha()
        self.Titulo2 = pygame.image.load("assets/images/menu/Titulo_02.png")
        self.Titulo2 = pygame.transform.scale(self.Titulo2, (500, 100)).convert_alpha()
        self.Titulo3 = pygame.image.load("assets/images/menu/Titulo_03.png")
        self.Titulo3 = pygame.transform.scale(self.Titulo3, (500, 100)).convert_alpha()

        self.Start_01 = pygame.image.load("assets/images/menu/Start_01.png")
        self.Start_01 = pygame.transform.scale(self.Start_01, (80, 30)).convert_alpha()
        self.Start_02 = pygame.image.load("assets/images/menu/Start_02.png")
        self.Start_02 = pygame.transform.scale(self.Start_02, (80, 30)).convert_alpha()
        self.Start_03 = pygame.image.load("assets/images/menu/Start_03.png")
        self.Start_03 = pygame.transform.scale(self.Start_03, (80, 30)).convert_alpha()


        self.key_Space = pygame.image.load("assets/images/HUD/buttons/space2.png")
        self.key_Space = pygame.transform.scale(self.key_Space, (110, 30)).convert_alpha()


        #Creo el texto
        #Donde va a aparecer el texto (
        self.mTextGuia = TextSprite("To start press :", 15, "assets/fonts/ROBO.ttf", (0xff,0xff,0xff))
        self.mTextGuia.setXY(GameConstants.SCREEN_WIDTH - (self.key_Space.get_width() + 20) - self.mTextGuia.getWidth() - 5, GameConstants.SCREEN_HEIGHT - self.mTextGuia.getHeight() - 10)


        # Cargar la imagen del fondo. La imagen es de 800x600 al igual que la pantalla.
        self.mImgSpace = pygame.image.load("assets/images/background/BackgroundStars.jpg")
        self.mImgSpace = self.mImgSpace.convert()

        # Cargar la imagen del fondo. La imagen es de 800x600 al igual que la pantalla.
        self.mImgSpace2 = self.mImgSpace


        # Dibujar la imagen cargada en la imagen de fondo del juego.
        Game.inst().setBackground(self.mImgSpace)

    def update(self):
        GameState.update(self)

        if (self.mContador <= 135):
            self.mContador +=1
        else:
            self.mContador = 0

        # Mover las estrellas
        for star in self.stars:
            star.move(star.update2())

        #esto hace que pase de un lv al otro (estado a otro)
        if Keyboard.inst().fire():
            from game.states.ShipSelection import ShipSelection
            nextState = ShipSelection()
            Game.inst().setState(nextState)
            return

        #Mover el fondo
        if self.contador == 60:
            self.contador = 0
        elif self.contador <= 59:
            self.contador  = self.contador + 1

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

        #dibujo el titulo
        screen.blit(self.Titulo1, (1368/2 - 500 / 2, 50))

        #dibujo el start q prende y apaga
        if self.mContador > 105 and self.mContador < 135 :
            screen.blit(self.Titulo3, (1368/2 - 500 / 2, 50))
        else:
            screen.blit(self.Titulo2, (1368 / 2 - 500 / 2, 50))

        if self.mContador  < 30:
            screen.blit(self.Start_01, (1368 / 2 - 80 / 2, 600))
        elif self.mContador < 35:
            screen.blit(self.Start_02, (1368 / 2 - 80 / 2, 600))
        elif self.mContador < 40:
            screen.blit(self.Start_03, (1368 / 2 - 80 / 2, 600))


        #dibujo la guia del boton a apretar en la esquina inferior derecha
        screen.blit(self.key_Space, (GameConstants.SCREEN_WIDTH - (self.key_Space.get_width() + 20), GameConstants.SCREEN_HEIGHT - self.key_Space.get_height() - 5))

        self.mTextGuia.render(screen)

    def destroy(self):
        GameState.destroy(self)

        self.stars = None

        self.fondo = None
        self.fondo = None

        self.Titulo1 = None
        self.Titulo1 = None
        self.Titulo1 = None

        self.Start_01 = None
        self.Start_02 = None
        self.Start_03 = None

        self.mImgSpace = None



