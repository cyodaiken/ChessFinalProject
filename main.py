import chess
import chess.svg
from stockfish import Stockfish

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

def minimax(depth, board, alpha, beta, isMaximizing):
    if (depth == 0):
        return evaluation(board) 
    
    possibleMoves = board.legal_moves

    if (isMaximizing):
        bestMove = -float("inf")
        for m in possibleMoves:
            move = chess.Move.from_uci(str(m))
            board.push(move)
            bestMove = max(bestMove, minimax(depth - 1, board, alpha, beta, not isMaximizing))
            board.pop()
            alpha = max(alpha, bestMove)
            if beta <= alpha:
                return bestMove
        return bestMove
    else:
        bestMove = float("inf")
        for m in possibleMoves:
            move = chess.Move.from_uci(str(m))
            board.push(move)
            bestMove = min(bestMove, minimax(depth - 1, board, alpha, beta, not isMaximizing))
            board.pop()
            beta = min(beta, bestMove)
            if (beta <= alpha):
                return bestMove
        return bestMove

def minimaxRoot(depth, board, isMaximizing):
    possibleMoves = board.legal_moves

    bestMove = float('-inf')
    bestMoveFinal = None
    
    for m in possibleMoves:
        move = chess.Move.from_uci(str(m))
        board.push(move)
        value = max(bestMove, minimax(depth - 1, board, -float("inf"), float("inf"), not isMaximizing))
        # print("value: ", value)
        # unmake the last move 
        board.pop()
        if (value >= bestMove):
            # print("Best score: ", str(bestMove))
            # print("Best move: ", str(bestMoveFinal))
            bestMove = value
            bestMoveFinal = move

    return bestMoveFinal

def main():
    stockfish = Stockfish(depth=1, parameters={"Skill Level": 1})
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
            move = minimaxRoot(3, board, True)
            # if move == None:
            #     print("Game Over")
            #     return 
            move = chess.Move.from_uci(str(move))
            board.push(move)
            stockfish.make_moves_from_current_position([move])
        else:
            # Stockfish 
            print("Black's Turn: ")
            # move = stockfish.get_best_move()
            moves = list(board.generate_legal_moves())
            # if move == None:
            #     return "Game Over"
            move = chess.Move.from_uci(str(moves[0]))
            board.push(move)
            stockfish.make_moves_from_current_position([move])
        print(board)
        chess.svg.board(board)
        n += 1
    print("100 move limit exceeded")
    return 

if __name__ == "__main__":
    main() 