class Rules:
    def __init__(self, playerNr_in):
        self.playerNr = playerNr_in

    def fillMetafield(self, field):
        metafield = [0] * 9
        for i in range(9):
            counter = 9*i
            tmp = [[0 for col in range(3)] for row in range(3)]
            for x in range(3):
                for y in range(3):
                    tmp[x][y] = field[counter]
                    counter += 1
            metafield[i] = self.helpFunction(tmp)
        return metafield

    def returnAllLegalMoves(self, field):
        moves = []
        prevMove = field[81]
        metafield = [0]*9
        if(prevMove == -1):
            metafield = self.fillMetafield(field)
            for i in range(81):
                if(field[i] == 0 and metafield[i/9]==0):
                    moves.append(i)
            return moves
        else:
            counter = 9*prevMove
            tmp = [[0 for col in range(3)] for row in range(3)]
            for x in range(3):
                for y in range(3):
                    counter += 1
            meta = self.helpFunction(tmp)
            if(meta==0):
                counter = prevMove*9
                for i in range(9):
                    if(field[counter] == 0):
                        moves.append(counter)
                    counter += 1
            else:
                metafield = self.fillMetafield(field)
                for i in range(81):
                    if(field[i] == 0 and metafield[i/9]==0):
                        moves.append(i)
            if (moves != []):
                return moves
            else:
                metafield = self.fillMetafield(field)
                for i in range(81):
                    if(field[i] == 0 and metafield[i/9]==0):
                        moves.append(i)
                return moves

    """def returnAllLegalMoves(self, field):
        moves = []
        prevMove = field[81]
        if(prevMove == -1):
            metafield = [0] * 9
            for i in range(9):
                counter = 9*i
                tmp = [[0 for col in range(3)] for row in range(3)]
                for x in range(3):
                    for y in range(3):
                        tmp[x][y] = field[counter]
                        counter += 1
            metafield[i] = self.helpFunction(tmp)
            for i in range(81):
                if(field[i] == 0 and metafield[i/9]==0):
                    moves.append(i)
            return moves
        else:
            counter = 9*prevMove
            tmp = [[0 for col in range(3)] for row in range(3)]
            for x in range(3):
                for y in range(3):
                    tmp[x][y] = field[counter]
                    counter += 1
            meta = self.helpFunction(tmp)

            if(meta == 0):
                counter = prevMove*9
                #print counter
                for i in range(9):
                    #print counter
                    if(field[counter] == 0):
                        moves.append(counter)
                    counter += 1
                if(moves == []):
                    metafield = [0] * 9
                    for i in range(9):
                        counter = 9*i
                        tmp = [[0 for col in range(3)] for row in range(3)]
                        for x in range(3):
                            for y in range(3):
                                tmp[x][y] = field[counter]
                                counter += 1
                        metafield[i] = self.helpFunction(tmp)
                    for i in range(81):
                        if(field[i] == 0 and metafield[i/9]==0):
                            moves.append(i)
                    return moves
                else:

                    metafield = [0] * 9
                    for i in range(9):
                        counter = 9*i
                        tmp = [[0 for col in range(3)] for row in range(3)]
                        for x in range(3):
                            for y in range(3):
                                tmp[x][y] = field[counter]
                                counter += 1
                    metafield[i] = self.helpFunction(tmp)
                    for i in range(81):
                        if(field[i] == 0 and metafield[i/9]==0):
                            moves.append(i)
                    return moves

            else:
                return moves
    """

    def getPlayerList(self):
        return [1,2]

    def nextPlayer(self):
        if(self.playerNr == 1):
            self.playerNr = 2
        else:
            self.playerNr = 1
    def otherPlayerNr(self):
        if(self.playerNr == 1):
            return 2
        else:
            return 1

    def makeMove(self, field, n, player):
        field[n] = player
        field[81] = n-int (n/9)*9
        tmp = [[0 for col in range(3)] for row in range(3)]
        counter = field[81]*9

        nrEmptySquares = 0
        for x in range(3):
            for y in range(3):
                tmp[x][y] = field[counter]
                if(field[counter] == 0):
                    nrEmptySquares += 1
                counter += 1
        if(nrEmptySquares == 0):
            field[81] = -1
        elif(self.helpFunction(tmp) == 1 or self.helpFunction(tmp) == 2):
            field[81] = -1

        return field

    def getNewBoard(self):
        #So the 82nd element keeps track of
        #where the previous move went.
        f=[0]*82
        f[81] = -1
        return f


    def helpFunction(self, smallfield):
        #print smallfield
        for p in [1, 2]:
            for x in range(3):
                for y in range(3):
                    if(smallfield[x][y] != p):
                        break
                    elif(y == 2):
                        return p
            for y in range(3):
                for x in range(3):
                    if(smallfield[x][y] != p):
                        break
                    elif(x == 2):
                        return p
            for x in range(3):
                if(smallfield[x][2-x] != p):
                    break
                elif(x == 2):
                    return p
            for y in range(3):
                if(smallfield[y][y] != p): #if(smallfield[2-y][y] != p):
                    break
                elif(y==2):
                    return p
        return 0

    def hasWon(self, field):
        metafield = [0]* 9
        for i in range(9):
            counter = 9*i
            tmp = [[0 for col in range(3)] for row in range(3)]
            for x in range(3):
                for y in range(3):
                    tmp[x][y] = field[counter]
                    counter += 1
            metafield[i] = self.helpFunction(tmp)
        counter = 0
        #print metafield
        out = [[0 for col in range(3)] for row in range(3)]
        for x in range(3):
            for y in range(3):
                out[x][y] = metafield[counter]
                counter += 1
        #print out
        #print metafield
        #print self.helpFunction(out)
        return self.helpFunction(out)==self.playerNr

    def hasLost(self, field):
        metafield = [0]* 9
        for i in range(9):
            counter = 9*i
            tmp = [[0 for col in range(3)] for row in range(3)]
            for x in range(3):
                for y in range(3):
                    tmp[x][y] = field[counter]
                    counter += 1

            metafield[i] = self.helpFunction(tmp)
        #print metafield
        counter = 0
        out = [[0 for col in range(3)] for row in range(3)]
        for x in range(3):
            for y in range(3):
                out[x][y] = metafield[counter]
                counter += 1
        return self.helpFunction(out)==self.otherPlayerNr()

    def isDraw(self, field):
        moves = self.returnAllLegalMoves(field)
        if (len(moves)==0):
            return True
        else:
            return False
    def isOver(self, field):
        return self.hasWon(field) or self.hasLost(field) or self.isDraw(field)
