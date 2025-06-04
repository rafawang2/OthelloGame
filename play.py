from OthelloGame import OthelloGame
from Players.Player import RandomBOT, Human

borad_size = 8

def play():
    g = OthelloGame(borad_size)
    p1 = RandomBOT()
    p2 = Human()
    g.play(p2, p1) #修改玩家

def main():
    play()


if __name__ == '__main__':
    main()
