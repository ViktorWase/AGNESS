"""
    The rules for tic-tac-toe co-op mode.
    Both players play with the same markers
    and the goal is to win (together) in as
    few moves as possible. The optimal game
    consists of only 3 moves.
"""

class Rules:
    def __init__(self, playerNr_in):
        self.playerNr = playerNr_in

    def returnAllLegalMoves(self, field):
        moves = []
        for i in range(9):
            if(field[i] == 0):
                moves.append(i)
        return moves

    def getPlayerList(self):
        return [1,1]

    def nextPlayer(self):
        if(self.playerNr == 1):
            self.playerNr = 1
        else:
            self.playerNr = 1
    def otherPlayerNr(self):
        if(self.playerNr == 1):
            return 1
        else:
            return 1

    def makeMove(self, field, n, player):
        field[n] = 1
        return field

    def getNewBoard(self):
        return [0]*9
    def hasWon(self, field):
        f = [[0 for x in range(3)] for y in range(3)]
        counter = 0
        for i in range(3):
            for j in range(3):
                f[i][j] = field[counter]
                counter += 1

        for i in range(3):
            for j in range(3):
                if(f[i][j] != self.playerNr):
                    break
                if(j==2):
                    return True

        for i in range(3):
            for j in range(3):
                if(f[j][i] != self.playerNr):
                    break
                if(j==2):
                    return True

        for i in range(3):
            if(f[i][i] != self.playerNr ):
                break
            if(i==2):
                return True

        for i in range(3):
            if(f[i][2-i] != self.playerNr ):
                break
            if(i==2):
                return True
        return False

    def hasLost(self, field):
        f = [[0 for x in range(3)] for y in range(3)]
        counter = 0
        for i in range(3):
            for j in range(3):
                f[i][j] = field[counter]
                counter += 1
        if(self.playerNr == 1):
            opponentNr = 2
        else:
            opponentNr =1
        for i in range(3):
            for j in range(3):
                if(f[i][j] != opponentNr):
                    break
                if(j==2):
                    return True

        for i in range(3):
            for j in range(3):
                if(f[j][i] != opponentNr):
                    break
                if(j==2):
                    return True

        for i in range(3):
            if(f[i][i] != opponentNr):
                break
            if(i==2):
                return True

        for i in range(3):
            if(f[i][2-i] != opponentNr):
                break
            if(i==2):
                return True
        return False
    def isDraw(self, field):
        moves = self.returnAllLegalMoves(field)
        if (len(moves)==0):
            return True
        else:
            return False
    def isOver(self, field):
        return self.hasWon(field) or self.hasLost(field) or self.isDraw(field)

    def returnValue(self, field):
        if self.isOver(field)==False:
            return 0.0
        else:
            return 1.0/float(sum(field));
