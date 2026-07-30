from abc import ABC
import functools


def print_board(func):
    @functools.wraps(func)
    def wrapper(self, *args, **kwargs):
        result = func(self, *args, **kwargs)
        if self.board is not None:
            self.board.print_board()
        return result
    return wrapper


def save_board(func):
    @functools.wraps(func)
    def wrapper(self, *args, **kwargs):
        result = func(self, *args, **kwargs)
        if self.board is not None:
            self.board.save_board_state()
        return result
    return wrapper


class BaseChessPiece(ABC, dict):
    def __init__(self, color: str, name: str, symbol: str, identifier: int):
        self.color = color
        self.name = name
        self.symbol = symbol
        self.identifier = identifier
        self.position = 'None'
        self.is_alive = True
        self.board = None
        dict.__init__(self, color=color, name=name, symbol=symbol,
                      identifier=identifier, position='None', is_alive=True)

    @print_board
    @save_board
    def move(self, movement: str):
        """Execute the move on the board. Called by subclasses via super().move(movement)."""
        if self.board is None:
            print(movement)
            return

        if movement == self.position:
            print("Movement blocked: out of bounds or invalid move")
            return

        new_location = self.board.get_piece(movement)

        if new_location is not None:
            if new_location.color == self.color:
                print(f"Cannot move to {movement}: occupied by a friendly piece")
                return
            self.board.kill_piece(movement)

        self.board.squares[self.position] = None
        self.position = movement
        self['position'] = movement
        self.board.squares[self.position] = self
        print(f"{self} moved to {movement}")

    def die(self):
        self.is_alive = False
        self['is_alive'] = False

    def set_initial_position(self, position: str):
        self.position = position
        self['position'] = position

    def define_board(self, board):
        self.board = board

    def __str__(self):
        return f"{self.color} {self.name} {self.identifier}"

    def __repr__(self):
        return f"{self.color} {self.name} {self.identifier}"


class Pawn(BaseChessPiece):
    def __init__(self, color: str, identifier: int):
        super().__init__(color, 'Pawn', '-', identifier)

    def move(self):
        from board_movements import BoardMovements
        movement = BoardMovements.forward(self.position, self.color, 1)
        super().move(movement)


class Rook(BaseChessPiece):
    def __init__(self, color: str, identifier: int):
        super().__init__(color, 'Rook', 'R', identifier)

    def move(self, direction: str = 'Forward', squares: int = 1):
        from board_movements import BoardMovements
        directions = {
            'Forward':  BoardMovements.forward,
            'Backward': BoardMovements.backward,
            'Left':     BoardMovements.left,
            'Right':    BoardMovements.right,
        }
        if direction in directions:
            movement = directions[direction](self.position, self.color, squares)
            super().move(movement)
        else:
            print(f"Invalid direction for Rook: {direction}")


class Bishop(BaseChessPiece):
    def __init__(self, color: str, identifier: int):
        super().__init__(color, 'Bishop', 'B', identifier)

    def move(self, direction: str = 'ForwardRight', squares: int = 1):
        from board_movements import BoardMovements
        directions = {
            'ForwardLeft':   BoardMovements.forward_left,
            'ForwardRight':  BoardMovements.forward_right,
            'BackwardLeft':  BoardMovements.backward_left,
            'BackwardRight': BoardMovements.backward_right,
        }
        if direction in directions:
            movement = directions[direction](self.position, self.color, squares)
            super().move(movement)
        else:
            print(f"Invalid direction for Bishop: {direction}")


class Knight(BaseChessPiece):
    def __init__(self, color: str, identifier: int):
        super().__init__(color, 'Knight', 'N', identifier)

    def move(self, direction: str = 'ForwardLeft'):
        col_idx = ord(self.position[0]) - ord('a')
        row = int(self.position[1])

        # L-shaped moves: (col_offset, row_offset)
        knight_moves = {
            'ForwardLeft':   (col_idx - 1, row + 2),
            'ForwardRight':  (col_idx + 1, row + 2),
            'BackwardLeft':  (col_idx - 1, row - 2),
            'BackwardRight': (col_idx + 1, row - 2),
            'LeftForward':   (col_idx - 2, row + 1),
            'LeftBackward':  (col_idx - 2, row - 1),
            'RightForward':  (col_idx + 2, row + 1),
            'RightBackward': (col_idx + 2, row - 1),
        }

        if direction not in knight_moves:
            print(f"Invalid direction for Knight: {direction}")
            return

        new_col_idx, new_row = knight_moves[direction]
        if new_col_idx < 0 or new_col_idx > 7 or new_row < 1 or new_row > 8:
            print("Knight movement blocked: out of bounds")
            return

        movement = f"{chr(ord('a') + new_col_idx)}{new_row}"
        super().move(movement)


class Queen(BaseChessPiece):
    def __init__(self, color: str, identifier: int):
        super().__init__(color, 'Queen', 'Q', identifier)

    def move(self, direction: str = 'Forward', squares: int = 1):
        from board_movements import BoardMovements
        directions = {
            'Forward':       BoardMovements.forward,
            'Backward':      BoardMovements.backward,
            'Left':          BoardMovements.left,
            'Right':         BoardMovements.right,
            'ForwardLeft':   BoardMovements.forward_left,
            'ForwardRight':  BoardMovements.forward_right,
            'BackwardLeft':  BoardMovements.backward_left,
            'BackwardRight': BoardMovements.backward_right,
        }
        if direction in directions:
            movement = directions[direction](self.position, self.color, squares)
            super().move(movement)
        else:
            print(f"Invalid direction for Queen: {direction}")


class King(BaseChessPiece):
    def __init__(self, color: str, identifier: int):
        super().__init__(color, 'King', 'K', identifier)

    def move(self, direction: str = 'Forward'):
        from board_movements import BoardMovements
        directions = {
            'Forward':       BoardMovements.forward,
            'Backward':      BoardMovements.backward,
            'Left':          BoardMovements.left,
            'Right':         BoardMovements.right,
            'ForwardLeft':   BoardMovements.forward_left,
            'ForwardRight':  BoardMovements.forward_right,
            'BackwardLeft':  BoardMovements.backward_left,
            'BackwardRight': BoardMovements.backward_right,
        }
        if direction in directions:
            # King always moves exactly 1 square
            movement = directions[direction](self.position, self.color, 1)
            super().move(movement)
        else:
            print(f"Invalid direction for King: {direction}")
