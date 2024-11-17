import numpy as np
from OthelloUtil import getValidMoves, executeMove, isValidMove
from ANSI import ANSI_string

class OthelloGame(np.ndarray):
    BLACK = -1
    WHITE = 1
    
    def __new__(cls, board_size):
        return super().__new__(cls, shape=(board_size,board_size), dtype='int')
    
    def __init__(self, board_size):
        self.board_size=board_size
        self.current_player=OthelloGame.BLACK
        self[np.where(self!=0)]=0
        self[int(board_size/2)][int(board_size/2)]=OthelloGame.WHITE
        self[int(board_size/2)-1][int(board_size/2)-1]=OthelloGame.WHITE
        self[int(board_size/2)-1][int(board_size/2)]=OthelloGame.BLACK
        self[int(board_size/2)][int(board_size/2)-1]=OthelloGame.BLACK
        
    def move(self, position):
        if isValidMove(self, self.current_player, position):
            executeMove(self, self.current_player, position)
            self.current_player=-self.current_player
            self.showBoard()
        else:
            raise Exception('invalid move')
    
    def isEndGame(self):
        white_valid_moves=len(getValidMoves(self, OthelloGame.WHITE))
        black_valid_moves=len(getValidMoves(self, OthelloGame.BLACK))
        if white_valid_moves==0 and black_valid_moves==0:
            v,c=np.unique(self, return_counts=True)
            white_count=c[np.where(v==OthelloGame.WHITE)]
            black_count=c[np.where(v==OthelloGame.BLACK)]
            if len(white_count) == 0:
                white_count = np.array([0])
            if len(black_count) == 0:
                black_count = np.array([0])
            if white_count>black_count:
                return OthelloGame.WHITE
            elif black_count>white_count:
                return OthelloGame.BLACK
            else:
                return 0
        else:
            return None
    
    def play(self, black, white, verbose=True):
        self.showBoard()
        while self.isEndGame() == None:
            if len(getValidMoves(self, self.current_player))==0:
                if verbose:
                    print('no valid move, next player')
                self.current_player=-self.current_player
                continue
            if self.current_player==OthelloGame.WHITE:
                position=white.getAction(self.current_player)
            else:
                position=black.getAction(self.current_player)
            try:
                self.move(position)
            except:
                if verbose:
                    print('invalid move', end='\n\n')
                continue
        
        if verbose:
            print('---------- Result ----------', end='\n\n')
            self.showBoard()
            print()
            print('Winner:', self.isEndGame())
        return self.isEndGame()
    
    def showBoard(self):
        # 定義角落偏移格式，用於棋盤坐標的居中顯示
        corner_offset_format = '{:^' + str(len(str(self.board_size)) + 1) + '}'
        
        # 打印列名
        print(corner_offset_format.format(''), end='')  # 打印空的角落
        for i in range(self.board_size):
            alpha_col = ANSI_string(s = '{:^2}'.format(chr(ord('A') + i)), bold=True)
            print(alpha_col, end='')  # 打印字母標籤（A、B、C...）
        print()  # 換行
        
        # 打印行數和棋盤內容
        for i in range(self.board_size):
            num_row = ANSI_string(s = corner_offset_format.format(i + 1), bold=True)
            print(num_row, end='')  # 打印行數
            for j in range(self.board_size):
                # 判斷是否是有效移動位置，如果是，用特殊符號∎表示，否則用棋盤內容表示
                if isValidMove(self, self.current_player, (i, j)):
                    valid_block = ANSI_string(s = '{:^2}'.format('■'),color='green')
                    print(valid_block, end='')  # 有效移動位置用特殊符號∎表示
                else:
                    if self[i][j] == 1:
                        black_block = ANSI_string(s='{:^2}'.format('●'),color='yellow')
                        print(black_block, end='')  # 棋盤內容-黑棋
                    elif self[i][j] == -1:
                        white_block = ANSI_string(s='{:^2}'.format('●'),color='blue')
                        print(white_block, end='')  # 棋盤內容-白棋
                    else:
                        blank_block = ANSI_string(s = '{:^2}'.format('□'))
                        print(blank_block, end='')  # 棋盤內容
            print(num_row, end='')  # 打印行數
            print()  # 換行
        print(corner_offset_format.format(''), end='')  # 打印空的角落
        for i in range(self.board_size):
            alpha_col = ANSI_string(s = '{:^2}'.format(chr(ord('A') + i)), bold=True)
            print(alpha_col, end='')  # 打印字母標籤（A、B、C...）
        print()  # 換行
    
    
    def clone(self):
        new=self.copy()
        new.board_size=self.board_size
        new.current_player=self.current_player
        return new
    
