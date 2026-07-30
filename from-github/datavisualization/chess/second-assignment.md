# Chess Assignment — OOP & Git Deep Dive

## Goal of This Assignment

The goal is to build a **textual chess game** in Python that demonstrates:

1. **Object-Oriented Programming** — inheritance, abstract methods, ABCs
2. **Advanced Python syntax** — decorators (`@functools.wraps`), generators, dict/list comprehensions
3. **Static methods & class design** — `BoardMovements` as a utility class with no instance state
4. **Git branching workflow** — dedicated branches per topic (not mixing everything into main)

This assignment goes beyond the Git basics by combining OOP concepts with version control in a real project context.

---

## What Has Been Implemented

### 1. Pieces (`pieces.py`) — All 6 piece types

| Piece | Movement Logic |
|-------|----------------|
| **Pawn** | `forward()` only, 1 square (direction auto-toggled by color) |
| **Rook** | Forward / Backward / Left / Right (n squares) |
| **Bishop** | All 4 diagonals (ForwardLeft, ForwardRight, etc.) — n squares |
| **Knight** | 8 L-shaped moves with bounds checking (`col_idx - 1`, `row + 2`) |
| **Queen** | Rook directions + Bishop directions combined |
| **King** | All 8 directions, always 1 square |

Each piece inherits from `BaseChessPiece` which:
- Inherits both `ABC` (abstract base class) and `dict` (for JSON serialization)
- Defines abstract `move()` and concrete `die()` methods
- Stores shared properties: `color`, `name`, `symbol`, `identifier`, `position`, `is_alive`
- Uses `__str__` / `__repr__` for display formatting

### 2. Board (`board.py`) — Full board setup & management

- **Dict comprehension** creates all 64 squares: `{f"{chr(col)}{row}": None}`
- **`setup_board()`** uses dict comprehensions to place black pawns (row 2), white pawns (row 7), and major pieces on rows 1 and 8
- **`print_board()`** — row-first display using list comprehension nesting
- **`find_piece(symbol, identifier, color)`** — list comprehension filters all non-None squares
- **`kill_piece(square)`** — calls `die()` then clears the square
- **`save_board_state()`** — appends JSON to `board.txt` (used by `@save_board` decorator)
- **`load_board_states()`** — generator that yields one board state at a time from file

### 3. BoardMovements (`board_movements.py`) — Static movement helpers

All methods are `@staticmethods`:
- `forward(position, color, squares)` — row increment/decrement based on color
- `backward(position, color, squares)` — opposite direction
- `left` / `right` — column arithmetic with boundary checks (`'a'` to `'h'`)
- Combined diagonals: `forward_left`, `forward_right`, `backward_left`, `backward_right`

Direction convention: **BLACK** moves forward by incrementing row; **WHITE** decrements (board is flipped for each color).

### 4. Decorators (`pieces.py`) — Auto logging & state saving

- **`@print_board`** — after every move, prints the current board state
- **`@save_board`** — appends JSON to `board.txt` after every move
- Both use `@functools.wraps(func)` for proper metadata preservation

### 5. Main (`main.py`) — Demo flow

```
1. Basic piece creation (no board) → Pawn('BLACK', 1)
2. Full board setup                → Board() with all pieces
3. BLACK Pawn 1 moves forward      → a2 → a3
4. WHITE Pawn 1 moves forward      → h7 → h6
5. BLACK Knight 1 ForwardLeft       → b8 → a6
6. Replay saved states via generator → reads board.txt line by line
```

### 6. Git Branches (as documented in README.md)

| Branch | What It Contains |
|--------|-----------------|
| `main` | Fully merged working implementation |
| `feature/chess-pieces` | All 6 piece classes with movement stubs |
| `feature/board-setup` | Board class + BoardMovements static helpers |
| `feature/decorators-and-state` | Decorator system + generator state loader |

---

## What Has Changed Since Previous Session

### git-fundamentals (first assignment)

| Change | Details |
|--------|---------|
| Issue #1 created | "Documentation improvements" on GitHub |
| PR #2 merged | Squash-merged `project-structure.md` into main; feature branch deleted |
| Second-assignment.md | Written — covers merge conflicts + Git LFS topics (this file) |

### chess (second assignment)

- **No new changes** since initial creation — the project is fully implemented and committed.
- The repo has 4 commits with clean history:
  - `chore: remove __pycache__` / `.DS_Store` files
  - All previous git-fundamentals commits were synced via shared origin

---

## What's Missing (Optional Extensions from the Assignment)

| Feature | Effort | Notes |
|---------|--------|-------|
| **Pawn diagonal kills** | Small | Pawns move vertically but kill diagonally — currently they can only capture on forward squares |
| **Piece blocking** | Medium | All pieces except Knight should check if path is blocked by another piece |
| **Turn system** | Medium | Alternating white/black turns, preventing two consecutive moves by same side |
| **En passant** | Small-Medium | Special pawn capture rule after double-move |
| **Castling (rokade)** | Medium | King-side and queen-side castling rules |
| **Promotion** | Small | Pawn reaching last row becomes Queen/Rook/Bishop/Knight |
| **Check/Checkmate/Stalemate detection** | Large | Requires full move validation across all piece types |
| **Interactive input (Jupyter/IPython)** | Medium | Replace hardcoded moves in `main.py` with user input |

---

## How to Present This During Your Sketch Session

1. **Walk through the class hierarchy** — show how `BaseChessPiece(ABC, dict)` provides shared state and JSON serialization
2. **Explain why inheriting from both ABC + dict** — abstract methods for interface contract, dict mixin for serialisation into board states
3. **Demo `python main.py`** so the output shows: initial board → pawn moves → knight move → replayed states
4. **Point out where each concept is used:**
   - Dict comprehension in `board.py` lines 8–12 (squares) and 33–36 (black pawns)
   - List comprehension in `find_piece()` line 67-74
   - Generator in `load_board_states()` — yields one JSON line at a time, memory efficient
   - Decorators in `pieces.py` lines 5–22 wrapping the `move()` method
