from GameUtil import *

class OthelloGame():
    def __init__(self, board_size):
        self.board_size=board_size
        self.current_player=BLACK   #黑棋先手
        self.board = [[0 for _ in range(self.board_size)] for _ in range(self.board_size)]

        #設置棋盤中心初始狀態
        self.board[board_size//2][board_size//2]=WHITE
        self.board[board_size//2-1][board_size//2-1]=WHITE
        self.board[board_size//2-1][board_size//2]=BLACK
        self.board[board_size//2][board_size//2-1]=BLACK

        self.result = {0: 'Tie!', -1: "BLACK", 1: "WHITE"}

    def move(self, position):
        if isValidMove(self.board, position, self.current_player):
            make_move(self.board, position, self.current_player)
            self.current_player=-self.current_player
            showBoard(self.board, self.current_player)
        else:
            raise Exception('invalid move')

    def play(self, black, white, verbose=True):
        showBoard(self.board, self.current_player)
        while GetWinner(self.board) == None:
            print(f"Currenr player: {self.result[self.current_player]}")
            if len(getValidMoves(self.board, self.current_player))==0:
                if verbose:
                    print('no valid move, next player')
                self.current_player=-self.current_player
                continue
            if self.current_player==WHITE:
                position=white.getAction(self.board, self.current_player)
            else:
                position=black.getAction(self.board, self.current_player)
            try:
                self.move(position)
            except:
                if verbose:
                    print('invalid move', end='\n\n')
                continue

        if verbose:
            print('Result', end='\n\n')
            showBoard(self.board, self.current_player)
            print()
            winner = GetWinner(self.board)
            print(f"winner: {self.result[winner]}")
        return winner