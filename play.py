from OthelloGame import OthelloGame
from Player import RandomBOT, Human

borad_size = 10
    
def play():
    g = OthelloGame(borad_size)
    p1 = RandomBOT(game = g)
    p2 = Human(game=g)
    g.play(p1, p1) #修改玩家

def main():
    play()


if __name__ == '__main__':
    main()
