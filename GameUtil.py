BLACK = -1
WHITE = 1

def ANSI_string(s="", color=None, background=None, bold=False):
        colors = {
            'black': '\033[30m',
            'red': '\033[31m',
            'green': '\033[32m',
            'yellow': '\033[33m',
            'blue': '\033[34m',
            'magenta': '\033[35m',
            'cyan': '\033[36m',
            'white': '\033[37m',
            'reset': '\033[0m'
        }

        background_colors = {
            'black': '\033[40m',
            'red': '\033[41m',
            'green': '\033[42m',
            'yellow': '\033[43m',
            'blue': '\033[44m',
            'magenta': '\033[45m',
            'cyan': '\033[46m',
            'white': '\033[47m',
            'reset': '\033[0m',
            'gray': '\033[100m',  # 新增的灰色背景
            'light_gray': '\033[47m'  # 新增的淺灰色背景
        }

        styles = {
            'bold': '\033[1m',
            'reset': '\033[0m'
        }
        color_code = colors[color] if color in colors else ''
        background_code = background_colors[background] if background in colors else ''
        bold_code = styles['bold'] if bold else ''

        return f"{color_code}{background_code}{bold_code}{s}{styles['reset']}"

def getValidMoves(board, color):  #獲取指定顏色的所有有效走法
    moves = set()  #有效的走法位置
    board_size = len(board)
    for y, row in enumerate(board):    #y: 0~board_size-1, row:  board[y]
        for x, cell in enumerate(row):      #x: 0~board_size-1, cell: board[y][x]
            if cell == color:  #如果當前格子是玩家的棋子
                #遍歷8個方向
                for direction in [(1, 1), (1, 0), (1, -1), (0, -1), (-1, -1), (-1, 0), (-1, 1), (0, 1)]:
                    flips = []  #要翻轉的棋子

                    for size in range(1, board_size):  #探索從當前格子出發的每一個方向
                        ydir = y + direction[1] * size  #計算新的縱向座標
                        xdir = x + direction[0] * size  #計算新的橫向座標

                        #檢查新的座標是否在棋盤範圍內
                        if xdir >= 0 and xdir < board_size and ydir >= 0 and ydir < board_size:
                            if board[ydir][xdir] == -color:  #如果是對方的棋子
                                flips.append((ydir, xdir))  #需要翻轉
                            elif board[ydir][xdir] == 0:  #如果是空格
                                if len(flips) != 0:  #如果有棋子需要翻轉
                                    moves.add((ydir, xdir))  #則當前位置是有效的走法
                                break  #不能再繼續擴展，跳出循環
                            else:  #如果是自己顏色的棋子，不能再繼續，跳出循環
                                break
                        else:  #如果超出了棋盤範圍，跳出循環
                            break
    return list(moves)  #返回有效走法的位置列表

def isValidMove(board, position, color):
    valids = getValidMoves(board, color)
    if position in valids:
        return True
    else:
        return False

def make_move(board, position, color):
    y, x = position
    board_size = len(board)
    board[y][x] = color  #直接落子

    #遍歷所有方向
    for direction in [(1, 1), (1, 0), (1, -1), (0, -1), (-1, -1), (-1, 0), (-1, 1), (0, 1)]:
        flips = []
        valid_route = False  #用來標記是否找到有效的翻轉路徑

        # 從當前位置開始，沿著方向逐步搜尋，最大範圍為棋盤大小
        for size in range(1, board_size):
            ydir = y + direction[1] * size  # 計算新的縱向座標
            xdir = x + direction[0] * size  # 計算新的橫向座標

            #檢查是否超出棋盤範圍
            if xdir >= 0 and xdir < board_size and ydir >= 0 and ydir < board_size:
                if board[ydir][xdir] == -color:  # 如果發現對方的棋子
                    flips.append((ydir, xdir))  # 將其加入翻轉列表
                elif board[ydir][xdir] == color:  # 如果發現自己的棋子
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
                board[yflip][xflip] = color

def GetWinner(board):
    white_valid_moves=len(getValidMoves(board, WHITE))
    black_valid_moves=len(getValidMoves(board, BLACK))
    if white_valid_moves==0 and black_valid_moves==0:
        black_count = 0
        white_count = 0
        for row in board:
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

def showBoard(board, color):
    board_size = len(board)
    #定義角落偏移，用於棋盤置中顯示
    corner_offset_format = '{:^' + str(len(str(board_size)) + 1) + '}'
    print(corner_offset_format.format(''), end='')  #空角落

    #列用字母代替
    for i in range(board_size):
        alpha_col = ANSI_string(s = '{:^2}'.format(chr(ord('A') + i)), bold=True)
        print(alpha_col, end='')
    print()

    #行數和棋盤內容
    for i in range(board_size):
        num_row = ANSI_string(s = corner_offset_format.format(i + 1), bold=True)
        print(num_row, end='')  #行數
        for j in range(board_size):
            if isValidMove(board, (i, j), color):    #有效: 綠方格
                valid_block = ANSI_string(s = '{:^2}'.format('■'),color='green')
                print(valid_block, end='')  # 有效移動位置用特殊符號∎表示
            else:
                if board[i][j] == BLACK:   #黑子: 黃點代替
                    black_block = ANSI_string(s='{:^2}'.format('●'),color='yellow')
                    print(black_block, end='')
                elif board[i][j] == WHITE: #白子: 藍點代替
                    white_block = ANSI_string(s='{:^2}'.format('●'),color='blue')
                    print(white_block, end='')
                else:   #空格: 空心方格
                    blank_block = ANSI_string(s = '{:^2}'.format('□'))
                    print(blank_block, end='')
        print(num_row, end='')  #行數
        print()
    print(corner_offset_format.format(''), end='')  #空角落
    for i in range(board_size):
        alpha_col = ANSI_string(s = '{:^2}'.format(chr(ord('A') + i)), bold=True)
        print(alpha_col, end='')
    print()  # 換行
    print(" " + "="*((board_size+1)*2+1) + " ")
















    