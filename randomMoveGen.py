import chess
import chess.svg
import chess.polyglot
import chess.syzygy
import random

def getRandMove(board):

    possibleMoves = list(board.legal_moves)

    lenPossibleMoves = len(possibleMoves)

    m = random.randrange(0, lenPossibleMoves)

    # Random Move
    # print("Random Generator's Turn: ")
    move = chess.Move.from_uci(str(possibleMoves[m]))
    board.push(move)

    return 