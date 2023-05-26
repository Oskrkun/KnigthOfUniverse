# -*- coding: utf-8 -*-

from api.GameState import *
from api.Game import *
from game.Player import *
from game.GameData import *
from api.WaveCreator import *
from api.TextSprite import *
from game.EstrellasFondo import *
from api.GameConstants import *
from game.states.GameOver import *
from api.PowersUpCreator import *
from api.PowerUpManager import *
from game.Boss import *
from game.MiniBoss import *
from game.states.WinGame import *


class BossLevel(GameState):
    mPlayer = None
    mImgSpace = None
    mTextScore1 = None
    mTextShield1 = None
    mTextLives1 = None

    # Relacionado a las estrellas
    stars = None
    stars2 = None
    vec = None

    fondo = None
    fondo2 = None
    x = 0
    contador = 0

    mContadorTiempo = 0
    mContadorTiempoSec = 0
    tiempomax = 0

    def __init__(self):
        GameState.__init__(self)

        self.mImgSpace = None

        self.mPlayer = None

        self.mTextScore1 = None
        self.mTextShield1 = None
        self.mTextLives1 = None

        # Relacionado a las estrellas
        self.stars = None
        self.stars2 = None
        self.vec = None

        self.fondo = None
        self.fondo2 = None

        self.x = 0
        self.contador = 0

        self.mContadorTiempo = 0
        self.mContadorTiempoSec = 0

        self.tiempomax = 0


    # Función donde se inicializan los elementos necesarios del nivel.
    def init(self):
        GameState.init(self)

        # Creo Las Estrellas
        self.stars = [Star() for _ in range(50)]
        self.stars2 = [Star() for _ in range(50)]

        self.x = 0
        self.contador = 0

        self.mImgSpace = pygame.image.load("assets/images/background/BackgroundStars.jpg").convert()

        self.fondo = pygame.image.load("assets/images/background/BackgroundStars.jpg").convert()
        self.fondo2 = self.fondo

        # Dibujar la imagen cargada en la imagen de background.
        Game.inst().setBackground(self.mImgSpace)

        # Creo el Jugador
        self.mPlayer = Player(GameConstants.inst().SCREEN_WIDTH, GameConstants.inst().SCREEN_HEIGHT,
                              GameConstants.inst().PLAYERSHIP)
        self.posicion = (GameConstants.inst().SCREEN_HEIGHT / 2) - (self.mPlayer.getHeight() / 2)
        self.mPlayer.setXY(0, self.posicion)

        # Cargo el Sonido
        # Música de background (loop) del juego.
        pygame.mixer.music.load("assets/sounds/music_game.ogg")
        pygame.mixer.music.play(-1)  # -1 para que se repita infinitamente

        # Creo el texto
        # Donde va a aparecer el texto
        self.mTextPuntaje = TextSprite("SCORE: " + str(GameData.inst().getScore()), 20, "assets/fonts/ROBO.ttf",
                                       (0xFF, 0xFF, 0xFF))
        self.mTextPuntaje.setXY(5, 5)
        self.mTextShield = TextSprite("SHIELD: " + str(GameData.inst().getShieldJugador()), 20, "assets/fonts/ROBO.ttf",
                                      (0xFF, 0xFF, 0xFF))
        self.mTextShield.setXY(5, 25)
        self.mTextVidas = TextSprite("LIFES: " + str(GameData.inst().getVidasJugador()), 20, "assets/fonts/ROBO.ttf",
                                     (0xFF, 0xFF, 0xFF))
        self.mTextVidas.setXY(GameConstants.inst().SCREEN_WIDTH - 150, 5)

        self.mTextReady = TextSprite("READY BOSS: ", 20, "assets/fonts/ROBO.ttf", (0xFF, 0x00, 0x00))
        self.mTextReady.setXY((GameConstants.inst().SCREEN_WIDTH / 2) - (self.mTextReady.getWidth() / 2),
                              (GameConstants.inst().SCREEN_HEIGHT / 2) - (self.mTextReady.getHeight() / 2))

        self.tiempomax = 60

        self.boss = Boss(1368,768)
        self.boss.setXY(1368 - self.boss.getWidth(), 768 / 2 - self.boss.getHeight() / 2)
        EnemyManager.inst().add(self.boss)

        pocisionX = 1100
        pocisionY = 250
        aRadio = 200


        self.miniBboss1 = MiniBoss(1368,768)
        self.miniBboss1.centerSpriteXY(pocisionX,pocisionY)
        self.miniBboss1.setAngleStart(180)
        self.miniBboss1.setRadio(aRadio)
        EnemyManager.inst().add(self.miniBboss1)

        self.miniBboss2 = MiniBoss(1368,768)
        self.miniBboss2.centerSpriteXY(pocisionX, pocisionY)
        self.miniBboss2.setAngleStart(150)
        self.miniBboss2.setRadio(aRadio)
        EnemyManager.inst().add(self.miniBboss2)

        self.miniBboss3 = MiniBoss(1368,768)
        self.miniBboss3.centerSpriteXY(pocisionX, pocisionY)
        self.miniBboss3.setAngleStart(120)
        self.miniBboss3.setRadio(aRadio)
        EnemyManager.inst().add(self.miniBboss3)






    # Actualizar los objetos del nivel.
    def update(self):
        GameState.update(self)

        # Cronometro de tiempo
        if self.mContadorTiempoSec == 60:
            self.mContadorTiempoSec = 0
            self.mContadorTiempo += 1
        elif self.mContadorTiempoSec <= 59:
            self.mContadorTiempoSec = self.contador + 1

        # cuando pasen 3 segundos empiezan a salir los enemigos
        if self.mContadorTiempo > 3:
            # si no perdi y paso mas de 3 segundos desde que empeso el lv salen los enemigos
            if not self.mPlayer.isGameOver():
                PowersUpCreator.inst().actualizarPowersUp(self.tiempomax)
            EnemyManager.inst().update()
            PowerUpManager.inst().update()

        BulletManager.inst().update()

        # Mover las estrellas
        for star in self.stars:
            star.move(star.update())

        # actualizo el jugador
        self.mPlayer.update()

        # aca si paso el tiempo minimo del nivel y no queda ningun enemigo
        if GameData.inst().bossVivo == False:
            nextState = WinGame()
            pygame.mixer.music.stop()
            Game.inst().setState(nextState)
            return

        for star2 in self.stars2:
            star2.move(star.update())

        self.mTextPuntaje.update()
        self.mTextShield.update()
        self.mTextVidas.update()

        # Mover el fondo
        if self.contador == 60:
            self.contador = 0
        elif self.contador <= 59:
            self.contador = self.contador + 1

        self.x = self.x - 1
        if self.x == -GameConstants.inst().SCREEN_WIDTH:
            self.x = 0

    # Dibujar el frame del nivel.
    def render(self):

        GameState.render(self)

        screen = Game.inst().getScreen()

        # dibujo el fondo
        screen.blit(self.fondo, (self.x, 0))
        screen.blit(self.fondo2, (self.x + GameConstants.inst().SCREEN_WIDTH, 0))

        # dibujo las estrellas
        for star in self.stars:
            star.draw(screen)

        # Dibuja las Balas antes para que salgan de atras de la nave
        BulletManager.inst().render(screen)

        # Dibujo el player
        self.mPlayer.render(screen)


        # cuando pasen 3 segundos empiezan a salir los enemigos
        if self.mContadorTiempo > 3:
            # Dibujo los enemigos
            EnemyManager.inst().render(screen)
            PowerUpManager.inst().render(screen)



        # estas son para que pasen por delante del player y de los enemigos
        for star2 in self.stars2:
            star2.draw(screen)

        self.mTextPuntaje.setText("SCORE: " + str(GameData.inst().getScore()))
        self.mTextShield.setText("SHIELD: " + str(GameData.inst().getShieldJugador()))
        self.mTextVidas.setText("LIFES: " + str(GameData.inst().getVidasJugador()))

        self.mTextPuntaje.render(screen)
        self.mTextShield.render(screen)
        self.mTextVidas.render(screen)

        if self.mContadorTiempo <= 3:
            if self.mContadorTiempoSec < 10:
                self.mTextReady.render(screen)
            elif self.mContadorTiempoSec < 20:
                pass
            elif self.mContadorTiempoSec < 30:
                self.mTextReady.render(screen)
            elif self.mContadorTiempoSec < 40:
                pass
            elif self.mContadorTiempoSec < 50:
                self.mTextReady.render(screen)
            elif self.mContadorTiempoSec < 60:
                pass

    # Destruir los objetos creados en el nivel.
    def destroy(self):
        GameState.destroy(self)

        # self.mPlayer.destroy()
        # self.mPlayer = None

        self.stars = None
        self.stars2 = None

        self.mImgSpace = None

        self.fondo = None
        self.fondo = None

        BulletManager.inst().destroy()
        EnemyManager.inst().destroy()

        self.mTextPuntaje.destroy()
        self.mTextShield.destroy()
        self.mTextVidas.destroy()

        GameData.inst().destroy()
