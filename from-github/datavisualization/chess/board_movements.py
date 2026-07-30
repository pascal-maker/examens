class BoardMovements:
    """
    Static movement helpers for chess pieces.
    All methods return the new position string, or the original position
    if the move is blocked (out of bounds).

    Direction convention:
    - BLACK starts on rows 1-2, WHITE starts on rows 7-8.
    - 'Forward' for BLACK increments the row; for WHITE it decrements.
    - 'Left' / 'Right' are from an absolute board perspective (a←h).
    """

    @staticmethod
    def forward(position: str, color: str, squares: int = 1) -> str:
        column = position[0]
        row = int(position[1])
        new_row = row + squares if color == 'BLACK' else row - squares
        if new_row < 1 or new_row > 8:
            print("Movement blocked: out of bounds")
            return position
        return f"{column}{new_row}"

    @staticmethod
    def backward(position: str, color: str, squares: int = 1) -> str:
        column = position[0]
        row = int(position[1])
        new_row = row - squares if color == 'BLACK' else row + squares
        if new_row < 1 or new_row > 8:
            print("Movement blocked: out of bounds")
            return position
        return f"{column}{new_row}"

    @staticmethod
    def left(position: str, color: str, squares: int = 1) -> str:
        column = position[0]
        row = int(position[1])
        new_column = chr(ord(column) - squares)
        if new_column == '`' or new_column < 'a' or new_column > 'h':
            print("Movement blocked: out of bounds")
            return position
        return f"{new_column}{row}"

    @staticmethod
    def right(position: str, color: str, squares: int = 1) -> str:
        column = position[0]
        row = int(position[1])
        new_column = chr(ord(column) + squares)
        if new_column == 'i' or new_column < 'a' or new_column > 'h':
            print("Movement blocked: out of bounds")
            return position
        return f"{new_column}{row}"

    @staticmethod
    def forward_left(position: str, color: str, squares: int = 1) -> str:
        new_pos = BoardMovements.forward(position, color, squares)
        if new_pos == position:
            return position
        result = BoardMovements.left(new_pos, color, squares)
        return position if result == new_pos else result

    @staticmethod
    def forward_right(position: str, color: str, squares: int = 1) -> str:
        new_pos = BoardMovements.forward(position, color, squares)
        if new_pos == position:
            return position
        result = BoardMovements.right(new_pos, color, squares)
        return position if result == new_pos else result

    @staticmethod
    def backward_left(position: str, color: str, squares: int = 1) -> str:
        new_pos = BoardMovements.backward(position, color, squares)
        if new_pos == position:
            return position
        result = BoardMovements.left(new_pos, color, squares)
        return position if result == new_pos else result

    @staticmethod
    def backward_right(position: str, color: str, squares: int = 1) -> str:
        new_pos = BoardMovements.backward(position, color, squares)
        if new_pos == position:
            return position
        result = BoardMovements.right(new_pos, color, squares)
        return position if result == new_pos else result
