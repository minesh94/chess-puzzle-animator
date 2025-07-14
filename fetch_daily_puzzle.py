# fetch_daily_puzzle.py

import requests
import chess
import chess.pgn
from io import StringIO

def fetch_and_save_daily_puzzle():
    print("📥 Fetching Lichess daily puzzle...")
    res = requests.get("https://lichess.org/api/puzzle/daily")
    res.raise_for_status()
    data = res.json()

    puzzle_id = data["puzzle"]["id"]
    solution_uci = data["puzzle"]["solution"]
    themes = data["puzzle"].get("themes", [])
    pgn_text = data["game"]["pgn"]

    # ♟ Rebuild board from full PGN (ignoring initialPly)
    game = chess.pgn.read_game(StringIO(pgn_text))
    board = game.board()

    for move in game.mainline_moves():
        board.push(move)

    fen = board.fen()
    print(f"📌 Final FEN after PGN: {fen}")
    print(f"➡️ Turn to move: {'White' if board.turn else 'Black'}")

    # Validate: first UCI move must match board.turn
    first_uci = solution_uci[0]
    from_square = chess.parse_square(first_uci[:2])
    piece = board.piece_at(from_square)

    if piece is None:
        raise ValueError(f"❌ No piece at {first_uci[:2]} in FEN: {fen}")
    if piece.color != board.turn:
        raise ValueError(f"❌ First move {first_uci} is not by the player to move at FEN: {fen}")

    # 🔍 Convert UCI to SAN
    san_moves = []
    for uci in solution_uci:
        move = chess.Move.from_uci(uci)
        if move not in board.legal_moves:
            raise ValueError(f"❌ Illegal move {uci} at FEN: {board.fen()}")
        san = board.san(move)
        board.push(move)
        san_moves.append(san)

    # 💾 Save puzzle config
    with open("puzzle_config.py", "w") as f:
        f.write(f'''# Auto-generated

puzzle_data = {{
    "id": "{puzzle_id}",
    "initial_fen": "{fen}",
    "solution_moves": {san_moves},
    "themes": {themes}
}}
''')
    print("✅ Puzzle saved to puzzle_config.py")
