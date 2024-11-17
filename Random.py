import random

class BOT():
    def __init__(self, game):
        self.game = game

    def getAction(self, color):
        valids=self.game.getValidMoves(color)
        position=random.choice(valids)
        return position
