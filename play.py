from OthelloGame import OthelloGame
from OthelloUtil import getValidMoves, isValidMove
from Random import BOT as RandomBOT

borad_size = 10

class Human():
    def __init__(self, game: OthelloGame):
        self.game = game
        self.valids = []
        
    def regularize_pos(self, pos):
        return (pos[0]+1, chr(pos[1] + ord('A')))
    
    def parse_input(self, user_input: str):
        # 移除多餘空白，並轉為大寫以統一處理
        user_input = user_input.strip().upper().split()
        if len(user_input) != 2:
            return
        # 判斷輸入格式
        if user_input[0].isalpha() and user_input[1].isdigit():
            col = ord(user_input[0]) - ord('A')  # 將字母轉換為列索引
            row = int(user_input[1]) - 1        # 將行轉為 0 基索引
        elif user_input[0].isdigit() and user_input[1].isalpha():
            row = int(user_input[0]) - 1
            col = ord(user_input[1]) - ord('A')
        else:
            return

        # 檢查行列是否有效
        if not (0 <= row < self.game.board_size and 0 <= col < self.game.board_size):
            return
        
        return (row, col)
    
    def getAction(self, color):
        self.valids=getValidMoves(self.game, color)
        s = "Valid Moves: " + ", ".join(map(str, [self.regularize_pos(move) for move in self.valids]))
        print(s)
        remind_str = "Enter your move using a letter for the column and a number for the row.\n"+"For example: 'B 1' or '1 B'. Please enter your move: "
        while True:
            user_input = str(input(remind_str))
            pos = self.parse_input(user_input=user_input)
            if pos in self.valids:
                return pos
            else:
                remind_str("Invalid move! Please try again: ")
    
def play():
    g = OthelloGame(borad_size)
    p1 = RandomBOT(game = g)
    p2 = RandomBOT(game = g)
    p3 = Human(game=g)
    result = g.play(p3, p3)
    print(result)

def main():
    play()


if __name__ == '__main__':
    main()
