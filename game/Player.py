# -*- coding: utf-8 -*-


from api.AnimatedSprite import *
from pygame import *
from api.Keyboard import *
from api.BulletManager import *
from game.Bullet import *
from api.GameConstants import *
from api.EnemyManager import *
from api.PowerUpManager import *
from api.AudioManager import *
from game.GameData import *


class Player(AnimatedSprite):
    # Máquina de estados.
    NORMAL = 0
    DYING = 1
    EXPLODING = 2
    START = 3
    SHIELD = 4
    GAME_OVER = 5

    # Tiempos que duran los estados.
    TIME_DYING = 30
    TIME_EXPLODING = 30
    TIME_START = 60
    TIME_SHIELD = 2

    def __init__(self,aSCREEN_WIDTH,aSCREEN_HEIGHT,aType):

        Sprite.__init__(self)

        self.SCREEN_WIDTH = aSCREEN_WIDTH
        self.SCREEN_HEIGHT = aSCREEN_HEIGHT

        #tamaño de la nave
        ancho = 150
        alto = 120

        if(aType == 1):
            GameData.inst().setVidasJugador(3)
            GameData.inst().setShieldJugador(100)
        elif (aType == 2):
            GameData.inst().setVidasJugador(3)
            GameData.inst().setShieldJugador(100)
        elif (aType == 3):
            GameData.inst().setVidasJugador(3)
            GameData.inst().setShieldJugador(100)


        self.type = aType

        # Crear el sonido de disparo.
        self.soundShoot = pygame.mixer.Sound("assets/sounds/player_shoot.wav")
        # Sonido de hit (cuando le pegan).
        self.soundHit = pygame.mixer.Sound("assets/sounds/player_hit.wav")
        # Sonido de explosión.
        self.soundExplosion = pygame.mixer.Sound("assets/sounds/player_explosion.wav")

        name = None
        if self.type == 1:
            #Imagen Nave1
            name  = "assets/images/spaceships/Nave1/nave1_"
            ancho,alto = 150,100
        elif self.type == 2:
            name = "assets/images/spaceships/Nave2/nave2_"
            ancho, alto = 150, 80
        elif self.type == 3:
            name = "assets/images/spaceships/Nave3/nave3_"
            ancho, alto = 150, 80

        self.mFrames = []
        i = 0
        while (i <= 2):
            tmpImg = pygame.image.load(name + str(i) + ".png")
            #aca controlar el tamaño de las imagenes
            tmpImg = pygame.transform.scale(tmpImg, (ancho, alto)).convert_alpha()
            self.mFrames.append(tmpImg)
            i = i + 1

        self.mEscudo = pygame.image.load("assets/images/spaceships/Naves-Shield.png").convert_alpha()
        self.mEscudo = pygame.transform.scale(self.mEscudo, (200, 130)).convert_alpha()

        # Cargar la secuencia de imágenes de la explosion.
        self.mFramesExplosion = []
        i = 1
        while (i <= 7):
            tmpImg = pygame.image.load("assets/images/explosion/Frame" + str(i) + ".png")
            tmpImg = pygame.transform.flip(tmpImg, True, False)
            tmpImg = pygame.transform.scale(tmpImg, (90, 50)).convert_alpha()
            self.mFramesExplosion.append(tmpImg)
            i = i + 1

        #tamaño de las naves
        self.mWidth = self.mFrames[0].get_width()
        self.mHeight = self.mFrames[0].get_height()

        # Estado inicial.
        self.mState = Player.NORMAL
        self.setState(Player.NORMAL)

    def update(self):
        if self.getState() == Player.NORMAL:
            enemy = EnemyManager.inst().collides(self)
            if enemy != None:
                if GameData.inst().getShieldJugador() >= 1:
                    # si colisione contra algo y tengo escudo lo muestro
                    escudo = GameData.inst().getShieldJugador()
                    GameData.inst().setShieldJugador(escudo - 10)
                    self.setState(Player.SHIELD)
                    enemy.hit(5)
                else:
                    self.setState(Player.DYING)
                return


            #reviso coliciones con powersUp
            powerUp = PowerUpManager.inst().collides(self)
            if powerUp != None:
                if powerUp.isStateNormal():
                    # Agregar el score al jugador que corresponda.
                    GameData.inst().addScore(powerUp.getScore())
                    powerUp.hit(10)
            self.move()
        elif self.getState() == Player.SHIELD:
            if (self.mTimeState > Player.TIME_SHIELD):
                self.setState(Player.NORMAL)
                return
            self.move()
        elif self.getState() == Player.DYING:
            if (self.mTimeState > Player.TIME_DYING):
                self.setState(Player.EXPLODING)
                return
        elif self.getState() == Player.EXPLODING:
            #isEnded es si termino la animacion de la explocion en este caso
            if self.isEnded():
                if GameData.inst().getVidasJugador() == 0:
                    self.setState(Player.GAME_OVER)
                else:
                    GameData.inst().addLives(-1)
                    GameData.inst().setShieldJugador(100)
                    self.setState(Player.START)
                    GameData.inst().setTipoBala(1)
                return
        elif self.getState() == Player.START:
            if (self.mTimeState > Player.TIME_START):
                self.setState(Player.NORMAL)
                return
            self.move()
        elif self.getState() == Player.GAME_OVER:
            return

        AnimatedSprite.update(self, self.mWidth, self.mHeight)

    def move(self):
        if (not Keyboard.inst().leftPressed() and not Keyboard.inst().rightPressed() and not Keyboard.inst().upPressed() and not Keyboard.inst().downPressed()):
            self.gotoAndStop(0, self.mWidth, self.mHeight)
            self.setVelX(0)
            self.setVelY(0)
        else:
            if Keyboard.inst().leftPressed():
                self.setVelX(-8)
            if Keyboard.inst().rightPressed():
                self.setVelX(8)
            if Keyboard.inst().upPressed():
                self.gotoAndStop(1, self.mWidth, self.mHeight)
                self.setVelY(-8)
            if Keyboard.inst().downPressed():
                self.gotoAndStop(2, self.mWidth, self.mHeight)
                self.setVelY(8)

        # controlo los bordes de pantalla para la nave
        # borde izquierdo
        if self.getX() < 0:
             self.setX(0)
        # borde derecho
        if self.getX() > self.SCREEN_WIDTH - self.getWidth():
             self.setX(self.SCREEN_WIDTH - self.getWidth())
        # borde arriba
        if self.getY() < 0:
             self.setY(0)
        # borde abajo
        if self.getY() > self.SCREEN_HEIGHT - self.getHeight():
             self.setY(self.SCREEN_HEIGHT - self.getHeight())

        if Keyboard.inst().fire():
            self.shoot()

    def render(self, aScreen):

        if self.getState() == Player.GAME_OVER:
            return
        if self.getState() == Player.SHIELD:
            #AnimatedSprite.render(self.mEscudo, aScreen)
            aScreen.blit(self.mEscudo, (self.getX()-30,self.getY()-20))
        elif self.getState() == Player.DYING:
            if self.getTimeState() % 2 == 0:
                self.setVisible(True)
            else:
                self.setVisible(False)
        elif self.getState() == Player.START:
            if self.getTimeState() % 6 == 0:
                self.setVisible(True)
            else:
                self.setVisible(False)
        AnimatedSprite.render(self, aScreen)

    def shoot(self):
        tipoBala = GameData.inst().getTipoBala()

        if tipoBala == 2:
            #BALA 1
            # setear el tipo de bala
            self.soundShoot.play()
            b = Bullet(tipoBala)
            b.setXY(self.getX() + 30, self.getY() + 24)
            b.setVelX(20)
            b.setVelY(0)
            b.setBounds(0, 0, GameConstants.inst().SCREEN_WIDTH, GameConstants.inst().SCREEN_HEIGHT)
            b.setBoundAction(GameObject.DIE)
            BulletManager.inst().addBullet(b)
            AudioManager.inst().play(self.soundShoot)
            self.soundShoot.play()

            #BALA 2
            # setear el tipo de bala
            self.soundShoot.play()
            b = Bullet(tipoBala)
            b.setXY(self.getX() + 30, self.getY() + 24)
            b.setVelX(20)
            b.setVelY(3)
            b.setBounds(0, 0, GameConstants.inst().SCREEN_WIDTH, GameConstants.inst().SCREEN_HEIGHT)
            b.setBoundAction(GameObject.DIE)
            BulletManager.inst().addBullet(b)
            AudioManager.inst().play(self.soundShoot)
            self.soundShoot.play()

            #BALA 3
            # setear el tipo de bala
            self.soundShoot.play()
            b = Bullet(tipoBala)
            b.setXY(self.getX() + 30, self.getY() + 24)
            b.setVelX(20)
            b.setVelY(-3)
            b.setBounds(0, 0, GameConstants.inst().SCREEN_WIDTH, GameConstants.inst().SCREEN_HEIGHT)
            b.setBoundAction(GameObject.DIE)
            BulletManager.inst().addBullet(b)
            AudioManager.inst().play(self.soundShoot)
            self.soundShoot.play()

        elif tipoBala == 5:
            #Bala 1
            # setear el tipo de bala
            self.soundShoot.play()
            b = Bullet(tipoBala)
            b.setXY(self.getX() + 30, self.getY() + 24)
            b.setVelX(20)
            b.setVelY(0)
            b.setBounds(0, 0, GameConstants.inst().SCREEN_WIDTH, GameConstants.inst().SCREEN_HEIGHT)
            b.setBoundAction(GameObject.DIE)
            BulletManager.inst().addBullet(b)
            AudioManager.inst().play(self.soundShoot)
            self.soundShoot.play()
            #Bala 2
            # setear el tipo de bala
            self.soundShoot.play()
            b = Bullet(tipoBala)
            b.setXY(self.getX() + 30, self.getY() + 24)
            b.setVelX(-20)
            b.setVelY(0)
            b.setBounds(0, 0, GameConstants.inst().SCREEN_WIDTH, GameConstants.inst().SCREEN_HEIGHT)
            b.setBoundAction(GameObject.DIE)
            BulletManager.inst().addBullet(b)
            AudioManager.inst().play(self.soundShoot)
            self.soundShoot.play()

        elif tipoBala == 3:
            # setear el tipo de bala
            self.soundShoot.play()
            b = Bullet(tipoBala)
            b.setXY(self.getX() + 30, self.getY() + 18)
            b.setVelX(20)
            b.setVelY(0)
            b.setBounds(0, 0, GameConstants.inst().SCREEN_WIDTH, GameConstants.inst().SCREEN_HEIGHT)
            b.setBoundAction(GameObject.DIE)
            BulletManager.inst().addBullet(b)
            AudioManager.inst().play(self.soundShoot)
            self.soundShoot.play()

            self.soundShoot.play()
            b = Bullet(tipoBala)
            b.setXY(self.getX() + 30, self.getY() + 30)
            b.setVelX(20)
            b.setVelY(0)
            b.setBounds(0, 0, GameConstants.inst().SCREEN_WIDTH, GameConstants.inst().SCREEN_HEIGHT)
            b.setBoundAction(GameObject.DIE)
            BulletManager.inst().addBullet(b)
            AudioManager.inst().play(self.soundShoot)
            self.soundShoot.play()

        else:
            # setear el tipo de bala
            self.soundShoot.play()
            b = Bullet(tipoBala)
            b.setXY(self.getX() + 30, self.getY() + 24)
            b.setVelX(20)
            b.setVelY(0)
            b.setBounds(0, 0, GameConstants.inst().SCREEN_WIDTH, GameConstants.inst().SCREEN_HEIGHT)
            b.setBoundAction(GameObject.DIE)
            BulletManager.inst().addBullet(b)
            AudioManager.inst().play(self.soundShoot)
            self.soundShoot.play()




    # Establece el estado actual e inicializa las variables correspondientes
    # al estado.
    def setState(self, aState):
        AnimatedSprite.setState(self, aState)
        self.setVisible(True)

        #Cuando lo alcanza una bala y tiene escudo
        if self.getState() == Player.SHIELD:
            self.initAnimation(self.mFrames, 0, 2, False, self.mWidth, self.mHeight)
            self.gotoAndStop(0, self.mWidth, self.mHeight)
        elif (self.getState() == Player.DYING):
            self.stopMove()
            self.initAnimation(self.mFrames, 0, 2, False, self.mWidth, self.mHeight)
            self.soundHit.play()
            self.gotoAndStop(0, self.mWidth, self.mHeight)
        elif self.getState() == Player.START:
            self.initAnimation(self.mFrames, 0, 2, False, self.mWidth, self.mHeight)
            self.gotoAndStop(0, self.mWidth, self.mHeight)
        elif self.getState() == Player.EXPLODING:
            self.initAnimation(self.mFramesExplosion, 0, 2, False, self.mWidth, self.mHeight)
            self.soundExplosion.play()
        elif self.getState() == Player.NORMAL:
            self.initAnimation(self.mFrames, 0, 2, False, self.mWidth, self.mHeight)
            self.gotoAndStop(0, self.mWidth, self.mHeight)
        elif self.getState() == Player.GAME_OVER:
            self.setVisible(False)

    def setResolution(self, aSCREEN_WIDTH, aSCREEN_HEIGHT):
        self.SCREEN_WIDTH = aSCREEN_WIDTH
        self.SCREEN_HEIGHT = aSCREEN_HEIGHT

    def isGameOver(self):
        return self.mState == Player.GAME_OVER

    def destroy(self):

        AnimatedSprite.destroy(self)

        self.mEscudo = None

        i = len(self.mFrames)
        while i > 0:
            self.mFrames[i - 1] = None
            self.mFrames.pop(i - 1)
            i = i - 1

        i = len(self.mFramesExplosion)
        while i > 0:
            self.mFramesExplosion[i - 1] = None
        self.mFramesExplosion.pop(i - 1)
        i = i - 1