from random import choice
from math import inf

def Gameboard(board):
    chars = {1: 'X', -1: 'O', 0: ' '}
    for row in board:
        for cell in row:
            ch = chars[cell]
            print(f'| {ch} |', end='')
        print('\n' + '---------------')
    print('===============')

def Clearboard(board):
    for x, row in enumerate(board):
        for y, col in enumerate(row):
            board[x][y] = 0

def winningPlayer(board, player, win_condition):
    board_size = len(board)
    conditions = []
    for i in range(board_size):
        conditions.append([board[i][j] for j in range(board_size)])  # rzedy
        conditions.append([board[j][i] for j in range(board_size)])  # kolumny
    conditions.append([board[i][i] for i in range(board_size)])  # glowna macierz
    conditions.append([board[i][board_size - i - 1] for i in range(board_size)])  #

    if [player] * win_condition in conditions:
        return True

    return False

def gameWon(board, win_condition):
    return winningPlayer(board, 1, win_condition) or winningPlayer(board, -1, win_condition)

def printResult(board, win_condition):
    if winningPlayer(board, 1, win_condition):
        print('X wygral!')

    elif winningPlayer(board, -1, win_condition):
        print('O\'s wygral!')

    else:
        print('Remis')

def blanks(board):
    blank = []
    for x, row in enumerate(board):
        for y, col in enumerate(row):
            if board[x][y] == 0:
                blank.append([x, y])

    return blank

def boardFull(board):
    if len(blanks(board)) == 0:
        return True
    return False

def setMove(board, x, y, player):
    board[x][y] = player

def playerMove(board):
    e = True
    moves = {}
    board_size = len(board)
    for i in range(board_size):
        for j in range(board_size):
            moves[(i * board_size) + j + 1] = [i, j]

    while e:
        try:
            move = int(input('Wpisz numer pomiedzy 1-' + str(board_size**2) + ': '))
            if move < 1 or move > board_size**2:
                print('Niepoprwany ruch! Spróbuj jeszcze raz!')
            elif not (moves[move] in blanks(board)):
                print('Niepoprwany ruch! Spróbuj jeszcze raz!')
            else:
                setMove(board, moves[move][0], moves[move][1], 1)
                Gameboard(board)
                e = False
        except(KeyError, ValueError):
            print('Wpisz cyfrę!')

def getScore(board, win_condition):
    if winningPlayer(board, 1, win_condition):
        return 10

    elif winningPlayer(board, -1, win_condition):
        return -10

    else:
        return 0

def abminimax(board, depth, alpha, beta, player, win_condition):
    row = -1
    col = -1
    if depth == 0 or gameWon(board, win_condition):
        return [row, col, getScore(board, win_condition)]

    else:
        for cell in blanks(board):
            setMove(board, cell[0], cell[1], player)
            score = abminimax(board, depth - 1, alpha, beta, -player, win_condition)
            if player == 1:
                # X is always the max player
                if score[2] > alpha:
                    alpha = score[2]
                    row = cell[0]
                    col = cell[1]

            else:
                if score[2] < beta:
                    beta = score[2]
                    row = cell[0]
                    col = cell[1]

            setMove(board, cell[0], cell[1], 0)

            if alpha >= beta:
                break

        if player == 1:
            return [row, col, alpha]

        else:
            return [row, col, beta]

def o_comp(board, win_condition):
    if len(blanks(board)) == len(board)**2:
        x = choice(range(len(board)))
        y = choice(range(len(board)))
        setMove(board, x, y, -1)
        Gameboard(board)

    else:
        result = abminimax(board, len(blanks(board)), -inf, inf, -1, win_condition)
        setMove(board, result[0], result[1], -1)
        Gameboard(board)

def x_comp(board, win_condition):
    if len(blanks(board)) == len(board)**2:
        x = choice(range(len(board)))
        y = choice(range(len(board)))
        setMove(board, x, y, 1)
        Gameboard(board)

    else:
        result = abminimax(board, len(blanks(board)), -inf, inf, 1, win_condition)
        setMove(board, result[0], result[1], 1)
        Gameboard(board)

def makeMove(board, player, mode, win_condition):
    if mode == 1:
        if player == 1:
            playerMove(board)

        else:
            o_comp(board, win_condition)
    else:
        if player == 1:
            o_comp(board, win_condition)
        else:
            x_comp(board, win_condition)

def pvc():
    while True:
        try:
            order = int(input('Wprowadz czy chcesz grać jako pierwszy(1) czy drugi(2): '))
            if not (order == 1 or order == 2):
                print('Prosze wybrac 1  lub 2')
            else:
                break
        except(KeyError, ValueError):
            print('Wpisz cyfre')

    board_size = int(input("Wpisz rozmiar tablicy do gry: "))
    win_condition = int(input("Wpisz ilość znaków w rzędzie potrzebną do wygranej: "))
    board = [[0] * board_size for _ in range(board_size)]
    depth = 3
    if order == 2:
        currentPlayer = -1
    else:
        currentPlayer = 1

    while not (boardFull(board) or gameWon(board, win_condition)):
        makeMove(board, currentPlayer, 1, win_condition)
        currentPlayer *= -1

    printResult(board, win_condition)

# Driver Code

pvc()
