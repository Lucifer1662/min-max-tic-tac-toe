import sys
import operator



def print_board(board):
    print("--------------")
    print("|",board[(0,0)], " ", board[(1,0)], " ", board[(2,0)], "|")
    print("|",board[(0,1)], " ", board[(1,1)], " ", board[(2,1)], "|")
    print("|",board[(0,2)], " ", board[(1,2)], " ", board[(2,2)], "|")
    print("--------------")
        

def create_board():
    board = {}
    for x in range(3):
        for y in range(3):
            board[(x,y)] = ' '
    return board


def combo3Winner(lst: list):
    for elm in lst:
        if(elm == ' '):
            return (False, ' ')
    first = lst[0]
    for elm in lst:
        if(elm != first):
            return (False, ' ')
    
    return (True, first)

def isWinnerHorizontal(board: dict, row: int):
    lst = []
    for i in range(3):
        lst.append(board[(i, row)])
    return combo3Winner(lst)

def isWinnerVertical(board: dict, col: int):
    lst = []
    for i in range(3):
        lst.append(board[(col, i)])
    return combo3Winner(lst)

def isWinnerDiagonalLeft(board):
    lst = [board[(0,0)], board[(1,1)], board[(2,2)]]
    return combo3Winner(lst)

def isWinnerDiagonalRight(board):
    lst = [board[(2,0)], board[(1,1)], board[(0,2)]]
    return combo3Winner(lst)

def isWinner(board:dict):
    for row in range(3):
        (success, winner) = isWinnerHorizontal(board, row)
        if(success):
            return (success, winner)

    for col in range(3):
        (success, winner) = isWinnerVertical(board, col)
        if(success):
            return (success, winner)
    
    (success, winner) = isWinnerDiagonalLeft(board)
    if(success):
        return (success, winner)

    (success, winner) = isWinnerDiagonalRight(board)
    if(success):
        return (success, winner)

    return (False, ' ')


def playerMove(board, token):
    while(True):
        position_str = input("Token position")
        x = int(position_str[1])
        y = int(position_str[3])
        position = (x,y)
        print(position)
        if(board[position] == ' '):
            return position
        print("There is a token there.")
    

def possibleMoves(board, token):
    moves = []
    for pos in board:
        if(board[pos] == ' '):
            b = board.copy()
            b[pos] = token
            moves.append((pos, b))
    return moves

def AIMoveMinMaxEval(board, myToken, enemyToken, evalMe, evalOp, sign, depth):
    #print_board(board)
    (success, winner) = isWinner(board)
    if(success):
        return (sign*(1/depth), None, board.copy())
        

    moves = possibleMoves(board, myToken)
    bestRes = None
    bestResBoard = board.copy()
    bestMove = None
    for (move, b) in moves:
        (res, _, resBoard)  = AIMoveMinMaxEval(b, enemyToken, myToken, evalOp, evalMe, -sign, depth+1)
        if(bestRes == None or not evalMe(bestRes, res)):
            bestRes = res
            bestResBoard = resBoard.copy()
            bestMove = move

    if(bestRes == None):
        bestRes = 0
    return (bestRes, bestMove, bestResBoard)



def AIMoveMinMax(board, token):
    enemyToken = 'o'
    if(token == 'o'):
        enemyToken = 'x'
    (res, move, resBoard) = AIMoveMinMaxEval(board, token, enemyToken, operator.gt, operator.lt, -1, 1)
    print(res)
    return move

def AIMoveMinMaxAlphaBetaPruning(board, token):
    pass

def main():
    board = create_board()
    currentTurn = 'o'

    # board[(0,0)] = 'x'
    # board[(2,1)] = 'o'
    # board[(0,1)] = 'x'
    # board[(2,2)] = 'x'
    # board[(0,2)] = 'o'
    # board[(1,2)] = 'o'

    makeMoveO = AIMoveMinMax
    makeMoveX = AIMoveMinMax

    while(True):
        print_board(board)
        (isGameOver, winner) = isWinner(board)
        if(isGameOver):
            break

        if(currentTurn == 'o'):
            position = makeMoveO(board, currentTurn)
        else:
            position = makeMoveX(board, currentTurn)

        if(position == None):
            break
        board[position] = currentTurn

        if(currentTurn == 'o'):
            currentTurn = 'x'
        else:
            currentTurn = 'o'
        
    
    print(winner)
    print_board(board)

    pass



if __name__ == '__main__':
    main()