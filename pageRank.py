import math
from random import *
from copy import copy

def printField(f):
    for i in range(3):
        for j in range(3):
            for k in range(3):
                print f[i*3 + j * 9 + k],
            print "|",
        print "\n",
        if(i==2 or i==5):
            print "------------------"
    for i in range(3):
        for j in range(3):
            for k in range(3):
                print f[27+i*3 + j * 9 + k],
            print "|",
        print "\n",
        if(i==2 or i==5):
            print "------------------"
    for i in range(3):
        for j in range(3):
            for k in range(3):
                print f[6*9+i*3 + j * 9 + k],
            print "|",
        print "\n",
        if(i==2 or i==5):
            print "------------------"


def matMult(A,B, n):
    C = [[0.0 for col in range(n)] for row in range(n)]
    su = 0
    for c in range(n):
        for d in range(n):
            for k in range(n):
                su = su + A[c][k]*B[k][d]
            C[c][d] = su
            su = 0
    return C

def vecMatMult(A,v,n):
    y = [0.0 for col in range(n)]
    for i in range(n):
        for j in range(n):
            y[i] = y[i] + A[i][j]*v[j]
    return y

def pagerank(A, n):
    x = [1.0/n for col in range(n)]
    B = A
    for i in range(600):
        B = matMult(A,B,n)
    eig = vecMatMult(B,x,n)
    return eig

def findSurvivours(winMatrix, n):
    #print winMatrix

    for i in range(n):
        for j in range(n):
            winMatrix[i][j] = winMatrix[i][j]*0.95+0.05
    for i in range(n):
        summa = 0
        for j in range(n):
            summa = summa + winMatrix[j][i]
        for j in range(n):
            winMatrix[j][i] = winMatrix[j][i]/float(summa)

    """for i in range(n):
        summa = 0
        for j in range(n):
            summa = summa + winMatrix[j][i]
        if(summa != 0):
            for j in range(n):
                winMatrix[j][i] = winMatrix[j][i]/ float(summa)
        else:
            for j in range(n):
                winMatrix[j][i] = 1.0 / n"""

    x = pagerank(winMatrix, n)
    print x
    survivingAnns = []
    for i in range(n/2):
        max_val = -1
        max_index = 0
        for j in range(len(x)):
            if(x[j]>=max_val):
                max_val = x[j]
                max_index = j
        x[max_index]=-1.0
        #x.pop(max_index)
        survivingAnns.append(max_index)
    print survivingAnns
    return survivingAnns

def playGame(AIs, rules):
    rules = copy(rules)
    f = rules.getNewBoard()
    AIs[0].playerNr = 1
    AIs[1].playerNr = 2
    AIs[0].resetPlayer()
    AIs[1].resetPlayer()
    rules.playerNr = 1
    while(1):
        for p in AIs:
            f = p.makeAMove(f)
            #printField(f)
            if(rules.isOver(f)):
                #print f
                if(rules.hasWon(f)):
                    #print "WON!"
                    return p.playerNr
                elif(rules.hasLost(f)):
                    #print "LOST!"
                    return p.rules.otherPlayerNr()
                elif(rules.isDraw(f)):
                    #print "draw!"
                    return 0
                else:
                    return "oopsie"
            rules.nextPlayer()

def tournament(AIs, rules):
    n = len(AIs)
    winMatrix = [[0 for col in range(n)] for row in range(n)]
    N = math.floor(1.5*math.log(n))+0
    gameCounter = 0
    nrGames = N*n

    for i in range(n):
        ind = range(n)
        ind.pop(i)
        opponents = []
        for j in range(int(N)):
            opponents.append(ind.pop(randint(0,n-1-1-j)))
        for j in range(len(opponents)):
            win = playGame([AIs[i], AIs[opponents[j]]], rules)
            gameCounter = gameCounter + 1
            print (gameCounter*100)/nrGames,
            print "%,",
            #print win
            if(win == 2):
                winMatrix[opponents[j]][i] = winMatrix[opponents[j]][i] + 1
            elif(win == 1):
                winMatrix[i][opponents[j]] = winMatrix[i][opponents[j]] + 1
    survivours = findSurvivours(winMatrix, n)
    return survivours

def errorOfBoardEval(player, boardEvalObj):
    """
        Uses
    """
    node = player.root
    error = 0.0
    for i in range(10):
        error += boardEvalObj.generalFuncBoardEval(node)
        if node.parent != None:
            node = node.parent
        else:
            break
    return error

def evolveBoardEval(player):
    currentError = player.boardEvalObj.errorOfBoardEval(player)

    boardEvalObj = player.boardEvalObj.returnCopy()
    boardEvalObj.mutate()
    errorOfMutatedObj = boardEvalObj



def playGameWithGeneralBoardEvaluationEvolution(AIs, rules, evoIter):
    """
        This is the same as playGame() but slower since it
        calculates the vector of the deep ANN that evaluates
        the board.
    """
    rules = copy(rules)
    f = rules.getNewBoard()
    AIs[0].playerNr = 1
    AIs[1].playerNr = 2
    AIs[0].resetPlayer()
    AIs[1].resetPlayer()
    rules.playerNr = 1
    while(1):
        for p in AIs:
            f = p.makeAMove(f)
            for i in range(evoIter):
                evolveBoardEval(p)
            #printField(f)
            if(rules.isOver(f)):
                #print f
                if(rules.hasWon(f)):
                    #print "WON!"
                    return p.playerNr
                elif(rules.hasLost(f)):
                    #print "LOST!"
                    return p.rules.otherPlayerNr()
                elif(rules.isDraw(f)):
                    #print "draw!"
                    return 0
                else:
                    return "oopsie"
            rules.nextPlayer()

def tournamentWithGeneralBoardEvaluationEvolution(AIs, rules, iterationsForBoardEvaluationEvolution):
    """
        This is the same as tournament() but slower since it
        calculates the vector of the deep ANN that evaluates
        the board.
    """
    n = len(AIs)
    winMatrix = [[0 for col in range(n)] for row in range(n)]
    N = math.floor(1.5*math.log(n))+1
    gameCounter = 0
    nrGames = N*n

    for i in range(n):
        ind = range(n)
        ind.pop(i)
        opponents = []
        for j in range(int(N)):
            opponents.append(ind.pop(randint(0,n-1-1-j)))
        for j in range(len(opponents)):
            win = playGameWithGeneralBoardEvaluationEvolution([AIs[i], AIs[opponents[j]]], rules, iterationsForBoardEvaluationEvolution)
            gameCounter = gameCounter + 1
            print (gameCounter*100)/nrGames,
            print "%,",
            #print win
            if(win == 2):
                winMatrix[opponents[j]][i] = winMatrix[opponents[j]][i] + 1
            elif(win == 1):
                winMatrix[i][opponents[j]] = winMatrix[i][opponents[j]] + 1
    survivours = findSurvivours(winMatrix, n)
    return survivours
