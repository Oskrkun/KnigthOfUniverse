# -*- coding: utf-8 -*-

from api.Game import *
from game.states.Menu import *

# ============= Punto de entrad del programa. =============

g = Game()

initState = Menu()

g.setState(initState)

g.gameLoop()

g.destroy()