import chess
import chess.svg
import chess.polyglot
import chess.syzygy
from stockfish import Stockfish
import math

def getPieceValueHeuristic(piece, i):
    if piece == None:
        return 0
    
    pawnValues = [0,  0,  0,  0,  0,  0,  0,  0, 
                  50, 50, 50, 50, 50, 50, 50, 50, 
                  10, 10, 20, 30, 30, 20, 10, 10,
5,  5, 10, 25, 25, 10,  5,  5,
0,  0,  0, 20, 20,  0,  0,  0,
5, -5,-10,  0,  0,-10, -5,  5,
5, 10, 10,-20,-20, 10, 10,  5,
0,  0,  0,  0,  0,  0,  0,  0]
    
    knightValues = [-50, -40, -30, -30, -30, -30, -40, -50,
-40, -20, 0, 0, 0, 0, -20, -40,
-30, 0, 10, 15, 15, 10, 0, -30,
-30, 5, 15, 20, 20, 15, 5, -30,
-30, 0, 15, 20, 20, 15, 0, -30,
-30, 5, 10, 15, 15, 10, 5, -30,
-40, -20, 0, 5, 5, 0, -20, -40,
-50, -40, -30, -30, -30, -30, -40, -50]
    
    bishopValues = [-20, -10, -10, -10, -10, -10, -10, -20,
-10, 0, 0, 0, 0, 0, 0, -10,
-10, 0, 5, 10, 10, 5, 0, -10,
-10, 5, 5, 10, 10, 5, 5, -10,
-10, 0, 10, 10, 10, 10, 0, -10,
-10, 10, 10, 10, 10, 10, 10, -10,
-10, 5, 0, 0, 0, 0, 5, -10,
-20, -10, -10, -10, -10, -10, -10, -20]
    
    rookValues = [0,  0,  0,  0,  0,  0,  0,  0,
  5, 10, 10, 10, 10, 10, 10,  5,
 -5,  0,  0,  0,  0,  0,  0, -5,
 -5,  0,  0,  0,  0,  0,  0, -5,
 -5,  0,  0,  0,  0,  0,  0, -5,
 -5,  0,  0,  0,  0,  0,  0, -5,
 -5,  0,  0,  0,  0,  0,  0, -5,
  0,  0,  0,  5,  5,  0,  0,  0]
    
    queenValues = [-20, -10, -10, -5, -5, -10, -10, -20,
-10, 0, 0, 0, 0, 0, 0, -10,
-10, 0, 5, 5, 5, 5, 0, -10,
-5, 0, 5, 5, 5, 5, 0, -5,
0, 0, 5, 5, 5, 5, 0, -5,
-10, 5, 5, 5, 5, 5, 0, -10,
-10, 0, 5, 0, 0, 0, 0, -10,
-20, -10, -10, -5, -5, -10, -10, -20]
    
    kingMiddleValues = [-30, -40, -40, -50, -50, -40, -40, -30,
-30, -40, -40, -50, -50, -40, -40, -30,
-30, -40, -40, -50, -50, -40, -40, -30,
-30, -40, -40, -50, -50, -40, -40, -30,
-20, -30, -30, -40, -40, -30, -30, -20,
-10, -20, -20, -20, -20, -20, -20, -10,
 20, 20, 0, 0, 0, 0, 20, 20,
 20, 30, 10, 0, 0, 10, 30, 20]
    value = 0

    if piece.casefold() == "p":
        value = pawnValues[i] + 100
    elif piece.casefold() == "n":
        value = knightValues[i] + 320
    elif piece.casefold() == "b":
        value = bishopValues[i] + 330
    elif piece.casefold() == "r":
        value = rookValues[i] + 500
    elif piece.casefold() == "q":
        value = queenValues[i] + 900
    elif piece.casefold() == "k":
        value = kingMiddleValues[i] + 20000
    
    return value 
    
def evaluationHeuristic(board):
    i = 0
    evaluation = 0
    x = True
    
    while i < 63:
        try:
            x = bool(board.piece_at(i).color)
        except AttributeError as e:
            x = x
        evaluation = evaluation + (getPieceValueHeuristic(str(board.piece_at(i)), 63 - i) if x else -getPieceValueHeuristic(str(board.piece_at(i)), i))
        i += 1

    if board.is_game_over():
        if board.outcome().winner == chess.WHITE:
            evaluation += 1000000
        elif board.outcome().winner == chess.BLACK:
            evaluation -= 1000000
        else:
            evaluation = 0
    return evaluation

def getPieceValue(piece):
    if piece == None:
        return 0
    value = 0
    if piece.casefold() == "p":
        value = 10
    elif piece.casefold() == "n":
        value = 30
    elif piece.casefold() == "b":
        value = 30
    elif piece.casefold() == "r":
        value = 50
    elif piece.casefold() == "q":
        value = 90
    elif piece.casefold() == "k":
        value = 900
    return value 

def evaluation(board):
    i = 0
    evaluation = 0
    x = True
    
    while i < 63:
        try:
            x = bool(board.piece_at(i).color)
        except AttributeError as e:
            x = x
        evaluation = evaluation + (getPieceValue(str(board.piece_at(i))) if x else -getPieceValue(str(board.piece_at(i))))
        i += 1

    if board.is_game_over():
        if board.outcome().winner == chess.WHITE:
            evaluation += 10000
        elif board.outcome().winner == chess.BLACK:
            evaluation -= 10000
        else:
            evaluation = 0

    return evaluation

def minimax(depth, board, alpha, beta, isMaximizing, M):
    
    if (depth == 0):
        return evaluationHeuristic(board) 
    
    possibleMoves = board.legal_moves

    if (isMaximizing):
        bestMove = float("-inf")
        for m in possibleMoves:
            move = chess.Move.from_uci(str(m))  
            newDepth = depth
            # if (board.is_capture(move)):
            #     newDepth = depth + 1
            
            board.push(move)

            if (board.fen() in M):
                result = board.fen()
                board.pop()
                return M.get(result)
            
            bestMove = max(bestMove, minimax(newDepth - 1, board, alpha, beta, not isMaximizing, M))

            alpha = max(alpha, bestMove)

            M[board.fen()] = bestMove
            board.pop()

            if beta <= alpha:
                return bestMove
            
        return bestMove
    else:
        bestMove = float("inf")
        for m in possibleMoves:
            move = chess.Move.from_uci(str(m))
            newDepth = depth
            if (board.is_capture(move)):
                newDepth = depth + 2

            board.push(move)

            if (board.fen() in M):
                result = board.fen()
                board.pop()
                return M.get(result)
            
            bestMove = min(bestMove, minimax(newDepth - 1, board, alpha, beta, not isMaximizing, M))

            beta = min(beta, bestMove)

            M[board.fen()] = bestMove
            
            board.pop()

            if (beta <= alpha):
                return bestMove
            
        return bestMove
    
def endgame(board, possibleMoves):
        
    with chess.syzygy.open_tablebase("syzygyTables") as tablebase:
        valuePos = -1
        positiveMove = None
        valueNeg = 1
        negativeMove = None
        zeroMove = None
        move = None
        for m in possibleMoves:
            move = chess.Move.from_uci(str(m))
            board.push(move)
            value = tablebase.probe_dtz(board)
            board.pop()
            if value == 0:
                zeroMove = move

            elif value > 0:
               if value > valuePos:
                    positiveMove = move
                    valuePos = value
            else:
                if value > valueNeg:
                    negativeMove = move
                    valueNeg = move

    if negativeMove:
        return negativeMove
    elif zeroMove:
        return zeroMove
    else:
        return positiveMove                

def minimaxRoot(board, isMaximizing):

    M = {}
    
    possibleMoves = board.legal_moves

    pieceDict = board.piece_map()

    with chess.polyglot.open_reader("polyglotBook/Book.bin") as reader:   
        try:
           print("move: ", reader.weighted_choice(board).move)
           return reader.weighted_choice(board).move
        except IndexError:
            pass
    
    if (len(pieceDict) <= 5):
        return endgame(board, possibleMoves)
    
    depth = 2
    # depth = int(15 / math.log(len(pieceDict), 2))
    # print("depth: ", depth)

    bestMove = float('-inf')
    bestMoveFinal = None
    
    for m in possibleMoves:
        
        move = chess.Move.from_uci(str(m))
        
        newDepth = depth
        if (board.is_capture(move)):
            newDepth += 2

        board.push(move)

        if (board.fen() in M):
            return M.get(board.fen())
        
        value = minimax(newDepth - 1, board, -float("inf"), float("inf"), not isMaximizing, M)
        

        if (value >= bestMove):
            bestMove = value
            bestMoveFinal = move

        M[board.fen()] = bestMove

        # unmake the last move 
        board.pop()
    return bestMoveFinal

def main():
    stockfish = Stockfish(depth=1, parameters={"UCI_LimitStrength": True, "UCI_Elo": 100})
    stockfish.set_elo_rating(100)
    board = chess.Board()
    n = 0
    print(board)

    while n < 1000:

        if board.is_game_over():
            print(board.outcome())
            return 

        if n % 2 == 0:
            # Alpha-Beta Pruning
            print("White's Turn: ")
            move = minimaxRoot(board, True)
            move = chess.Move.from_uci(str(move))
            board.push(move)
            stockfish.make_moves_from_current_position([move])
        else:
            # Stockfish 
            print("Black's Turn: ")
            move = stockfish.get_best_move()
            move = chess.Move.from_uci(str(move))
            board.push(move)
            stockfish.make_moves_from_current_position([move])
        print(board)
        chess.svg.board(board)
        n += 1
    print("1000 move limit exceeded")
    return 

if __name__ == "__main__":
    main() 