from ANSI import ANSI_string

BLACK = -1
WHITE = 1

class OthelloGame():
    def __init__(self, board_size):
        self.board_size=board_size
        self.current_player=BLACK
        self.board = [[0 for _ in range(self.board_size)] for _ in range(self.board_size)]
        self.board[board_size//2][board_size//2]=WHITE
        self.board[board_size//2-1][board_size//2-1]=WHITE
        self.board[board_size//2-1][board_size//2]=BLACK
        self.board[board_size//2][board_size//2-1]=BLACK
        
    def getValidMoves(self, color): #get valid moves of color
        moves = set()
        for y, row in enumerate(self.board):
            for x, cell in enumerate(row):
                if cell == color:
                    for direction in [(1,1),(1,0),(1,-1),(0,-1),(-1,-1),(-1,0),(-1,1),(0,1)]:
                        flips = []
                        for size in range(1, self.board_size):
                            ydir = y + direction[1] * size
                            xdir = x + direction[0] * size
                            if xdir >= 0 and xdir < self.board_size and ydir >= 0 and ydir < self.board_size:
                                if self.board[ydir][xdir]==-color:
                                    flips.append((ydir, xdir))
                                elif self.board[ydir][xdir]==0:
                                    if len(flips)!=0:
                                        moves.add((ydir, xdir))
                                    break
                                else:
                                    break
                            else:
                                break
        return list(moves)
    

    def isValidMove(self, position):
        valids = self.getValidMoves(self.current_player)
        if position in valids:
            return True
        else:
            return False

    def executeMove(self, position):
        y, x = position
        self.board[y][x] = self.current_player
        for direction in [(1,1),(1,0),(1,-1),(0,-1),(-1,-1),(-1,0),(-1,1),(0,1)]:
            flips = []
            valid_route=False
            for size in range(1, self.board_size):
                ydir = y + direction[1] * size
                xdir = x + direction[0] * size
                if xdir >= 0 and xdir < self.board_size and ydir >= 0 and ydir < self.board_size:
                    if self.board[ydir][xdir]==-self.current_player:
                        flips.append((ydir, xdir))
                    elif self.board[ydir][xdir]==self.current_player:
                        if len(flips)>0:
                            valid_route=True
                        break
                    else:
                        break
                else:
                    break
            if valid_route:
                # self.board[tuple(zip(*flips))]=self.current_player
                for flip in flips:
                    yflip, xflip = flip
                    self.board[yflip][xflip] = self.current_player

    def move(self, position):
        if self.isValidMove(position):
            self.executeMove(position)
            self.current_player=-self.current_player
            self.showBoard()
        else:
            
            raise Exception('invalid move')
    
    def isEndGame(self):
        white_valid_moves=len(self.getValidMoves(WHITE))
        black_valid_moves=len(self.getValidMoves(BLACK))
        if white_valid_moves==0 and black_valid_moves==0:
            black_count = 0
            white_count = 0
            for row in self.board:
                for cell in row:
                    if cell == WHITE:
                        white_count+=1
                    elif cell == BLACK:
                        black_count+=1
            if white_count>black_count:
                return WHITE
            elif black_count>white_count:
                return BLACK
            else:
                return 0
        else:
            return None
    
    def play(self, black, white, verbose=True):
        self.showBoard()
        while self.isEndGame() == None:
            if len(self.getValidMoves(self.current_player))==0:
                if verbose:
                    print('no valid move, next player')
                self.current_player=-self.current_player
                continue
            if self.current_player==WHITE:
                position=white.getAction(self.current_player)
            else:
                position=black.getAction(self.current_player)
            try:
                print(f"Get: {position}")
                self.move(position)
            except:
                if verbose:
                    print('invalid move', end='\n\n')
                continue
        
        if verbose:
            print('Result', end='\n\n')
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
                if self.isValidMove((i, j)):
                    valid_block = ANSI_string(s = '{:^2}'.format('■'),color='green')
                    print(valid_block, end='')  # 有效移動位置用特殊符號∎表示
                else:
                    if self.board[i][j] == BLACK:
                        black_block = ANSI_string(s='{:^2}'.format('●'),color='yellow')
                        print(black_block, end='')  # 棋盤內容-黑棋
                    elif self.board[i][j] == WHITE:
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
        print(" " + "="*((self.board_size+1)*2+1) + " ")
