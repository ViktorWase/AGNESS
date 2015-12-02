# -*- coding: cp1252 -*-
from random import randint
from random import gauss
import random
#from tictactoeRules import *
from parameters import *
from copy import copy
from math import sqrt
from math import log
from time import time
from ANNalgorithm import ANN

def shift(l, n):
    l2 = list(l)
    return l2[n:] + l2[:n]

class monteNode:
    def __init__(self, parent, field, playerNr, rules,c, moveNr):
        self.parent = parent
        self.playerNr = playerNr
        self.field = list(field)
        self.wins = 0
        self.losses = 0
        self.draws = 0
        self.leaf = True
        self.c = c
        self.rules = copy(rules)
        self.rules.playerNr = playerNr #IIIIIIIIIINTE HELT HUNDRA P� DEN H�R RADEN!
        self.moveNr = moveNr
        self.children = [None]*len(rules.returnAllLegalMoves(field))

    def pickExploreNode(self, nodeIndependentPlayerNr):
        counter = 0

        if nodeIndependentPlayerNr == self.playerNr:
            bestVal = -1
            bestIndex = 0
        else:
            bestVal = 1
            bestIndex = 0
        totalSimulations = 0
        for child in self.children:
            if(child == None):
                return counter
            totalSimulations += child.wins+child.draws+child.losses
            counter += 1
        totalSimulations = float(totalSimulations)
        counter = 0
        for child in self.children:
            n = child.wins+child.losses+child.draws
            if n == 0:
                return counter
            #This function HAS GOT TO CHANGE. It works and all, but could
            #probably be improved with an ANN or some GEP.
            tmp = float(child.wins)/n+ self.c*sqrt(log(totalSimulations)/n)
            #Make the move that's best if it's your turn, otherwise you make the
            #move that's worst for you. (Minimax as it's called.)
            if (tmp >= bestVal and nodeIndependentPlayerNr == self.playerNr) or ((tmp < bestVal and nodeIndependentPlayerNr != self.playerNr)):
                bestVal = tmp
                bestIndex = counter
            counter += 1
        return bestIndex

    def explore(self, nodeIndependentPlayerNr):
        if(len(self.children)==0):
            #Something should probably happen here. Like something big. Maybe a parade or something. Is there a library that opens the cd tray and then there's a cookie in there? That's what should happen here.
            p = self.rules.playerNr
            if(self.rules.isOver(self.field)):
                if(self.rules.hasWon(self.field)):
                    if(p == nodeIndependentPlayerNr):
                        w = 1
                    else:
                        w =-1
                elif(self.rules.hasLost(self.field)):
                    if(p == nodeIndependentPlayerNr):
                        w =-1
                    else:
                        w = 1
                elif(self.rules.isDraw(self.field)):
                    w = 0

            if(w == 1):
                self.backPropagation(1)
            elif(w == -1):
                self.backPropagation(2)
            elif(w == 0):
                self.backPropagation(0)
            else:
                print "ERROR. again. monte simulate. oops"
            return False
        r = self.pickExploreNode(nodeIndependentPlayerNr)
        if(self.children[r] == None):
            field = list(self.field)
            self.leaf = False
            moves = self.rules.returnAllLegalMoves(field)
            field = self.rules.makeMove(list(field), moves[r], self.playerNr)

            newRules = copy(self.rules)
            newRules.playerNr = self.rules.otherPlayerNr()

            self.children[r] = monteNode(self, list(field), newRules.playerNr, newRules, self.c, self.moveNr+1)
            w = self.children[r].simulateRandomGame(nodeIndependentPlayerNr)

            #Shouldn't these start at self.children[r]? FIX!
            if(w == 1):
                self.backPropagation(1)
            elif(w == -1):
                self.backPropagation(2)
            elif(w == 0):
                self.backPropagation(0)
            else:
                print "error. again. monte simulate.",
                print " w=",
                print w
        else:
            self.children[r].explore(nodeIndependentPlayerNr)

    def backPropagation(self, winner):
        if(winner == 1):
            self.wins += 1
        elif(winner == 2):
            self.losses += 1
        else:
            self.draws += 1
        if(self.parent != None):
            self.parent.backPropagation(winner)

    def simulateRandomGame(self, nodeIndependentPlayerNr):
        keepGoing = True
        players = self.rules.getPlayerList()

        rules = copy(self.rules)
        rules.playerNr = self.playerNr

        players = shift(list(players),self.playerNr)
        field = list(self.field)
        while(keepGoing):
            for p in players:
                rules.playerNr = p
                moves = rules.returnAllLegalMoves(field)
                if(len(moves)!=0):
                    rand = randint(0, len(moves)-1)
                    field = rules.makeMove(list(field),moves[rand],p)
                else:
                    if(rules.isOver(field)):
                        keepGoing = False
                        if(rules.hasWon(field)):
                            if(p == nodeIndependentPlayerNr):
                                return 1
                            else:
                                return -1
                        elif(rules.hasLost(field)):
                            if(p == nodeIndependentPlayerNr):
                                return -1
                            else:
                                return 1

                        elif(rules.isDraw(field)):
                            return 0
                        else:
                            print "Yeah. so. There's an error in simulateRandomGame."
                            return False

                    print "Riiiight, big error here. It's in rebuild 2 monte. Fuck that file."
                    return
                if(rules.isOver(field)):
                    keepGoing = False
                    if(rules.hasWon(field)):
                        if(p == nodeIndependentPlayerNr):
                            return 1
                        else:
                            return -1
                    elif(rules.hasLost(field)):
                        if(p == nodeIndependentPlayerNr):
                            return -1
                        else:
                            return 1

                    elif(rules.isDraw(field)):
                        return 0
                    else:
                        print "Yeah. so. There's an error in simulateRandomGame."
                        return False

class montePlayer:
    """
        A player based on Monte Carlo Tree Search.
        So far it only handles zero-sum 2P games. And no randomness.
        But when it comes to choosing a move it uses an ANN with weights
        determined by some evolutionary algorithm.
    """
    def __init__(self, w,c,sigma, playerNr, rules):
        self.field = rules.getNewBoard()
        self.root = monteNode(None, list(self.field), 1, copy(rules),c,0)
        self.playerNr = playerNr
        self.rules = copy(rules)
        self.rules.playerNr = playerNr
        self.w = list(w)
        self.c = float(c)
        self.sigma = sigma
        for i in range(len(self.root.children)):
            self.root.explore(self.playerNr)

    def setPlayerNr(self, playerNr):
        self.playerNr = playerNr
        self.rules.playerNr = playerNr

    def resetPlayer(self):
        self.rules.playerNr = self.playerNr
        self.field = self.rules.getNewBoard()
        self.root = monteNode(None, list(self.field), 1, copy(self.rules),self.c,0)
        if(self.playerNr != 1): #INTE HELT HUNDRA P� DEN H�R IF-SATSEN!
            for i in range(len(self.root.children)):
                self.root.explore(self.playerNr)

    def findChildNode(self,field):
        if field == self.root.field:
            return
        counter = 0
        foundIt = False
        #print self.root.children
        for child in self.root.children:
            if child != None:
                #print child.field
                if (child.field == field):
                    #print "found it!"
                    foundIt = True
                    break
            counter += 1
        if(foundIt == False):
            print "Didn't find the node. If this happens a lot it's gonna be a problem"
            tmpRules = copy(self.rules)
            self.root = monteNode(None, list(field), self.playerNr, tmpRules,self.c, self.root.moveNr+1)

        else:
            self.root = self.root.children[counter]
            self.root.parent = None

    """
    def pickChildNode(self):
        bestMoveNr=-1
        bestVal =-100000000000
        counter = 0
        for child in self.root.children:
            if(child != None):
                #Make this line better. Maybe using ANN or stuff.
                val = -child.losses
                if(val>=bestVal):
                    bestVal = val
                    bestMoveNr = counter
            counter += 1
        self.root = self.root.children[bestMoveNr]
        self.root.parent = None
        return list(self.root.field)
    """

    def pickChildNodeUsingANN(self):
        bestMoveNr=-1
        bestVal =-1
        counter = 0
        for child in self.root.children:
            if(child != None):
                val = ANN([float(child.wins), float(child.losses), float(child.draws), float(child.moveNr)],3,[6, 5,4],self.w, True)
                if(val>=bestVal):
                    bestVal = val
                    bestMoveNr = counter
            counter += 1
        self.root = self.root.children[bestMoveNr]
        self.root.parent = None
        return list(self.root.field)

    def spawnChild(self):
        sigma = self.sigma + random.gauss(0.0,self.sigma/2.0)
        c = self.c + random.gauss(0, self.sigma)
        tmp_w = list(self.w)
        for i in range(len(tmp_w)):
            tmp_w[i] += random.gauss(0.0, self.sigma)
        child = montePlayer(tmp_w, c,sigma,self.playerNr,copy(self.rules))
        return child

    def makeAMove(self,f):
        """
            This is the function that should be called from
            outside. It takes a board (array) from outside and
            then makes its move and returns a new board (array).
        """
        #print "makes move!"
        for child in self.root.children:
            if(child == None):
                self.root.explore(self.playerNr)
        self.findChildNode(list(f))
        oldTime = time()
        #for i in range(81):
        while(time()-oldTime<0.5):
            #print i
            self.root.explore(self.playerNr)
        f = self.pickChildNodeUsingANN()
        return f

class montePlayerCoop:
    """
        A player based on Monte Carlo Tree Search.
        Same as above, but this one learns to
        cooperate instead of competing.
        It should be noted that the rule-file will
        look sligthly different. Instead of the
        hasLost, hasWon, isDraw functions there
        will be one function: returnValue. This
        is the value that will be maximized.
    """
    def __init__(self, w,c,sigma, playerNr, rules):
        self.field = rules.getNewBoard()
        self.root = monteNodeCoop(None, list(self.field), 1, copy(rules),c,0,-1)
        self.playerNr = playerNr
        self.rules = copy(rules)
        self.rules.playerNr = playerNr
        self.w = list(w)
        self.c = float(c)
        self.sigma = sigma
        #print len(self.root.children)
        #print "hm"
        for i in range(len(self.root.children)):
            #print i
            self.root.explore(self.playerNr)

    def setPlayerNr(self, playerNr):
        self.playerNr = playerNr
        self.rules.playerNr = playerNr

    def resetPlayer(self):
        self.rules.playerNr = self.playerNr
        self.field = self.rules.getNewBoard()
        self.root = monteNode(None, list(self.field), 1, copy(self.rules),self.c,0,-1)
        if(self.playerNr != 1): #INTE HELT HUNDRA P� DEN H�R IF-SATSEN!
            for i in range(len(self.root.children)):
                self.root.explore(self.playerNr)

    def findChildNode(self,field):
        if field == self.root.field:
            return
        counter = 0
        foundIt = False
        #print self.root.children
        for child in self.root.children:
            if child != None:
                #print child.field
                if (child.field == field):
                    #print "found it!"
                    foundIt = True
                    break
            counter += 1
        if(foundIt == False):
            print "Didn't find the node. If this happens a lot it's gonna be a problem"
            tmpRules = copy(self.rules)
            self.root = monteNodeCoop(None, list(field), self.playerNr, tmpRules,self.c, self.root.moveNr+1,-1)

        else:
            self.root = self.root.children[counter]
            self.root.parent = None

    def pickChildNodeUsingANN(self):
        bestMoveNr=-1
        bestVal =-1
        counter = 0
        for child in self.root.children:
            if(child != None):
                val = ANN([float(child.wins), float(child.losses), float(child.draws), float(child.moveNr)],3,[6, 5,4],self.w, True)
                if(val>=bestVal):
                    bestVal = val
                    bestMoveNr = counter
            counter += 1
        self.root = self.root.children[bestMoveNr]
        self.root.parent = None
        return list(self.root.field)

    def spawnChild(self):
        sigma = self.sigma + random.gauss(0.0,self.sigma/2.0)
        c = self.c + random.gauss(0, self.sigma)
        tmp_w = list(self.w)
        for i in range(len(tmp_w)):
            tmp_w[i] += random.gauss(0.0, self.sigma)
        child = montePlayer(tmp_w, c,sigma,self.playerNr,copy(self.rules))
        return child

    def makeAMove(self,f):
        """
            This is the function that should be called from
            outside. It takes a board (array) from outside and
            then makes its move and returns a new board (array).
        """
        #print "makes move!"
        for child in self.root.children:
            if(child == None):
                self.root.explore(self.playerNr)
        self.findChildNode(list(f))
        oldTime = time()
        #for i in range(81):
        while(time()-oldTime<0.5):
            #print i
            self.root.explore(self.playerNr)
        f = self.pickChildNodeUsingANN()
        return f

class monteNodeCoop:
    def __init__(self, parent, field, playerNr, rules,c, moveNr, indexNr):
        #print "start"
        self.parent = parent
        self.playerNr = playerNr
        self.field = list(field)
        self.indexNr = indexNr
        #self.wins = 0
        #self.losses = 0

        #The value of the node.
        self.value = 0
        #The variance of the values of the children. (Can only be
        #calculated fully if all children have been visited.)
        self.childVar = -1
        self.childMean = -1
        #The number of simulations
        self.totalSimulations = 0
        #The mean of the output of all simulations from all the
        #children of this node.
        self.meanTerminalCulmValOfSimulations = 0

        #This is the culmative value
        #(The sum of value of all its parents)
        #This should be maximized.
        self.culmValue = rules.returnValue(field)

        if self.parent == None:
            self.value = self.culmValue
        else:
            self.value = self.culmValue - self.parent.culmValue

        self.bestCulmValOfTerminalChild = -1
        self.indexOfBestCulmValOfTerminalChild = -1

        self.leaf = True
        self.c = c
        self.rules = copy(rules)
        self.rules.playerNr = playerNr #IIIIIIIIIINTE HELT HUNDRA P� DEN H�R RADEN!
        self.moveNr = moveNr
        self.children = [None]*len(rules.returnAllLegalMoves(field))

        #print "end"

    def calcMeanAndVarOfChildren(self):
        li = []
        for child in self.children:
            if child!=None:
                li.append(child.value)
        self.mean = float(sum(li))/len(li)
        self.variance = 0
        for i in range(len(l)):
            self.variance = self.variance + (li[i]-self.mean)*(li[i]-self.mean)
        self.variance = self.variance/float(len(li))

    def pickExploreNode(self):
        counter = 0
        bestVal = -1
        bestIndex = -1
        totalSimulations = float(self.totalSimulations)
        counter = 0
        for child in self.children:
            if child == None:
                return counter #Is it necessary to evaluate every child? FIX!

            #This function HAS GOT TO CHANGE. It works and all, but could
            #probably be improved with an ANN or some GEP.
            #tmp = float(child.wins)/n+ self.c*sqrt(log(totalSimulations)/n)
            tmp = random.random()# 1.0/(totalSimulations+1); #FIX!

            #Make the move that's best if it's your turn, otherwise you make the
            #move that's worst for you. (Minimax as it's called.)
            if tmp >= bestVal and (child.leaf == False):
                bestVal = tmp
                bestIndex = counter
            counter += 1
        if bestIndex == -1:
            print "ERROR!"
        return bestIndex

    def explore(self, nodeIndependentPlayerNr):
        if(len(self.children)==0):
            #Something should probably happen here. Like something big. Maybe a parade or something. Is there a library that opens the cd tray and then there's a cookie in there? That's what should happen here.
            val = self.rules.returnValue(self.field)
            self.backPropagation(val)
            #Should probably update culmValue here. FIX!
            if(self.parent != None and self.indexNr != -1):
                #print self.field
                self.parent.backPropagationOfTerminalNode(self.culmValue, self.indexNr)
            return
        r = self.pickExploreNode()
        if(self.children[r] == None):
            field = list(self.field)
            self.leaf = False
            moves = self.rules.returnAllLegalMoves(field)
            field = self.rules.makeMove(list(field), moves[r], self.playerNr)

            newRules = copy(self.rules)
            newRules.playerNr = self.rules.otherPlayerNr()

            self.children[r] = monteNodeCoop(self, list(field), newRules.playerNr, newRules, self.c, self.moveNr+1,r)
            if(self.children[r].rules.isOver(self.children[r].field)):
                val = self.children[r].culmValue
                self.children[r].backPropagation(val) #Changed these.
                self.children[r].backPropagationOfTerminalNode(self.children[r].culmValue, self.indexNr)
                self.children[r].leaf = True
            else:
                val = self.children[r].simulateRandomGame(nodeIndependentPlayerNr)
                self.backPropagation(val)
        else:
            self.children[r].explore(nodeIndependentPlayerNr)

    def backPropagationOfTerminalNode(self, culmVal, indexNr):
        if culmVal>self.bestCulmValOfTerminalChild:
            self.bestCulmValOfTerminalChild = culmVal
            self.indexOfBestCulmValOfTerminalChild = indexNr
            if self.parent != None:
                self.parent.backPropagationOfTerminalNode(culmVal, self.indexNr)

    def backPropagation(self, val):
        self.meanTerminalCulmValOfSimulations = float(val+self.totalSimulations*self.meanTerminalCulmValOfSimulations)/(self.totalSimulations+1.0)
        self.totalSimulations +=  1
        if(self.parent != None):
            self.parent.backPropagation(val)

    def simulateRandomGame(self, nodeIndependentPlayerNr):
        keepGoing = True
        players = self.rules.getPlayerList()

        rules = copy(self.rules)
        rules.playerNr = self.playerNr

        players = shift(list(players),self.playerNr)
        field = list(self.field)
        while(keepGoing):
            for p in players:
                rules.playerNr = p
                moves = rules.returnAllLegalMoves(field)
                if(len(moves)!=0):
                    rand = randint(0, len(moves)-1)
                    field = rules.makeMove(list(field),moves[rand],p)
                else:
                    if(rules.isOver(field)):
                        val = rules.returnValue(field)
                        return val
                    print "Riiiight, big error here. It's in rebuild 2 monte. Fuck that file."
                    return
                if(rules.isOver(field)):
                    val = rules.returnValue(field)
                    return val
