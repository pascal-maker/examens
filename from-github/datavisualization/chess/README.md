# Chess — OOP & Git Assignment

A textual chess game built in Python to explore Object-Oriented Programming, Git branching, and advanced Python features.

## Repository

[chess](https://github.com/pascal-maker/chess)

## Project Structure

```
chess/
├── main.py              # Entry point — run this to start the demo
├── pieces.py            # BaseChessPiece (ABC + dict) and all 6 piece types
├── board.py             # Board class with setup, printing, and state saving
└── board_movements.py   # BoardMovements static helpers for all 8 directions
```

## Concepts Demonstrated

| Concept | Where |
|---------|-------|
| Inheritance & ABC | `BaseChessPiece` → `Pawn`, `Rook`, `Bishop`, `Knight`, `Queen`, `King` |
| Abstract methods | `move()` pattern in `BaseChessPiece` |
| Decorators | `@print_board`, `@save_board` in `pieces.py` |
| Dict comprehension | Board squares init + pawn placement in `board.py` |
| List comprehension | `print_board()` row builder, `find_piece()` in `board.py` |
| Generator | `Board.load_board_states()` — reads `board.txt` one line at a time |
| Static methods | All movement helpers in `BoardMovements` |
| `dict` inheritance | `BaseChessPiece(ABC, dict)` — enables JSON serialisation of pieces |

## Branch Workflow

| Branch | Description |
|--------|-------------|
| `main` | Fully merged, working implementation |
| `feature/chess-pieces` | All 6 piece classes with movement logic |
| `feature/board-setup` | `Board` class + `BoardMovements` |
| `feature/decorators-and-state` | `@print_board`, `@save_board` decorators + generator state loader |

## How to Run

```bash
cd chess
python main.py
```

## Board Layout

```
[BLACK Rook 1, BLACK Knight 1, BLACK Bishop 1, BLACK Queen 1, BLACK King 1, BLACK Bishop 2, BLACK Knight 2, BLACK Rook 2]
[BLACK Pawn 1, BLACK Pawn 2, BLACK Pawn 3, BLACK Pawn 4, BLACK Pawn 5, BLACK Pawn 6, BLACK Pawn 7, BLACK Pawn 8]
[None, None, None, None, None, None, None, None]
[None, None, None, None, None, None, None, None]
[None, None, None, None, None, None, None, None]
[None, None, None, None, None, None, None, None]
[WHITE Pawn 1, WHITE Pawn 2, WHITE Pawn 3, WHITE Pawn 4, WHITE Pawn 5, WHITE Pawn 6, WHITE Pawn 7, WHITE Pawn 8]
[WHITE Rook 1, WHITE Knight 1, WHITE Bishop 1, WHITE Queen 1, WHITE King 1, WHITE Bishop 2, WHITE Knight 2, WHITE Rook 2]
```

BLACK occupies rows 1–2, WHITE occupies rows 7–8. Forward for each colour moves toward the opponent.

## Movement Directions

| Piece | Valid directions |
|-------|----------------|
| Pawn | `forward` only (1 square) |
| Rook | `Forward`, `Backward`, `Left`, `Right` (n squares) |
| Bishop | `ForwardLeft`, `ForwardRight`, `BackwardLeft`, `BackwardRight` (n squares) |
| Knight | `ForwardLeft`, `ForwardRight`, `BackwardLeft`, `BackwardRight`, `LeftForward`, `LeftBackward`, `RightForward`, `RightBackward` |
| Queen | All 8 directions (n squares) |
| King | All 8 directions (1 square) |
