# board_renderer.py

from manim import *
import chess
from puzzle_config import puzzle_data
import os

SQUARE_SIZE = 1
BOARD_ORIGIN = LEFT * 3.5 + DOWN * 3.5

LIGHT_COLOR = "#f0d9b5"
DARK_COLOR = "#b58863"

FONT_SIZE = 42
LABEL_FONT_SIZE = 24

PIECE_DIR = "assets/pieces/png"
PIECE_SUFFIX = ".png"

class ChessPuzzleScene(Scene):
    def construct(self):
        board = chess.Board(puzzle_data["initial_fen"])
        move_list = puzzle_data["solution_moves"]

        squares = self.create_board()
        self.add_coordinates()
        pieces = self.draw_pieces(board, squares)

        title = Text("Lichess Puzzle Solution", font_size=36).to_edge(UP)
        self.play(FadeIn(title))
        self.wait(1)

        for move_san in move_list:
            move = board.parse_san(move_san)
            from_sq = move.from_square
            to_sq = move.to_square

            piece = pieces.pop(from_sq)
            target_piece = pieces.get(to_sq)

            animations = [piece.animate.move_to(squares[to_sq])]

            if target_piece:
                animations.append(FadeOut(target_piece))
                pieces.pop(to_sq)

            self.play(*animations, run_time=1.5)
            pieces[to_sq] = piece
            board.push(move)
            self.wait(0.5)

        self.wait(1)

    def create_board(self):
        squares = {}
        for rank in range(8):
            for file in range(8):
                color = LIGHT_COLOR if (rank + file) % 2 == 0 else DARK_COLOR
                square = Square(side_length=SQUARE_SIZE, fill_color=color, fill_opacity=1)
                pos = BOARD_ORIGIN + RIGHT * file + UP * rank
                square.move_to(pos)
                self.add(square)
                index = chess.square(file, rank)
                squares[index] = pos
        return squares

    def draw_pieces(self, board, squares):
        pieces = {}
        for square in chess.SQUARES:
            piece = board.piece_at(square)
            if piece:
                color_prefix = 'w' if piece.color == chess.WHITE else 'b'
                piece_char = piece.symbol().upper()
                img_path = os.path.join(PIECE_DIR, f"{color_prefix}{piece_char}.png")

                if not os.path.isfile(img_path):
                    print(f"⚠️ Missing PNG for {piece.symbol()} at {img_path}")
                    continue

                img = ImageMobject(img_path)
                # Scale to fit inside the square (slightly smaller than the square)
                target_height = SQUARE_SIZE * 0.9  # 90% of square size
                img_height = img.height
                scale_factor = target_height / img_height
                img.scale(scale_factor)

                img.move_to(squares[square])
                self.add(img)
                pieces[square] = img
        return pieces


    def add_coordinates(self):
        files = "abcdefgh"
        ranks = "12345678"

        for i in range(8):
            # File (a-h)
            label = Text(files[i], font_size=LABEL_FONT_SIZE)
            label.move_to(BOARD_ORIGIN + RIGHT * i + DOWN * 0.6)
            self.add(label)

            # Rank (1-8)
            label = Text(ranks[i], font_size=LABEL_FONT_SIZE)
            label.move_to(BOARD_ORIGIN + LEFT * 0.6 + UP * i)
            self.add(label)

class PuzzleTeaserScene(Scene):
    def construct(self):
        board = chess.Board(puzzle_data["initial_fen"])
        squares = self.create_board()
        self.add_coordinates()
        self.draw_pieces(board, squares)

        self.wait(15)

    def create_board(self):
        squares = {}
        for rank in range(8):
            for file in range(8):
                color = LIGHT_COLOR if (rank + file) % 2 == 0 else DARK_COLOR
                square = Square(side_length=SQUARE_SIZE, fill_color=color, fill_opacity=1)
                pos = BOARD_ORIGIN + RIGHT * file + UP * rank
                square.move_to(pos)
                self.add(square)
                index = chess.square(file, rank)
                squares[index] = pos
        return squares
    
    def draw_pieces(self, board, squares):
        pieces = {}
        for square in chess.SQUARES:
            piece = board.piece_at(square)
            if piece:
                color_prefix = 'w' if piece.color == chess.WHITE else 'b'
                piece_char = piece.symbol().upper()
                img_path = os.path.join(PIECE_DIR, f"{color_prefix}{piece_char}.png")

                if not os.path.isfile(img_path):
                    print(f"⚠️ Missing PNG for {piece.symbol()} at {img_path}")
                    continue

                img = ImageMobject(img_path)
                # Scale to fit inside the square (slightly smaller than the square)
                target_height = SQUARE_SIZE * 0.9  # 90% of square size
                img_height = img.height
                scale_factor = target_height / img_height
                img.scale(scale_factor)

                img.move_to(squares[square])
                self.add(img)
                pieces[square] = img
        return pieces


    def add_coordinates(self):
        files = "abcdefgh"
        ranks = "12345678"

        for i in range(8):
            # File (a-h)
            label = Text(files[i], font_size=LABEL_FONT_SIZE)
            label.move_to(BOARD_ORIGIN + RIGHT * i + DOWN * 0.6)
            self.add(label)

            # Rank (1-8)
            label = Text(ranks[i], font_size=LABEL_FONT_SIZE)
            label.move_to(BOARD_ORIGIN + LEFT * 0.6 + UP * i)
            self.add(label)
