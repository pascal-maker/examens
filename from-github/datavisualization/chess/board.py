import json
from pieces import Rook, Knight, Bishop, Queen, King, Pawn


class Board:
    def __init__(self):
        # Dict comprehension: all 64 squares initialised to None
        self.squares = {
            f"{chr(col)}{row}": None
            for col in range(ord('a'), ord('i'))
            for row in range(1, 9)
        }
        self.setup_board()

        # Give every piece its starting position and a reference to this board
        for square, piece in self.squares.items():
            if piece is not None:
                piece.set_initial_position(square)
                piece.define_board(self)

    def setup_board(self):
        # --- BLACK major pieces on row 1 ---
        self.squares['a1'] = Rook('BLACK', 1)
        self.squares['b1'] = Knight('BLACK', 1)
        self.squares['c1'] = Bishop('BLACK', 1)
        self.squares['d1'] = Queen('BLACK', 1)
        self.squares['e1'] = King('BLACK', 1)
        self.squares['f1'] = Bishop('BLACK', 2)
        self.squares['g1'] = Knight('BLACK', 2)
        self.squares['h1'] = Rook('BLACK', 2)

        # Black pawns on row 2 — dict comprehension
        black_pawns = {
            f"{chr(col)}2": Pawn('BLACK', col - ord('a') + 1)
            for col in range(ord('a'), ord('i'))
        }
        self.squares.update(black_pawns)

        # --- WHITE major pieces on row 8 ---
        self.squares['a8'] = Rook('WHITE', 1)
        self.squares['b8'] = Knight('WHITE', 1)
        self.squares['c8'] = Bishop('WHITE', 1)
        self.squares['d8'] = Queen('WHITE', 1)
        self.squares['e8'] = King('WHITE', 1)
        self.squares['f8'] = Bishop('WHITE', 2)
        self.squares['g8'] = Knight('WHITE', 2)
        self.squares['h8'] = Rook('WHITE', 2)

        # White pawns on row 7 — dict comprehension
        white_pawns = {
            f"{chr(col)}7": Pawn('WHITE', col - ord('a') + 1)
            for col in range(ord('a'), ord('i'))
        }
        self.squares.update(white_pawns)

    def print_board(self):
        """Print the board row by row using list comprehensions."""
        rows = [
            [self.squares[f"{chr(col)}{row}"] for col in range(ord('a'), ord('i'))]
            for row in range(1, 9)
        ]
        for row in rows:
            print(row)

    def find_piece(self, symbol: str, identifier: int, color: str):
        """Return all (square, piece) pairs matching the given symbol, identifier and color."""
        return [
            (square, piece)
            for square, piece in self.squares.items()
            if piece is not None
            and piece.symbol == symbol
            and piece.identifier == identifier
            and piece.color == color
        ]

    def get_piece(self, square: str):
        """Return the piece on a specific square."""
        return self.squares[square]

    def is_square_empty(self, square: str) -> bool:
        """Return True if the square is empty."""
        return self.get_piece(square) is None

    def kill_piece(self, square: str):
        """Call die() on the piece at the given square and clear the square."""
        piece = self.squares[square]
        if piece is not None:
            piece.die()
            self.squares[square] = None

    def save_board_state(self):
        """Append the current board state as a JSON line to board.txt."""
        with open('board.txt', 'a') as file:
            file.write(json.dumps(self.squares) + '\n')

    @staticmethod
    def load_board_states():
        """Generator that yields one saved board state at a time from board.txt."""
        with open('board.txt', 'r') as file:
            for line in file:
                line = line.strip()
                if line:
                    yield json.loads(line)
