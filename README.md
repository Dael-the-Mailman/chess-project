# Chess Engine + AI Project

> Author: Kaleb Ugalde

The goal of this project is to create a chess engine and an accompanying AI to go alone with it. I wanted to explore the minimax algorithm and the monte carlo tree search algorithm in this project as well. Inspiration for this project was seeing AlphaZero and having previous chess experience as a child.

## Libraries Used

- Numpy
- Pygame

## Chess Engine

This includes all the inner workings such as the board representation, legality checking, special rule considerations, etc.

### Board Representation

The chess board is represented by a 2D numpy array whose format is as follows:

- First character (b or w) represents the color (black or white) of the piece
- The second character represents the type of piece it is
  - K is king
  - Q is queen
  - R is rook
  - B is bishop
  - N is knight
  - p is pawn
- The string "--" represents an empty space on the board

```
self.board = np.array([
    ["bR", "bN", "bB", "bQ", "bK", "bB", "bN", "bR"],
    ["bp", "bp", "bp", "bp", "bp", "bp", "bp", "bp"],
    ["--", "--", "--", "--", "--", "--", "--", "--"],
    ["--", "--", "--", "--", "--", "--", "--", "--"],
    ["--", "--", "--", "--", "--", "--", "--", "--"],
    ["--", "--", "--", "--", "--", "--", "--", "--"],
    ["wp", "wp", "wp", "wp", "wp", "wp", "wp", "wp"],
    ["wR", "wN", "wB", "wQ", "wK", "wB", "wN", "wR"]
])
```

> Starting position of a chess board

### Miscellaneous

- Turn tracker to tell whose move it is
- Move log to show the history of moves made

## Minimax Algorithm

## Monte Carlo Tree Search
