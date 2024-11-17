import numpy as np
from OthelloUtil import getValidMoves

class BOT():
    def __init__(self, game):
        self.game = game

    def getAction(self, color):
        valids=getValidMoves(self.game, color)
        position=np.random.choice(range(len(valids)), size=1)[0]
        position=valids[position]
        return position
