import numpy as np

opponentDict = {'w': 'b', 'b': 'w'}


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
                              "B": self.getBishopMoves, "Q": self.getQueenMoves, "K": self.getKingMoves}
        self.whiteToMove = True
        self.moveHistory = []
        self.whiteKingLocation = (7, 4)
        self.blackKingLocation = (0, 4)
        self.checkmate = False
        self.stalemate = False

    def makeMove(self, move):
        self.board[move.startRow][move.startCol] = '--'
        self.board[move.endRow][move.endCol] = move.pieceMoved
        self.moveHistory.append(move)
        self.whiteToMove = not self.whiteToMove
        if move.pieceMoved == "wK":
            self.whiteKingLocation = (move.endRow, move.endCol)
        elif move.pieceMoved == "bK":
            self.blackKingLocation = (move.endRow, move.endCol)

    def undoMove(self):
        if len(self.moveHistory) != 0:
            move = self.moveHistory.pop()
            self.board[move.startRow][move.startCol] = move.pieceMoved
            self.board[move.endRow][move.endCol] = move.pieceCaptured
            self.whiteToMove = not self.whiteToMove
            if move.pieceMoved == "wK":
                self.whiteKingLocation = (move.startRow, move.startCol)
            elif move.pieceMoved == "bK":
                self.blackKingLocation = (move.startRow, move.startCol)

    def getValidMoves(self):
        moves = self.getAllPossibleMoves()

        for i in range(len(moves)-1, -1, -1):
            self.makeMove(moves[i])
            self.whiteToMove = not self.whiteToMove
            if self.inCheck():
                moves.remove(moves[i])
            self.whiteToMove = not self.whiteToMove
            self.undoMove()
        
        if len(moves)==0:
            if self.inCheck():
                self.checkmate = True
            else:
                self.stalemate = True
        else:
            self.checkmate = False
            self.stalemate = False

        return moves

    def inCheck(self):
        if self.whiteToMove:
            return self.isAttacking(self.whiteKingLocation[0], self.whiteKingLocation[1])
        else:
            return self.isAttacking(self.blackKingLocation[0], self.blackKingLocation[1])

    def isAttacking(self, row, col):
        self.whiteToMove = not self.whiteToMove
        moves = self.getAllPossibleMoves()
        self.whiteToMove = not self.whiteToMove
        for move in moves:
            if move.endRow == row and move.endCol == col:
                return True
        return False

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
            if row + 1 < 8:
                if self.board[row+1][col] == "--":
                    moves.append(Move((row, col), (row+1, col), self.board))
                    if row == 1 and self.board[row+2][col] == "--":
                        moves.append(
                            Move((row, col), (row+2, col), self.board))
                if col-1 >= 0:
                    if self.board[row+1][col-1][0] == 'w':
                        moves.append(
                            Move((row, col), (row+1, col-1), self.board))
                if col+1 <= 7:
                    if self.board[row+1][col+1][0] == 'w':
                        moves.append(
                            Move((row, col), (row+1, col+1), self.board))

    def getRookMoves(self, row, col, moves):
        color = self.board[row][col][0]
        opponent = opponentDict[color]

        for i in range(4):
            dr = 0
            dc = 0
            while True:
                if i == 0:
                    dr += 1
                elif i == 1:
                    dr -= 1
                elif i == 2:
                    dc += 1
                elif i == 3:
                    dc -= 1
                if (row + dr >= 8) or (row + dr < 0) or (col + dc >= 8) or (col + dc < 0):
                    break
                if self.board[row + dr][col + dc] == "--":
                    moves.append(
                        Move((row, col), (row + dr, col + dc), self.board))
                if self.board[row + dr][col + dc][0] == opponent:
                    moves.append(
                        Move((row, col), (row + dr, col + dc), self.board))
                    break
                if self.board[row + dr][col + dc][0] == color:
                    break

    def getBishopMoves(self, row, col, moves):
        color = self.board[row][col][0]
        opponent = opponentDict[color]

        for i in range(4):
            dr = 0
            dc = 0
            while True:
                if i == 0:
                    dr += 1
                    dc += 1
                elif i == 1:
                    dr -= 1
                    dc += 1
                elif i == 2:
                    dr += 1
                    dc -= 1
                elif i == 3:
                    dr -= 1
                    dc -= 1
                if (row + dr >= 8) or (row + dr < 0) or (col + dc >= 8) or (col + dc < 0):
                    break
                if self.board[row + dr][col + dc] == "--":
                    moves.append(
                        Move((row, col), (row + dr, col + dc), self.board))
                if self.board[row + dr][col + dc][0] == opponent:
                    moves.append(
                        Move((row, col), (row + dr, col + dc), self.board))
                    break
                if self.board[row + dr][col + dc][0] == color:
                    break



    def getKnightMoves(self, row, col, moves):
        color = self.board[row][col][0]
        opponent = opponentDict[color]

        for i in range(8):
            dr = 0
            dc = 0
            if i == 0:
                dr -= 2
                dc += 1
            elif i == 1:
                dr -= 2
                dc -= 1
            elif i == 2:
                dr += 2
                dc += 1
            elif i == 3:
                dr += 2
                dc -= 1
            elif i == 4:
                dr -= 1
                dc += 2
            elif i == 5:
                dr += 1
                dc += 2
            elif i == 6:
                dr -= 1
                dc -= 2
            elif i == 7:
                dr += 1
                dc -= 2
            if (row + dr >= 8) or (row + dr < 0) or (col + dc >= 8) or (col + dc < 0):
                continue
            if self.board[row + dr][col + dc] == "--":
                moves.append(
                    Move((row, col), (row + dr, col + dc), self.board))
            if self.board[row + dr][col + dc][0] == opponent:
                moves.append(
                    Move((row, col), (row + dr, col + dc), self.board))

    def getQueenMoves(self, row, col, moves):
        color = self.board[row][col][0]
        opponent = opponentDict[color]

        for i in range(8):
            dr = 0
            dc = 0
            while True:
                if i == 0:
                    dr += 1
                    dc += 1
                elif i == 1:
                    dr -= 1
                    dc += 1
                elif i == 2:
                    dr += 1
                    dc -= 1
                elif i == 3:
                    dr -= 1
                    dc -= 1
                elif i == 4:
                    dr += 1
                elif i == 5:
                    dr -= 1
                elif i == 6:
                    dc += 1
                elif i == 7:
                    dc -= 1
                if (row + dr >= 8) or (row + dr < 0) or (col + dc >= 8) or (col + dc < 0):
                    break
                if self.board[row + dr][col + dc] == "--":
                    moves.append(
                        Move((row, col), (row + dr, col + dc), self.board))
                if self.board[row + dr][col + dc][0] == opponent:
                    moves.append(
                        Move((row, col), (row + dr, col + dc), self.board))
                    break
                if self.board[row + dr][col + dc][0] == color:
                    break

    def getKingMoves(self, row, col, moves):
        color = self.board[row][col][0]
        opponent = opponentDict[color]
        
        for i in range(8):
            dr = 0
            dc = 0
            if i == 0:
                dr += 1
                dc += 1
            elif i == 1:
                dr -= 1
                dc += 1
            elif i == 2:
                dr += 1
                dc -= 1
            elif i == 3:
                dr -= 1
                dc -= 1
            elif i == 4:
                dr += 1
            elif i == 5:
                dr -= 1
            elif i == 6:
                dc += 1
            elif i == 7:
                dc -= 1
            if (row + dr >= 8) or (row + dr < 0) or (col + dc >= 8) or (col + dc < 0):
                continue
            if self.board[row + dr][col + dc] == "--":
                moves.append(
                    Move((row, col), (row + dr, col + dc), self.board))
            if self.board[row + dr][col + dc][0] == opponent:
                moves.append(
                    Move((row, col), (row + dr, col + dc), self.board))



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
