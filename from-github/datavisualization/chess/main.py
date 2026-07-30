from pieces import Pawn
from board import Board

# --- 1. Basic piece creation (no board) ---
print("=== Basic piece test ===")
pawn = Pawn('BLACK', 1)
print(f"Created: {pawn}")

# --- 2. Full board setup ---
print("\n=== Initial board ===")
board = Board()
board.print_board()

# --- 3. Move BLACK Pawn 1 forward ---
print("\n=== BLACK Pawn 1 moves forward ===")
black_pawn = board.find_piece('-', 1, 'BLACK')[0][1]
black_pawn.move()

# --- 4. Move WHITE Pawn 1 forward (moves toward lower rows) ---
print("\n=== WHITE Pawn 1 moves forward ===")
white_pawn = board.find_piece('-', 1, 'WHITE')[0][1]
white_pawn.move()

# --- 5. Move BLACK Knight 1 ---
print("\n=== BLACK Knight 1 moves ForwardLeft ===")
black_knight = board.find_piece('N', 1, 'BLACK')[0][1]
black_knight.move('ForwardLeft')

# --- 6. Replay saved states via generator ---
print("\n=== Replaying saved board states ===")
for i, state in enumerate(Board.load_board_states()):
    pieces_on_board = sum(1 for v in state.values() if v is not None)
    print(f"State {i + 1}: {pieces_on_board} pieces on board")
