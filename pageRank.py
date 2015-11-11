from multiprocessing import Pool


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

def tournament(AIs, rules, numberOfCores):
    n = len(AIs)
    winMatrix = [[0 for col in range(n)] for row in range(n)]
    N = math.floor(1.5*math.log(n))+1

    #Make sure that the number of matches is a multiple of the number of cores.
    #N = math.ceil(N*numberOfCores)/numberOfCores
    N = numberOfCores
    #But it shouldn't exceed n-1
    #N = min(N,n-1)
    print N

    gameCounter = 0
    nrGames = N*n

    for i in range(n):
        ind = range(n)
        ind.pop(i)
        opponents = []
        for j in range(int(N)):
            opponents.append(ind.pop(randint(0,n-1-1-j)))
        oppCount = 0
        #for j in range(int(math.round(N/numberOfCores))):
        for j in range(1):
            #Starts a parallel pool of workers, that plays games async-ly.
            #multiprocessing.freeze_support()
            pool = Pool(processes=numberOfCores)
            resultArray = [None]*numberOfCores
            ansArray = [None]* numberOfCores
            for core in range(numberOfCores):
                resultArray[core] = pool.apply_async(playGame, [[copy(AIs[i]), copy(AIs[opponents[oppCount]])], copy(rules)])
                oppCount = oppCount + 1
            for core in range(numberOfCores):
                ansArray[core] = resultArray[core].get(timeout=60*60) #If nothing has happend after an hour, something is wrong.
            #print ansArray

            #win = playGame([copy(AIs[i]), copy(AIs[opponents[j]]]), copy(rules))
            for core in range(numberOfCores):
                win = ansArray[core]
                gameCounter = gameCounter + 1
                print int((gameCounter*100)/nrGames),
                print "%,",
                #print win
                if(win == 2):
                    winMatrix[opponents[j]][i] = winMatrix[opponents[j]][i] + 1
                elif(win == 1):
                    winMatrix[i][opponents[j]] = winMatrix[i][opponents[j]] + 1
                elif(win != 0):
                    print "BIG ERROR IN THE PARALLELIZATION!"
                    print ansArray
    survivours = findSurvivours(winMatrix, n)
    return survivours
