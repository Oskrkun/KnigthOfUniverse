# -*- coding: utf-8 -*-

import pygame
from api.Keyboard import *
from api.Game import *
from api.GameState import *
from game.states.ShipSelection import *
from api.TextSprite import *
from game.EstrellasFondo import *
from game.GameData import *

class GameOver(GameState):

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

        self.x = 0
        self.contador = 0

        #Creo Las Estrellas
        self.stars = [Star() for _ in range(100)]


        # Cargar la imagen del fondo. La imagen es de 800x600 al igual que la pantalla.
        self.mImgSpace = pygame.image.load("assets/images/background/BackgroundStars.jpg")
        self.mImgSpace = self.mImgSpace.convert()

        # Cargar la imagen del fondo. La imagen es de 800x600 al igual que la pantalla.
        self.mImgSpace2 = self.mImgSpace

        # Dibujar la imagen cargada en la imagen de fondo del juego.
        Game.inst().setBackground(self.mImgSpace)

        #Creo el texto
        #Donde va a aparecer el texto (
        self.mTextGameOver = TextSprite("GAME OVER", 40, "assets/fonts/ROBO.ttf", (0xFF,0x00,0x00))
        self.mTextGameOver.setXY(GameConstants.inst().SCREEN_WIDTH /2 - self.mTextGameOver.getWidth() / 2, 200)

        self.mTextContinue = TextSprite("CONTINUE", 20, "assets/fonts/ROBO.ttf", (0xFF, 0xFF, 0xFF))
        self.mTextContinue.setXY(GameConstants.inst().SCREEN_WIDTH /2 - self.mTextContinue.getWidth(), 500)

        self.mTextExit = TextSprite("EXIT", 20, "assets/fonts/ROBO.ttf", (0xFF, 0xFF, 0xFF))
        self.mTextExit.setXY(GameConstants.inst().SCREEN_WIDTH /2 - self.mTextContinue.getWidth(), 550)


        self.Manito = pygame.image.load("assets\images\cursor\Manito.png")
        self.Manito = pygame.transform.scale(self.Manito, (70, 70)).convert_alpha()

        self.pocision = (GameConstants.inst().SCREEN_WIDTH /2 - self.mTextContinue.getWidth() + 120, 470)


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
            if self.pocision == (GameConstants.inst().SCREEN_WIDTH /2 - self.mTextContinue.getWidth() + 120, 470):
                if GameData.inst().getContinues() > 0:
                    GameData.inst().setContinues(GameData.inst().getContinues() - 1)
                    from game.states.LevelSpace import LevelSpace
                    nextState = LevelSpace()
                    Game.inst().setState(nextState)
                    return
            if self.pocision == (GameConstants.inst().SCREEN_WIDTH / 2 - self.mTextContinue.getWidth() + 120, 520):
                # Traigo los datos de GameData
                GameData.inst().setContinues(3)
                GameData.inst().setPuntajeJugador(0)
                from game.states.Menu import Menu
                nextState = Menu()
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

        self.mTextGameOver.update()
        self.mTextContinue.update()
        self.mTextExit.update()

        if Keyboard.inst().upPressed():
            self.pocision = (GameConstants.inst().SCREEN_WIDTH / 2 - self.mTextContinue.getWidth() + 120, 470)
        if Keyboard.inst().downPressed():
            self.pocision = (GameConstants.inst().SCREEN_WIDTH / 2 - self.mTextContinue.getWidth() + 120, 520)


    def render(self):

        GameState.render(self)
        screen = Game.inst().getScreen()

        # dibujo el fondo
        screen.blit(self.mImgSpace, (self.x, 0))
        screen.blit(self.mImgSpace2, (self.x + GameConstants.inst().SCREEN_WIDTH, 0))
        screen.blit(self.Manito,(self.pocision))

        # dibujo las estrellas
        for star in  self.stars:
            star.draw(screen)

        self.mTextGameOver.render(screen)
        self.mTextContinue.render(screen)
        self.mTextExit.render(screen)

    def destroy(self):
        GameState.destroy(self)

        self.stars = None

        self.fondo = None
        self.fondo = None

        self.mImgSpace = None