import random
from GameUtil import *

class RandomBOT():
    def getAction(self, board, color):
        valids=getValidMoves(board, color)
        position=random.choice(valids)
        return position

class Human():
    def regularize_pos(self, pos):
        return (pos[0]+1, chr(pos[1] + ord('A')))

    def parse_input(self, user_input: str, board_size):
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
        if not (0 <= row < board_size and 0 <= col < board_size):
            return
        
        return (row, col)
    
    def getAction(self, board, color):
        self.valids = getValidMoves(board, color)
        s = "Valid Moves: " + ", ".join(map(str, [self.regularize_pos(move) for move in self.valids]))
        print(s)
        remind_str = "Enter your move using a letter for the column and a number for the row.\n" + "For example: 'B 1' or '1 B'. Please enter your move: "
        while True:
            user_input = str(input(remind_str))
            pos = self.parse_input(user_input=user_input, board_size=len(board))
            if pos in self.valids:
                return pos
            else:
                print(self.valids)
                remind_str = "Invalid move! Please try again: "