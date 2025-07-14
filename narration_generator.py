# narration_generator.py

import pyttsx3
import chess
import os

PIECE_NAMES = {
    chess.PAWN: "pawn", chess.KNIGHT: "knight", chess.BISHOP: "bishop",
    chess.ROOK: "rook", chess.QUEEN: "queen", chess.KING: "king"
}

def get_piece_name(symbol):
    piece = chess.Piece.from_symbol(symbol)
    return PIECE_NAMES.get(piece.piece_type, "piece")

def describe_move(san, board):
    try:
        move = board.parse_san(san)
        piece = board.piece_at(move.from_square)
        name = get_piece_name(piece.symbol()) if piece else "piece"
        from_sq = chess.square_name(move.from_square)
        to_sq = chess.square_name(move.to_square)

        if board.is_capture(move):
            desc = f"{name.capitalize()} captures on {to_sq}"
        else:
            desc = f"{name.capitalize()} from {from_sq} to {to_sq}"

        board.push(move)

        if board.is_checkmate():
            desc += " — checkmate"
        elif board.is_check():
            desc += " with check"

        return desc + "."

    except Exception as e:
        return f"(Invalid move: {san})"

def generate_narration(fen, san_moves, out_path="output/narration.mp3"):
    board = chess.Board(fen)
    side = "White" if board.turn == chess.WHITE else "Black"
    narration_lines = [f"{side} to move. Here's the solution."]

    for san in san_moves:
        narration_lines.append(describe_move(san, board))

    # Ensure output directory exists
    os.makedirs(os.path.dirname(out_path), exist_ok=True)

    # Save audio using pyttsx3
    try:
        engine = pyttsx3.init()
        engine.save_to_file(" ".join(narration_lines), out_path)
        engine.runAndWait()
        print(f"🔊 Narration audio saved to: {out_path}")
    except Exception as e:
        print("❌ Failed to generate narration:", e)

    return narration_lines
