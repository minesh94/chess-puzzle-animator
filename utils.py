# utils.py

import chess
import chess.pgn
from io import StringIO

def get_fen_from_pgn(pgn_text, ply_number):
    game = chess.pgn.read_game(StringIO(pgn_text))
    board = game.board()
    for i, move in enumerate(game.mainline_moves(), start=1):
        board.push(move)
        if i == ply_number:
            return board.fen()
    return board.fen()
