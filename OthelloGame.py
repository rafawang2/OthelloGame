from ANSI import ANSI_string

BLACK = -1
WHITE = 1

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
        
    def getValidMoves(self, color):  #獲取指定顏色的所有有效走法
        moves = set()  #有效的走法位置
        for y, row in enumerate(self.board):    #y: 0~self.board_size-1, row:  self.board[y]
            for x, cell in enumerate(row):      #x: 0~self.board_size-1, cell: self.board[y][x]
                if cell == color:  #如果當前格子是玩家的棋子
                    #遍歷8個方向
                    for direction in [(1, 1), (1, 0), (1, -1), (0, -1), (-1, -1), (-1, 0), (-1, 1), (0, 1)]:
                        flips = []  #要翻轉的棋子
                        
                        for size in range(1, self.board_size):  #探索從當前格子出發的每一個方向
                            ydir = y + direction[1] * size  #計算新的縱向座標
                            xdir = x + direction[0] * size  #計算新的橫向座標
                            
                            #檢查新的座標是否在棋盤範圍內
                            if xdir >= 0 and xdir < self.board_size and ydir >= 0 and ydir < self.board_size:
                                if self.board[ydir][xdir] == -color:  #如果是對方的棋子
                                    flips.append((ydir, xdir))  #需要翻轉
                                elif self.board[ydir][xdir] == 0:  #如果是空格
                                    if len(flips) != 0:  #如果有棋子需要翻轉
                                        moves.add((ydir, xdir))  #則當前位置是有效的走法
                                    break  #不能再繼續擴展，跳出循環
                                else:  #如果是自己顏色的棋子，不能再繼續，跳出循環
                                    break
                            else:  #如果超出了棋盤範圍，跳出循環
                                break
        return list(moves)  #返回有效走法的位置列表
    

    def isValidMove(self, position):
        valids = self.getValidMoves(self.current_player)
        if position in valids:
            return True
        else:
            return False

    def executeMove(self, position):
        y, x = position
        self.board[y][x] = self.current_player  #直接落子

        #遍歷所有方向
        for direction in [(1, 1), (1, 0), (1, -1), (0, -1), (-1, -1), (-1, 0), (-1, 1), (0, 1)]:
            flips = []
            valid_route = False  #用來標記是否找到有效的翻轉路徑

            # 從當前位置開始，沿著方向逐步搜尋，最大範圍為棋盤大小
            for size in range(1, self.board_size):
                ydir = y + direction[1] * size  # 計算新的縱向座標
                xdir = x + direction[0] * size  # 計算新的橫向座標

                #檢查是否超出棋盤範圍
                if xdir >= 0 and xdir < self.board_size and ydir >= 0 and ydir < self.board_size:
                    if self.board[ydir][xdir] == -self.current_player:  # 如果發現對方的棋子
                        flips.append((ydir, xdir))  # 將其加入翻轉列表
                    elif self.board[ydir][xdir] == self.current_player:  # 如果發現自己的棋子
                        if len(flips) > 0:  # 如果有對方棋子被翻轉，則標記為有效路徑
                            valid_route = True
                        break  # 條路徑結束，無需再繼續
                    else:  #如果發現空格，這條路徑無效，結束該方向的搜尋
                        break
                else:  #如果超出棋盤邊界，這條路徑無效，結束搜尋
                    break
            
            #如果該方向上存在有效的翻轉路徑
            if valid_route:
                #翻轉
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
            print(f"Currenr player: {self.result[self.current_player]}")
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
                self.move(position)
            except:
                if verbose:
                    print('invalid move', end='\n\n')
                continue
        
        if verbose:
            print('Result', end='\n\n')
            self.showBoard()
            print()
            print(f"winner: {self.result[self.isEndGame()]}")
        return self.isEndGame()
    
    def showBoard(self):
        #定義角落偏移，用於棋盤置中顯示
        corner_offset_format = '{:^' + str(len(str(self.board_size)) + 1) + '}'
        print(corner_offset_format.format(''), end='')  #空角落
        
        #列用字母代替
        for i in range(self.board_size):
            alpha_col = ANSI_string(s = '{:^2}'.format(chr(ord('A') + i)), bold=True)
            print(alpha_col, end='')
        print()
        
        #行數和棋盤內容
        for i in range(self.board_size):
            num_row = ANSI_string(s = corner_offset_format.format(i + 1), bold=True)
            print(num_row, end='')  #行數
            for j in range(self.board_size):
                if self.isValidMove((i, j)):    #有效: 綠方格
                    valid_block = ANSI_string(s = '{:^2}'.format('■'),color='green')
                    print(valid_block, end='')  # 有效移動位置用特殊符號∎表示
                else:
                    if self.board[i][j] == BLACK:   #黑子: 黃點代替
                        black_block = ANSI_string(s='{:^2}'.format('●'),color='yellow')
                        print(black_block, end='')
                    elif self.board[i][j] == WHITE: #白子: 藍點代替
                        white_block = ANSI_string(s='{:^2}'.format('●'),color='blue')
                        print(white_block, end='')
                    else:   #空格: 空心方格
                        blank_block = ANSI_string(s = '{:^2}'.format('□'))
                        print(blank_block, end='')
            print(num_row, end='')  #行數
            print()
        print(corner_offset_format.format(''), end='')  #空角落
        for i in range(self.board_size):
            alpha_col = ANSI_string(s = '{:^2}'.format(chr(ord('A') + i)), bold=True)
            print(alpha_col, end='')
        print()  # 換行
        print(" " + "="*((self.board_size+1)*2+1) + " ")
