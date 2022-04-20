import numpy as np


class GameState():
    def __init__(self):
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
        self.moveFunctions = {"p": self.getPawnMoves, "R": self.getRookMoves, "N": self.getKnightMoves,
                              "B": self.getBishopMoves, "Q": self.getBishopMoves, "K": self.getKingMoves}
        self.whiteToMove = True
        self.moveHistory = []

    def makeMove(self, move):
        self.board[move.startRow][move.startCol] = '--'
        self.board[move.endRow][move.endCol] = move.pieceMoved
        self.moveHistory.append(move)
        self.whiteToMove = not self.whiteToMove

    def undoMove(self):
        if len(self.moveHistory) != 0:
            move = self.moveHistory.pop()
            self.board[move.startRow][move.startCol] = move.pieceMoved
            self.board[move.endRow][move.endCol] = move.pieceCaptured
            self.whiteToMove = not self.whiteToMove

    def getValidMoves(self):
        return self.getAllPossibleMoves()

    def getAllPossibleMoves(self):
        moves = []
        for row in range(len(self.board)):
            for col in range(len(self.board[row])):
                turn = self.board[row][col][0]
                if(turn == 'w' and self.whiteToMove) or (turn == 'b' and not self.whiteToMove):
                    piece = self.board[row][col][1]
                    self.moveFunctions[piece](row, col, moves)
        return moves

    def getPawnMoves(self, row, col, moves):
        if self.whiteToMove:
            if self.board[row - 1][col] == "--":
                moves.append(Move((row, col), (row-1, col), self.board))
                if row == 6 and self.board[row-2][col] == "--":
                    moves.append(Move((row, col), (row-2, col), self.board))
            if col-1 >= 0:
                if self.board[row-1][col-1][0] == 'b':
                    moves.append(
                        Move((row, col), (row-1, col-1), self.board))
            if col+1 <= 7:
                if self.board[row-1][col+1][0] == 'b':
                    moves.append(
                        Move((row, col), (row-1, col+1), self.board))
        else:
            if self.board[row+1][col] == "--":
                moves.append(Move((row, col), (row+1, col), self.board))
                if row == 1 and self.board[row+2][col] == "--":
                    moves.append(Move((row, col), (row+2, col), self.board))
            if col-1 >= 0:
                if self.board[row+1][col-1][0] == 'w':
                    moves.append(
                        Move((row, col), (row+1, col-1), self.board))
            if col+1 <= 7:
                if self.board[row+1][col+1][0] == 'w':
                    moves.append(
                        Move((row, col), (row+1, col+1), self.board))

    def getRookMoves(self, row, col, moves):
        # Check up

        # Check down

        # Check right

        # Check left
        pass

    def getBishopMoves(self, row, col, moves):
        pass

    def getKnightMoves(self, row, col, moves):
        pass

    def getQueenMoves(self, row, col, moves):
        pass

    def getKingMoves(self, row, col, moves):
        pass


class Move():
    ranksToRows = {"1": 7, "2": 6, "3": 5, "4": 4,
                   "5": 3, "6": 2, "7": 1, "8": 0}
    rowsToRanks = {v: k for k, v in ranksToRows.items()}
    filesToCols = {"a": 0, "b": 1, "c": 2, "d": 3,
                   "e": 4, "f": 5, "g": 6, "h": 7}
    colsToFiles = {v: k for k, v in filesToCols.items()}

    def __init__(self, start, end, board):
        self.startRow = start[0]
        self.startCol = start[1]
        self.endRow = end[0]
        self.endCol = end[1]
        self.pieceMoved = board[self.startRow][self.startCol]
        self.pieceCaptured = board[self.endRow][self.endCol]
        self.moveID = self.startRow * 1000 + self.startCol * \
            100 + self.endRow * 10 + self.endCol

    def __eq__(self, other):
        if isinstance(other, Move):
            return self.moveID == other.moveID
        return False

    def getChessNotation(self):
        return self.getRankFile(self.startRow, self.startCol) + self.getRankFile(self.endRow, self.endCol)

    def getRankFile(self, r, c):
        return self.colsToFiles[c] + self.rowsToRanks[r]


if __name__ == '__main__':
    gs = GameState()
    print(gs.board.shape)
    print(gs.moveHistory)
